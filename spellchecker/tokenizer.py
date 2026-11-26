"""Tokenisation: "The system first tokenized the sentence into words,
separating words from punctuation marks (e.g. Ang bahay ko. -> Ang <space>
bahay <space> ko <space> .)".

Hyphens and apostrophes inside a word are kept (araw-araw, nag-text,
pagka't); a trailing hyphen is kept too so that "mag- kasama" yields the
token "mag-".  Character offsets are kept for highlighting in the GUI.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_L = "A-Za-zÀ-ÖØ-öø-ÿ"
_TOKEN = re.compile(
    rf"(?P<word>[{_L}]+(?:['’\-][{_L}]+)*-?)"
    r"|(?P<number>\d+(?:[.,:]\d+)*)"
    r"|(?P<space>\s+)"
    r"|(?P<punct>.)",
    re.S,
)


@dataclass(frozen=True)
class Token:
    text: str
    kind: str      # word | number | space | punct
    start: int
    end: int


def tokenize(text: str) -> list[Token]:
    return [Token(m.group(), m.lastgroup, m.start(), m.end()) for m in _TOKEN.finditer(text)]


def normalize(word: str) -> str:
    """Lower-case and unify apostrophes; this is the form looked up in the automata."""
    return word.lower().replace("’", "'").replace("‘", "'")
