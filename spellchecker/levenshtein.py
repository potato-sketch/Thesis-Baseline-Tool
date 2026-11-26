"""Levenshtein automaton and its parallel traversal with a DAFSA.

Error correction module: "a Levenshtein automaton from a misspelled word is
generated with at most two edit distance. Then, a Levenshtein automaton and
the Tagalog word list, represented in automaton, is parallel traversed. A word
can be considered as a candidate suggestion if the path of the word ends in
final state upon traversing the two automata."  (Schulz & Mihov, 2002)

A state of the Levenshtein automaton is the sparse column of the edit-distance
matrix restricted to cells <= n.  Transitions are computed on demand and
memoised, so the automaton is built lazily as a DFA, only for the parts the
traversal actually visits.
"""
from __future__ import annotations

from .dafsa import DAFSA

State = tuple[tuple[int, ...], tuple[int, ...]]


class LevenshteinAutomaton:
    def __init__(self, word: str, max_edits: int) -> None:
        self.word = word
        self.max_edits = max_edits
        self._delta: dict[tuple[State, str], State] = {}

    def start(self) -> State:
        k = min(len(self.word), self.max_edits)
        return tuple(range(k + 1)), tuple(range(k + 1))

    def step(self, state: State, ch: str) -> State:
        key = (state, ch)
        cached = self._delta.get(key)
        if cached is not None:
            return cached
        indices, values = state
        word, n = self.word, self.max_edits
        new_i: list[int] = []
        new_v: list[int] = []
        if indices and indices[0] == 0 and values[0] < n:
            new_i.append(0)
            new_v.append(values[0] + 1)
        for j, i in enumerate(indices):
            if i == len(word):
                break
            val = values[j] + (0 if word[i] == ch else 1)            # substitution / match
            if new_i and new_i[-1] == i:
                val = min(val, new_v[-1] + 1)                          # insertion
            if j + 1 < len(indices) and indices[j + 1] == i + 1:
                val = min(val, values[j + 1] + 1)                      # deletion
            if val <= n:
                new_i.append(i + 1)
                new_v.append(val)
        result = (tuple(new_i), tuple(new_v))
        self._delta[key] = result
        return result

    def is_match(self, state: State) -> bool:
        return bool(state[0]) and state[0][-1] == len(self.word)

    def can_match(self, state: State) -> bool:
        return bool(state[0])

    def distance(self, state: State) -> int | None:
        return state[1][-1] if self.is_match(state) else None


def fuzzy_search(dafsa: DAFSA, word: str, max_edits: int) -> dict[str, int]:
    """All words of `dafsa` within `max_edits` of `word`, mapped to their distance."""
    lev = LevenshteinAutomaton(word, max_edits)
    found: dict[str, int] = {}
    stack = [(0, "", lev.start())]
    while stack:
        state, prefix, lstate = stack.pop()
        if dafsa.final[state] and lev.is_match(lstate):
            found[prefix] = lev.distance(lstate)
        for ch, nxt in dafsa.edges[state].items():
            ls = lev.step(lstate, ch)
            if lev.can_match(ls):
                stack.append((nxt, prefix + ch, ls))
    return found


def edit_distance(a: str, b: str) -> int:
    """Plain dynamic-programming Levenshtein distance (used for tie-breaking)."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]
