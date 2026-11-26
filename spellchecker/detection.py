"""Error detection module.

For every token the paper applies, in order:
  1. dictionary look-up in the Tagalog and English automata, then again
     after stemming (handles inflection and English roots with Tagalog
     affixes such as magtext -> text);
  2. if the word has a hyphen: code-switching check (Tagalog prefix +
     English word: nag-text, mag-research) and compound-word check (two
     Tagalog words: bahay-kubo);
  3. n-gram look-up: every trigram of the stem must be among the top
     `threshold` trigrams of the stemmed profile, otherwise the word is
     flagged.

Two optional extensions (config.USE_EXTENSIONS) make the space errors of the
paper's Table I detectable; neither is described in the paper:
  * bound prefix: a prefix written as a separate word ("pag bigay");
  * clitic split: a function word fused with its neighbour ("parin" = pa rin).
"""
from __future__ import annotations

from dataclasses import dataclass

from . import config
from .modeling import LanguageModel
from .morphology import PREFIX_SET, is_prefix_form
from .stemmer import Stemmer
from .tokenizer import normalize


@dataclass
class Detection:
    word: str
    is_error: bool
    method: str            # which step decided
    detail: str = ""
    stem: str | None = None


class ErrorDetector:
    def __init__(self, model: LanguageModel, stemmer: Stemmer | None = None,
                 threshold: float | None = None, use_extensions: bool | None = None) -> None:
        self.model = model
        self.stemmer = stemmer or Stemmer(config.MIN_STEM_LENGTH)
        self.threshold = config.NGRAM_THRESHOLD if threshold is None else threshold
        self.use_extensions = config.USE_EXTENSIONS if use_extensions is None else use_extensions

    # -- helpers shared with the corrector ---------------------------------
    def in_dictionary(self, word: str) -> bool:
        return self.model.in_dictionary(word)

    def is_root(self, stem: str) -> bool:
        """A Tagalog root, or an English root long enough not to match by
        accident (pa-ka-i-'not', ka-i-'big' must not validate a word)."""
        return stem in self.model.tagalog or (
            len(stem) >= config.MIN_ENGLISH_STEM_LENGTH and stem in self.model.english)

    def stems(self, word: str) -> list[str]:
        return self.stemmer.valid_stems(word, self.is_root, exclude=self.model.function_words)

    def is_valid(self, word: str) -> bool:
        """Accepted by the dictionary, directly or after stemming."""
        w = normalize(word)
        return self.in_dictionary(w) or bool(self.stems(w))

    # -- the detection pipeline -------------------------------------------
    def check(self, word: str) -> Detection:
        w = normalize(word)
        if not any(ch.isalpha() for ch in w):
            return Detection(word, False, "skipped")
        bare = w.rstrip("-")
        tl, fw = self.model.tagalog, self.model.function_words

        # 1a. dictionary look-up
        if self.in_dictionary(w):
            return Detection(word, False, "dictionary")
        if w.endswith(("'y", "'t")) and self.in_dictionary(w[:-2]) and w[:-2] not in PREFIX_SET:
            return Detection(word, False, "dictionary", "contraction")

        # extension: a prefix cannot stand alone ("pag bigay", "mag- luto")
        if self.use_extensions and bare in PREFIX_SET and bare not in tl:
            return Detection(word, True, "bound-prefix",
                             f'"{bare}" is a prefix written apart from its root')

        # 1b. dictionary look-up after stemming
        stems = self.stems(w)
        if stems:
            return Detection(word, False, "stemmed-dictionary", f"stem: {stems[0]}", stems[0])

        # 2. code-switching and compound-word checking (hyphenated words)
        if "-" in bare:
            a, _, b = bare.partition("-")
            if is_prefix_form(a, b) and b in self.model.english:
                return Detection(word, False, "code-switching", f"{a}- + English '{b}'")
            if a == b and a in tl:
                return Detection(word, False, "compound", "full reduplication")
            if a in tl and b in tl and a not in fw and b not in fw:
                return Detection(word, False, "compound", f"{a} + {b}")

        # extension: function word fused with another word ("parin", "nalang")
        if self.use_extensions and "-" not in w:
            for k in range(config.MIN_SPLIT_LENGTH, len(w) - config.MIN_SPLIT_LENGTH + 1):
                a, b = w[:k], w[k:]
                if a in tl and b in tl and (a in fw or b in fw):
                    return Detection(word, True, "clitic-split",
                                     f'"{a} {b}" should be two words')

        # 3. n-gram look-up on the stem
        stem = self.stemmer.greedy(w)
        missing = self.model.ngrams.missing(stem, self.threshold)
        if not missing:
            return Detection(word, False, "n-gram", f"all trigrams of '{stem}' are frequent", stem)
        return Detection(word, True, "n-gram",
                         f"rare trigram(s) {', '.join(missing)} in stem '{stem}'", stem)
