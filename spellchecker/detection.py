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

Extensions (config.USE_EXTENSIONS; all switched off by --paper-only), none
of them described in the paper:
  * bound prefix: a prefix written as a separate word ("pag bigay");
  * clitic split: a function word fused with its neighbour ("parin" = pa rin);
  * contractions: "ako'y", "ganito't" accepted when the bare word is known;
  * English-root hyphen: an English word under a Tagalog prefix is set off
    with a hyphen (KWF orthography), so "nagreply" is flagged -> nag-reply;
  * stricter checks on steps the paper does describe -- an English root
    under Tagalog affixes needs >= MIN_ENGLISH_STEM_LENGTH letters, the
    code-switching check also accepts a prefix plus a reduplicated syllable
    (nagte-text), and the compound check rejects function words.
With the extensions off, steps 1-3 are exactly the paper's wording.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import config
from .modeling import LanguageModel
from .morphology import (ASSIMILATE_M, ASSIMILATE_N, PREFIX_SET, is_prefix_before_root,
                         is_prefix_form)
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
        """A stem the dictionary accepts.  The paper maps the stem into both
        automata; the extension also requires an English root long enough not
        to match by accident (pa-ka-i-'not', ka-i-'big' must not validate a word)."""
        if stem in self.model.tagalog:
            return True
        if self.use_extensions and len(stem) < config.MIN_ENGLISH_STEM_LENGTH:
            return False
        return stem in self.model.english

    def stems(self, word: str) -> list[str]:
        return self.stemmer.valid_stems(word, self.is_root, exclude=self.model.function_words)

    def is_valid(self, word: str) -> bool:
        """Accepted by the dictionary, directly or after stemming."""
        w = normalize(word)
        return self.in_dictionary(w) or bool(self.stems(w))

    # -- English roots under Tagalog prefixes (extension) -------------------
    # Filipino orthography (KWF, Ortograpiyang Pambansa) sets an English word
    # that keeps its English spelling apart from a Tagalog affix with a hyphen:
    # i-check, nag-text, nagte-text, ma-save.
    def root_language(self, word: str) -> str | None:
        """'tagalog' (directly or via a Tagalog stem), 'english', or None for a
        word in neither word list."""
        w = normalize(word)
        tl = self.model.tagalog
        if w in tl or w in self.model.function_words:
            return "tagalog"
        if w in self.model.english:
            return "english"
        if any(s in tl for s in self.stems(w)):
            return "tagalog"
        return None

    def looks_foreign(self, word: str) -> bool:
        """The Tagalog trigram profile finds the word rare ('binge': 'nge', 'ge_')."""
        return bool(self.model.ngrams.missing(normalize(word), self.threshold))

    def hyphenations(self, word: str) -> list[str]:
        """Hyphenated spellings of a solid word made of a Tagalog prefix (with
        an optional reduplicated syllable) and an English root, longest root
        first: nagreply -> nag-reply, ipost -> i-post, nagtetext -> nagte-text.
        Assimilated nasal prefixes (pan-, man-, pam- ...) are skipped: they only
        arise before a Tagalog root, so 'pancake' is not pan- + cake."""
        w = normalize(word)
        if "-" in w:
            return []
        out = []
        for k in range(1, len(w) - config.MIN_ENGLISH_STEM_LENGTH + 1):
            a, b = w[:k], w[k:]
            if a in ASSIMILATE_M or a in ASSIMILATE_N:
                continue
            if (is_prefix_before_root(a, b) and b in self.model.english
                    and b not in self.model.tagalog):
                out.append(f"{a}-{b}")
        return out

    # -- the detection pipeline -------------------------------------------
    def check(self, word: str) -> Detection:
        w = normalize(word)
        if not any(ch.isalpha() for ch in w):
            return Detection(word, False, "skipped")
        bare = w.rstrip("-")
        tl, fw = self.model.tagalog, self.model.function_words

        # 1a. dictionary look-up.  Extension: a Tagalog prefix standing alone is
        # not rescued by the English list ("Nag aral": 'nag' is also English).
        prefix_alone = self.use_extensions and bare in PREFIX_SET and bare not in tl
        if w in tl or (w in self.model.english and not (prefix_alone and len(bare) >= 3)):
            return Detection(word, False, "dictionary")
        # extension: contraction of a known word ("ako'y", "ganito't")
        if (self.use_extensions and w.endswith(("'y", "'t")) and self.in_dictionary(w[:-2])
                and w[:-2] not in PREFIX_SET):
            return Detection(word, False, "dictionary", "contraction")

        # extension: a prefix cannot stand alone ("pag bigay", "mag- luto")
        if prefix_alone:
            return Detection(word, True, "bound-prefix",
                             f'"{bare}" is a prefix written apart from its root')

        # 1b. dictionary look-up after stemming
        stems = self.stems(w)
        # extension: an English root fused to a Tagalog prefix needs a hyphen
        # ("nagreply" -> nag-reply), unless the word also has a Tagalog analysis
        if self.use_extensions and not any(s in tl for s in stems):
            fixes = self.hyphenations(w)
            if fixes:
                root = fixes[0].split("-", 1)[1]
                return Detection(word, True, "english-hyphen",
                                 f'the English word "{root}" takes a hyphen after a '
                                 f'Tagalog prefix: {fixes[0]}', root)
        if stems:
            return Detection(word, False, "stemmed-dictionary", f"stem: {stems[0]}", stems[0])

        # 2. code-switching and compound-word checking (hyphenated words):
        #    "the first word is checked if it is a Tagalog prefix and the second
        #    word is checked if it is in English word list ... [else] the module
        #    checks the two words if exists in the Tagalog word list."
        if "-" in bare:
            a, _, b = bare.partition("-")
            if self.use_extensions:
                if is_prefix_form(a, b) and b in self.model.english:
                    return Detection(word, False, "code-switching", f"{a}- + English '{b}'")
                if a == b and a in tl:
                    return Detection(word, False, "compound", "full reduplication")
                if a in tl and b in tl and a not in fw and b not in fw:
                    return Detection(word, False, "compound", f"{a} + {b}")
            else:
                if a in PREFIX_SET and b in self.model.english:
                    return Detection(word, False, "code-switching", f"{a}- + English '{b}'")
                if a in tl and b in tl:
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
