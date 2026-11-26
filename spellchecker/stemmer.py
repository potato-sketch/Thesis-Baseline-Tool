"""Rule-based Tagalog stemmer ("a built-in stemming system that specifically
handles Filipino linguistic phenomena", in the spirit of Bonus & Roxas, 2003).

Two modes:

* valid_stems(word, is_valid) -- explore every way of undoing affixation
  (prefixes with partial assimilation, infixes, CV reduplication, suffixes
  with o/u alternation, d/r alternation and syncope, linker -ng, hyphenated
  prefixes and full reduplication) and keep the candidates that a dictionary
  accepts.  Used by error detection ("the word will undergo further stemming
  and is mapped again into the automaton") and to build the n-gram profile.
* greedy(word) -- dictionary-free, one pass of the rules.  Used for words
  that no dictionary explains, before their trigrams are checked.
"""
from __future__ import annotations

from typing import Callable, Iterable

from .morphology import (
    ASSIMILATE_M, ASSIMILATE_N, ASSIMILATE_NG, INFIXES, MAX_PREFIX_LENGTH,
    PREFIX_SET, SUFFIXES, first_vowel, has_vowel, is_prefix_form, is_vowel,
    lower_final_u, onset, plausible_start,
)

Validator = Callable[[str], bool]


class Stemmer:
    def __init__(self, min_stem_length: int = 3, max_depth: int = 5) -> None:
        self.min_stem_length = min_stem_length
        self.max_depth = max_depth
        self._cache: dict[str, dict[str, int]] = {}

    # ------------------------------------------------------------------ rules
    def _undo(self, w: str) -> list[str]:
        """Every string obtained by undoing ONE morphological process."""
        out: list[str] = []
        n = len(w)

        if "-" in w:
            a, _, b = w.partition("-")
            if not a or not b:
                return out
            if a == b:                          # full reduplication: araw-araw
                out.append(a)
            elif b.startswith(a):               # bahay-bahayan
                out.append(a)
            elif a.endswith(b):                 # paulit-ulit
                out.append(b)
            # Orthography: the hyphen after a prefix only appears before a vowel
            # (mag-aral, nag-aaral, pinag-usapan).  mag-laro is NOT stemmed.
            if is_vowel(b[0]) and not is_vowel(a[-1]) and is_prefix_form(a):
                out.append(b)
            return out

        # prefixes (with partial assimilation)
        for k in range(min(MAX_PREFIX_LENGTH, n - 2), 0, -1):
            p = w[:k]
            if p not in PREFIX_SET:
                continue
            rest = w[k:]
            if not plausible_start(rest):
                continue
            out.append(rest)
            if is_vowel(rest[0]):
                if p in ASSIMILATE_M:
                    out += ["p" + rest, "b" + rest]
                elif p in ASSIMILATE_N:
                    out += ["t" + rest, "s" + rest, "d" + rest]
                elif p in ASSIMILATE_NG:
                    out.append("k" + rest)

        # infixes -um- / -in- (and their prefix-like variants)
        on = onset(w)
        i = len(on)
        if on and w[i:i + 2] in INFIXES and n > i + 3 and is_vowel(w[i + 2]):
            out.append(on + w[i + 2:])                      # k-um-ain, s-in-ulat
        if w[:2] in INFIXES and n > 4 and is_vowel(w[2]):
            out.append(w[2:])                               # umalis, inalis
        if w.startswith("ni") and n > 4 and w[2] in "ly":
            out.append(w[2:])                               # niluto

        # partial (CV) reduplication
        if n >= 4 and is_vowel(w[0]) and w[1] == w[0]:
            out.append(w[1:])                               # aalis
        if on and n >= 5 and i < n and is_vowel(w[i]):
            rest = w[i + 1:]
            if rest.startswith(on) and first_vowel(rest) == w[i]:
                out.append(rest)                            # kakain, tatrabaho

        # suffixes
        for s in SUFFIXES:
            if w.endswith(s) and n - len(s) >= 3:
                base = w[:-len(s)]
                out.append(base)
                lowered = lower_final_u(base)
                if lowered != base:
                    out.append(lowered)                     # lutu-in -> luto
                if base.endswith("r"):
                    out.append(base[:-1] + "d")             # bayar-an -> bayad
                if not is_vowel(base[-1]):                  # syncope
                    if s[0] == "h":
                        out += [base + v for v in "aiou"]   # dal-hin -> dala, bil-hin -> bili
                    elif not is_vowel(base[-2]):
                        out += [base[:-1] + v + base[-1] for v in "aiou"]  # bigy-an -> bigay

        # linker -ng / -g and contractions
        if w.endswith("ng") and n >= 5:
            if is_vowel(w[-3]):
                out.append(w[:-2])                          # magandang -> maganda
            out.append(w[:-1])                              # kaibigang -> kaibigan
        if w.endswith(("'y", "'t")) and n >= 4:
            out.append(w[:-2])                              # ako'y -> ako
        return out

    # ------------------------------------------------------------- search
    def derivations(self, word: str) -> dict[str, int]:
        """Candidate stems of `word` -> number of processes undone."""
        cached = self._cache.get(word)
        if cached is not None:
            return cached
        seen = {word: 0}
        frontier = [word]
        for depth in range(1, self.max_depth + 1):
            nxt = []
            for w in frontier:
                for c in self._undo(w):
                    if c not in seen and len(c) >= 2:
                        seen[c] = depth
                        nxt.append(c)
            if not nxt:
                break
            frontier = nxt
        del seen[word]
        self._cache[word] = seen
        return seen

    def valid_stems(self, word: str, is_valid: Validator,
                    exclude: Iterable[str] = frozenset()) -> list[str]:
        """Dictionary-confirmed stems, closest to the root first.

        `exclude` should hold function words: particles such as 'rin' or
        'lang' never take affixes, so 'parin' must not count as pa- + rin."""
        excluded = exclude if isinstance(exclude, (set, frozenset)) else set(exclude)
        derived = self.derivations(word)
        good = [c for c, d in derived.items()
                if len(c) >= self.min_stem_length and has_vowel(c)
                and c not in excluded and is_valid(c)]
        good.sort(key=lambda c: (len(c), derived[c], c))
        return good

    def stem(self, word: str, is_valid: Validator | None = None,
             exclude: Iterable[str] = frozenset()) -> str:
        if is_valid is not None:
            stems = self.valid_stems(word, is_valid, exclude)
            if stems:
                return stems[0]
            if is_valid(word):
                return word
        return self.greedy(word)

    def greedy(self, word: str) -> str:
        """Dictionary-free stemming: prefix, infix, reduplication, suffix."""
        w = word
        m = self.min_stem_length
        if "-" in w:
            a, _, b = w.partition("-")
            if a and (a == b or b.startswith(a)):
                return a
            if b and a.endswith(b):
                return b
            if a and b and is_vowel(b[0]) and not is_vowel(a[-1]) and is_prefix_form(a):
                w = b
            else:
                return w            # irregular hyphen: keep it, its trigrams are rare
        for k in range(min(MAX_PREFIX_LENGTH, len(w) - m), 0, -1):
            if w[:k] in PREFIX_SET and plausible_start(w[k:]):
                w = w[k:]
                break
        on = onset(w)
        i = len(on)
        if on and w[i:i + 2] in INFIXES and len(w) - 2 >= m and is_vowel(w[i + 2:i + 3] or "x"):
            w = on + w[i + 2:]
        elif w[:2] in INFIXES and len(w) - 2 >= m and is_vowel(w[2:3] or "x"):
            w = w[2:]
        on = onset(w)
        i = len(on)
        if len(w) > m and is_vowel(w[0]) and w[1:2] == w[0]:
            w = w[1:]
        elif on and len(w) - i - 1 >= m and is_vowel(w[i:i + 1] or "x"):
            rest = w[i + 1:]
            if rest.startswith(on) and first_vowel(rest) == w[i]:
                w = rest
        for s in SUFFIXES:
            if w.endswith(s) and len(w) - len(s) >= m:
                w = w[:-len(s)]
                break
        return w
