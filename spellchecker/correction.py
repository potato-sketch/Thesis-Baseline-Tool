"""Error correction module.

1. Space-dash correction
   * merge test -- the misspelled word is a Tagalog prefix: merge it with
     the next word following the prefix rules (mag- + kasama -> magkasama,
     mag- + asawa -> mag-asawa);
   * split test -- every split with >= 2 letters per part whose parts are
     both in the dictionary (palang -> pa lang, pal ang, pala ng);
   * dash test (extension, not in the paper) -- drop an illegal hyphen
     (magka-ugnay -> magkaugnay) or add a required one (nagaral -> nag-aral);
   * English-root hyphen (extension) -- an English word keeps a hyphen after
     a Tagalog prefix: nagreply -> nag-reply, and the merge test joins
     "nag binge" as nag-binge.
2. Edit distance -- only if step 1 produced nothing: Levenshtein automaton
   (<= 2 edits) traversed in parallel with the Tagalog DAFSA.
3. Ranking -- Dice coefficient between the Filipino-metaphone codes of the
   misspelled word and of each candidate (ties: fewer edits, then a-z).

Extensions (config.USE_EXTENSIONS; off with --paper-only): the dash test;
edit-distance candidates listed after the space-dash ones; and a split test
that looks the parts up in the Tagalog list only.  With them off, the split
test uses "a dictionary look-up" as the paper says, i.e. both word lists,
exactly as the detection module's dictionary look-up does.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import config
from .detection import ErrorDetector
from .levenshtein import fuzzy_search
from .metaphone import dice, encode
from .morphology import PREFIX_SET, attach_prefix, is_vowel
from .tokenizer import normalize


@dataclass
class Suggestion:
    text: str
    source: str            # merge | split | dash | edit-distance
    score: float = 1.0     # Dice coefficient of the phonetic codes
    distance: int = 0      # edit distance (edit-distance suggestions only)
    span: int = 1          # number of words replaced (2 for a merge)
    end: int | None = None  # filled in by SpellChecker: end offset of the replaced text


class ErrorCorrector:
    def __init__(self, detector: ErrorDetector, max_edits: int | None = None,
                 max_suggestions: int | None = None) -> None:
        self.detector = detector
        self.model = detector.model
        self.max_edits = config.MAX_EDIT_DISTANCE if max_edits is None else max_edits
        self.max_suggestions = config.MAX_SUGGESTIONS if max_suggestions is None else max_suggestions

    def suggest(self, word: str, next_word: str | None = None) -> list[Suggestion]:
        w = normalize(word)
        suggestions = self.space_dash(w, next_word)
        if not suggestions:
            suggestions = self.edit_distance(w)
        elif self.detector.use_extensions and suggestions[0].source != "merge":
            # extension: keep the edit-distance candidates after the space-dash ones
            seen = {s.text for s in suggestions}
            suggestions += [s for s in self.edit_distance(w) if s.text not in seen]
        return suggestions[: self.max_suggestions]

    # ---------------------------------------------------- space-dash correction
    def space_dash(self, w: str, next_word: str | None = None) -> list[Suggestion]:
        ext = self.detector.use_extensions
        found = self.merge_test(w, next_word) or (ext and self.hyphen_test(w)) or self.split_test(w)
        if not found and ext:
            found = self.dash_test(w)
        return found

    def merge_test(self, w: str, next_word: str | None) -> list[Suggestion]:
        prefix = w.rstrip("-")
        if prefix not in PREFIX_SET or not next_word:
            return []
        nxt = normalize(next_word)
        if not any(ch.isalpha() for ch in nxt):
            return []
        merged = attach_prefix(prefix, nxt)
        texts = [merged]
        hyphenated = f"{prefix}-{nxt}"
        if self.detector.use_extensions and hyphenated != merged:
            # extension: an English root keeps its hyphen (nag + update -> nag-update).
            # A root in neither list gets both spellings, the likelier one first
            # (nag + binge -> nag-binge, nagbinge).
            lang = self.detector.root_language(nxt)
            if lang == "english":
                texts = [hyphenated]
            elif lang is None:
                foreign = self.detector.looks_foreign(nxt)
                texts = [hyphenated, merged] if foreign else [merged, hyphenated]
        return [Suggestion(t, "merge", span=2) for t in texts]

    def hyphen_test(self, w: str) -> list[Suggestion]:
        """Extension: nagreply -> nag-reply (English root after a Tagalog prefix)."""
        return [Suggestion(h, "dash") for h in self.detector.hyphenations(w)]

    def split_test(self, w: str) -> list[Suggestion]:
        if self.detector.use_extensions:
            known = self.model.tagalog.__contains__
        else:
            known = self.detector.in_dictionary
        m = config.MIN_SPLIT_LENGTH
        out = []
        for k in range(m, len(w) - m + 1):
            a, b = w[:k], w[k:]
            if "-" in a or "-" in b or "'" in a or "'" in b:
                continue
            if known(a) and known(b):
                out.append(Suggestion(f"{a} {b}", "split"))
        return out

    def dash_test(self, w: str) -> list[Suggestion]:
        out: list[Suggestion] = []
        if "-" in w:
            joined = w.replace("-", "")
            if self.detector.is_valid(joined):
                out.append(Suggestion(joined, "dash"))
        else:
            for k in range(2, min(len(w) - 1, 10)):
                prefix, rest = w[:k], w[k:]
                if prefix in PREFIX_SET and not is_vowel(prefix[-1]) and is_vowel(rest[0]):
                    hyphenated = attach_prefix(prefix, rest)
                    if self.detector.is_valid(hyphenated):
                        out.append(Suggestion(hyphenated, "dash"))
        return out

    # ------------------------------------------------- edit distance + ranking
    def edit_distance(self, w: str) -> list[Suggestion]:
        candidates = fuzzy_search(self.model.tagalog, w, self.max_edits)
        candidates.pop(w, None)
        return self.rank(w, candidates)

    @staticmethod
    def rank(w: str, candidates: dict[str, int]) -> list[Suggestion]:
        code = encode(w)
        scored = [Suggestion(c, "edit-distance", round(dice(code, encode(c)), 4), d)
                  for c, d in candidates.items()]
        scored.sort(key=lambda s: (-s.score, s.distance, s.text))
        return scored
