"""Stemmed character n-gram profile (Modeling module, function 2).

"This language model is composed of character trigram of the Tagalog word
list ... The module checks each trigram of the stemmed word if it is in the
top trigram based on the predefined threshold of the system.  For example,
each trigram of the word 'mano' will be checked if it exists in the top 10%
language model of the system when threshold value is set to .10."

Frequencies are type frequencies: the number of distinct stems a trigram
occurs in (the resource is a word list, not a corpus).
"""
from __future__ import annotations

import math
from collections import Counter
from typing import Iterable


class NGramProfile:
    def __init__(self, n: int = 3, pad: str = "_", counts: dict[str, int] | None = None) -> None:
        self.n = n
        self.pad = pad
        self.counts: Counter[str] = Counter(counts or {})
        self._ranked: list[str] | None = None
        self._top_cache: dict[float, frozenset[str]] = {}

    def ngrams(self, word: str) -> list[str]:
        padded = f"{self.pad}{word}{self.pad}"
        if len(padded) < self.n:
            return [padded]
        return [padded[i:i + self.n] for i in range(len(padded) - self.n + 1)]

    def train(self, stems: Iterable[str]) -> "NGramProfile":
        self.counts = Counter()
        for stem in set(stems):
            self.counts.update(set(self.ngrams(stem)))
        self._ranked = None
        self._top_cache.clear()
        return self

    def ranked(self) -> list[str]:
        if self._ranked is None:
            self._ranked = [g for g, _ in sorted(self.counts.items(), key=lambda kv: (-kv[1], kv[0]))]
        return self._ranked

    def top(self, threshold: float) -> frozenset[str]:
        """The most frequent `threshold` fraction of trigram types."""
        threshold = min(max(threshold, 0.0), 1.0)
        cached = self._top_cache.get(threshold)
        if cached is None:
            ranked = self.ranked()
            k = max(1, math.ceil(threshold * len(ranked))) if ranked else 0
            cached = frozenset(ranked[:k])
            self._top_cache[threshold] = cached
        return cached

    def missing(self, word: str, threshold: float) -> list[str]:
        """Trigrams of `word` that are not among the top ones (empty = looks valid)."""
        top = self.top(threshold)
        return [g for g in self.ngrams(word) if g not in top]

    def to_dict(self) -> dict:
        return {"n": self.n, "pad": self.pad, "counts": dict(self.counts)}

    @classmethod
    def from_dict(cls, data: dict) -> "NGramProfile":
        return cls(data["n"], data["pad"], data["counts"])
