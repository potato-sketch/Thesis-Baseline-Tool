"""Deterministic acyclic finite-state automaton (DAFSA) for a word list.

Modeling module, function 1: "represent the English and Tagalog word lists
into two distinct deterministic acyclic finite state automaton ... allows
fast-checking whether an input word exists ... and saves a lot of memory."

Built with the incremental algorithm for sorted input of Daciuk, Mihov,
Watson & Watson (2000): equivalent suffix states are merged while words are
added, so the result is the minimal automaton for the list (shared prefixes
like a trie *and* shared suffixes such as -ahan, -in, -an).
"""
from __future__ import annotations

import itertools
from typing import Iterable, Iterator


class _BuildNode:
    __slots__ = ("id", "final", "edges")

    def __init__(self, uid: int) -> None:
        self.id = uid
        self.final = False
        self.edges: dict[str, _BuildNode] = {}

    def signature(self) -> tuple:
        # Children are already minimised, so their ids identify them.
        return self.final, tuple(sorted((ch, child.id) for ch, child in self.edges.items()))


class DAFSA:
    """Compact, immutable automaton: state 0 is the start state."""

    def __init__(self, final: list[bool], edges: list[dict[str, int]], word_count: int) -> None:
        self.final = final
        self.edges = edges
        self.word_count = word_count

    # -- construction ------------------------------------------------------
    @classmethod
    def build(cls, words: Iterable[str]) -> "DAFSA":
        ordered = sorted({w for w in words if w})
        ids = itertools.count()
        root = _BuildNode(next(ids))
        register: dict[tuple, _BuildNode] = {}
        unchecked: list[tuple[_BuildNode, str, _BuildNode]] = []

        def minimise(down_to: int) -> None:
            while len(unchecked) > down_to:
                parent, ch, child = unchecked.pop()
                sig = child.signature()
                twin = register.get(sig)
                if twin is not None:
                    parent.edges[ch] = twin
                else:
                    register[sig] = child

        previous = ""
        for word in ordered:
            common = 0
            for a, b in zip(word, previous):
                if a != b:
                    break
                common += 1
            minimise(common)
            node = unchecked[-1][2] if unchecked else root
            for ch in word[common:]:
                child = _BuildNode(next(ids))
                node.edges[ch] = child
                unchecked.append((node, ch, child))
                node = child
            node.final = True
            previous = word
        minimise(0)

        # Renumber states breadth-first into flat arrays.
        index = {root.id: 0}
        order = [root]
        i = 0
        while i < len(order):
            node = order[i]
            i += 1
            for ch in sorted(node.edges):
                child = node.edges[ch]
                if child.id not in index:
                    index[child.id] = len(order)
                    order.append(child)
        final = [n.final for n in order]
        edges = [{ch: index[c.id] for ch, c in sorted(n.edges.items())} for n in order]
        return cls(final, edges, len(ordered))

    # -- queries -----------------------------------------------------------
    def __contains__(self, word: object) -> bool:
        if not isinstance(word, str):
            return False
        state = 0
        edges = self.edges
        for ch in word:
            state = edges[state].get(ch)
            if state is None:
                return False
        return self.final[state]

    def __len__(self) -> int:
        return self.word_count

    def __iter__(self) -> Iterator[str]:
        stack = [(0, "")]
        while stack:
            state, prefix = stack.pop()
            if self.final[state]:
                yield prefix
            for ch in sorted(self.edges[state], reverse=True):
                stack.append((self.edges[state][ch], prefix + ch))

    @property
    def num_states(self) -> int:
        return len(self.final)

    @property
    def num_transitions(self) -> int:
        return sum(len(e) for e in self.edges)

    # -- (de)serialisation -------------------------------------------------
    def to_dict(self) -> dict:
        return {"words": self.word_count, "final": [i for i, f in enumerate(self.final) if f],
                "edges": self.edges}

    @classmethod
    def from_dict(cls, data: dict) -> "DAFSA":
        edges = [dict(e) for e in data["edges"]]
        final = [False] * len(edges)
        for i in data["final"]:
            final[i] = True
        return cls(final, edges, data["words"])
