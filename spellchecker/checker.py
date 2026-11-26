"""SpellChecker: ties tokenisation, detection and correction together."""
from __future__ import annotations

from dataclasses import dataclass, field

from . import config
from .correction import ErrorCorrector, Suggestion
from .detection import Detection, ErrorDetector
from .modeling import LanguageModel, load_or_train
from .stemmer import Stemmer
from .tokenizer import Token, tokenize


@dataclass
class Flag:
    word: str
    start: int
    end: int
    method: str
    detail: str
    suggestions: list[Suggestion] = field(default_factory=list)
    stem: str | None = None


def match_case(original: str, suggestion: str) -> str:
    if len(original) > 1 and original.isupper():
        return suggestion.upper()
    if original[:1].isupper():
        return suggestion[:1].upper() + suggestion[1:]
    return suggestion


class SpellChecker:
    def __init__(self, model: LanguageModel | None = None, threshold: float | None = None,
                 use_extensions: bool | None = None, skip_proper_nouns: bool = False,
                 max_suggestions: int | None = None, max_edits: int | None = None,
                 lexicon: str | None = None) -> None:
        self.model = model or load_or_train(lexicon)
        self.stemmer = Stemmer(config.MIN_STEM_LENGTH)
        self.detector = ErrorDetector(self.model, self.stemmer, threshold, use_extensions)
        self.corrector = ErrorCorrector(self.detector, max_edits, max_suggestions)
        self.skip_proper_nouns = skip_proper_nouns

    @property
    def threshold(self) -> float:
        return self.detector.threshold

    def detect(self, word: str) -> Detection:
        return self.detector.check(word)

    def suggest(self, word: str, next_word: str | None = None) -> list[Suggestion]:
        return self.corrector.suggest(word, next_word)

    def check(self, text: str) -> list[Flag]:
        tokens = tokenize(text)
        positions = [i for i, t in enumerate(tokens) if t.kind == "word"]
        flags: list[Flag] = []
        for n, ti in enumerate(positions):
            tok = tokens[ti]
            if self.skip_proper_nouns and _is_proper_noun(tokens, ti):
                continue
            det = self.detector.check(tok.text)
            if not det.is_error:
                continue
            nxt = None
            if n + 1 < len(positions):
                between = tokens[ti + 1:positions[n + 1]]
                if all(t.kind == "space" for t in between):
                    nxt = tokens[positions[n + 1]]
            suggestions = self.corrector.suggest(tok.text, nxt.text if nxt else None)
            for s in suggestions:
                s.text = match_case(tok.text, s.text)
                s.end = nxt.end if (s.span == 2 and nxt) else tok.end
            flags.append(Flag(tok.text, tok.start, tok.end, det.method, det.detail,
                              suggestions, det.stem))
        return flags


def _is_proper_noun(tokens: list[Token], index: int) -> bool:
    if not tokens[index].text[:1].isupper():
        return False
    for t in reversed(tokens[:index]):
        if t.kind == "space":
            continue
        return t.kind != "punct" or t.text not in ".!?"
    return False          # first word of the text
