"""Evaluation with the metrics of Van Zaanen & Van Huyssteen (2003), as in
Section III of the paper.

Test set: one sentence per line, each with exactly one typographical error
(TSV columns: sentence, erroneous text, intended correction, error type).

* true positive  -- a flag overlapping the erroneous text
* false negative -- the erroneous text is not flagged
* false positive -- any other flag (a correct word marked wrong)
* recall = TP / (TP + FN)        precision = TP / (TP + FP)
* F-measure = 2PR / (P + R)
* suggestion adequacy = share of true positives whose suggestion list
  contains the intended correction

Optionally, held-out error-free sentences (data/clean_sentences.txt) are
checked too: every flag there is an extra false positive.  Their words are
not in the lexicon, so they measure what out-of-vocabulary text does to
precision -- the main source of the paper's false positives.
"""
from __future__ import annotations

import re
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path

from .checker import Flag, SpellChecker
from .tokenizer import tokenize

ERROR_TYPES = ["insertion", "deletion", "substitution", "space deletion",
               "hyphen insertion", "space insertion"]


@dataclass
class TestItem:
    sentence: str
    error: str
    correction: str
    error_type: str
    line: int = 0


@dataclass
class ItemResult:
    item: TestItem
    detected: bool
    adequate: bool = False
    top1: bool = False
    hit: Flag | None = None
    false_positives: list[Flag] = field(default_factory=list)
    accepted_by: str = ""      # for false negatives: the step that accepted the error


def load_test_set(path: Path) -> list[TestItem]:
    items = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cols = [c.strip() for c in line.split("\t")]
        if len(cols) < 4:
            raise ValueError(f"{path.name}:{lineno}: expected 4 tab-separated columns")
        if cols[0].lower() == "sentence":
            continue
        items.append(TestItem(cols[0], cols[1], cols[2], cols[3].lower(), lineno))
    return items


def load_clean_set(path: Path | None) -> list[str]:
    if path is None or not Path(path).exists():
        return []
    return [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")]


def _locate(sentence: str, error: str) -> tuple[int, int]:
    pattern = r"(?<![\w'’-])" + re.escape(error) + r"(?![\w'’-])"
    m = re.search(pattern, sentence) or re.search(pattern, sentence, re.I)
    if not m:
        raise ValueError(f"error text {error!r} not found in {sentence!r}")
    return m.start(), m.end()


def _same(a: str, b: str) -> bool:
    return a.lower().replace("’", "'") == b.lower().replace("’", "'")


def _ratio(a: float, b: float) -> float:
    return a / b if b else 0.0


def _f(p: float, r: float) -> float:
    return 2 * p * r / (p + r) if p + r else 0.0


class Evaluation:
    def __init__(self, results: list[ItemResult], threshold: float, extensions: bool,
                 clean_flags: list[tuple[int, Flag]] | None = None,
                 clean_sentences: int = 0, clean_words: int = 0) -> None:
        self.results = results
        self.threshold = threshold
        self.extensions = extensions
        self.clean_flags = clean_flags or []
        self.clean_sentences = clean_sentences
        self.clean_words = clean_words

    # -- the paper's four metrics on the error sentences -------------------
    tp = property(lambda self: sum(r.detected for r in self.results))
    fn = property(lambda self: sum(not r.detected for r in self.results))
    fp = property(lambda self: sum(len(r.false_positives) for r in self.results))
    adequate = property(lambda self: sum(r.adequate for r in self.results))
    top1_hits = property(lambda self: sum(r.top1 for r in self.results))
    recall = property(lambda self: _ratio(self.tp, self.tp + self.fn))
    precision = property(lambda self: _ratio(self.tp, self.tp + self.fp))
    f_measure = property(lambda self: _f(self.precision, self.recall))
    adequacy = property(lambda self: _ratio(self.adequate, self.tp))
    top1 = property(lambda self: _ratio(self.top1_hits, self.tp))

    # -- including the held-out clean sentences ----------------------------
    clean_fp = property(lambda self: len(self.clean_flags))
    precision_all = property(lambda self: _ratio(self.tp, self.tp + self.fp + self.clean_fp))
    f_measure_all = property(lambda self: _f(self.precision_all, self.recall))

    def by_type(self) -> "OrderedDict[str, dict]":
        table: OrderedDict[str, dict] = OrderedDict(
            (t, {"count": 0, "detected": 0, "adequate": 0}) for t in ERROR_TYPES)
        for r in self.results:
            row = table.setdefault(r.item.error_type, {"count": 0, "detected": 0, "adequate": 0})
            row["count"] += 1
            row["detected"] += r.detected
            row["adequate"] += r.adequate
        return table


def evaluate(checker: SpellChecker, items: list[TestItem],
             clean: list[str] | None = None) -> Evaluation:
    results = []
    for item in items:
        start, end = _locate(item.sentence, item.error)
        flags = checker.check(item.sentence)
        hits = [f for f in flags if f.start < end and f.end > start]
        res = ItemResult(item, bool(hits), hit=hits[0] if hits else None,
                         false_positives=[f for f in flags if f not in hits])
        if hits:
            suggestions = [s.text for f in hits for s in f.suggestions]
            res.adequate = any(_same(s, item.correction) for s in suggestions)
            res.top1 = bool(suggestions) and _same(suggestions[0], item.correction)
        else:
            det = checker.detect(item.error.split()[0])
            res.accepted_by = f"{det.method} ({det.detail})" if det.detail else det.method
        results.append(res)

    clean = clean or []
    clean_flags = [(i, f) for i, s in enumerate(clean, 1) for f in checker.check(s)]
    clean_words = sum(t.kind == "word" for s in clean for t in tokenize(s))
    return Evaluation(results, checker.threshold, checker.detector.use_extensions,
                      clean_flags, len(clean), clean_words)


# ------------------------------------------------------------------ reports
def summary_line(ev: Evaluation) -> str:
    line = (f"recall {ev.recall:6.2%}  precision {ev.precision:6.2%}  "
            f"F-measure {ev.f_measure:6.2%}  suggestion adequacy {ev.adequacy:6.2%}")
    if ev.clean_sentences:
        line += (f"\nwith {ev.clean_sentences} held-out clean sentences: "
                 f"{ev.clean_fp} false alarm(s) in {ev.clean_words} words -> "
                 f"precision {ev.precision_all:6.2%}  F-measure {ev.f_measure_all:6.2%}")
    return line


def format_report(ev: Evaluation, title: str = "Evaluation") -> str:
    mode = "with extensions" if ev.extensions else "paper-only pipeline"
    n = len(ev.results)
    lines = [f"# {title}", "",
             f"{n} test sentences, n-gram threshold {ev.threshold:.2f}, {mode}.", ""]
    if ev.clean_sentences:
        lines += ["| Metric | Test sentences | + held-out clean sentences | Paper |",
                  "|---|---|---|---|",
                  f"| Recall | {ev.recall:.2%} | {ev.recall:.2%} | 81% |",
                  f"| Precision | {ev.precision:.2%} | {ev.precision_all:.2%} | 53.64% |",
                  f"| F-measure | {ev.f_measure:.2%} | {ev.f_measure_all:.2%} | 64.53% |",
                  f"| Suggestion adequacy | {ev.adequacy:.2%} | {ev.adequacy:.2%} | 87.78% |",
                  f"| Correct word ranked first | {ev.top1:.2%} | {ev.top1:.2%} | not reported |",
                  "",
                  f"TP = {ev.tp}, FN = {ev.fn}, FP = {ev.fp} in the test sentences, "
                  f"plus {ev.clean_fp} false alarm(s) in {ev.clean_sentences} clean sentences "
                  f"({ev.clean_words} words)."]
    else:
        lines += ["| Metric | This replication | Paper |", "|---|---|---|",
                  f"| Recall | {ev.recall:.2%} | 81% |",
                  f"| Precision | {ev.precision:.2%} | 53.64% |",
                  f"| F-measure | {ev.f_measure:.2%} | 64.53% |",
                  f"| Suggestion adequacy | {ev.adequacy:.2%} | 87.78% |",
                  f"| Correct word ranked first | {ev.top1:.2%} | not reported |",
                  "", f"TP = {ev.tp}, FN = {ev.fn}, FP = {ev.fp}"]
    lines += ["", "## Results per error type (Table I categories)", "",
              "| Error type | Count | Detected | Correct word suggested |",
              "|---|---|---|---|"]
    for etype, row in ev.by_type().items():
        if row["count"]:
            lines.append(f"| {etype} | {row['count']} | {row['detected']} | {row['adequate']} |")
    lines += ["", "## False negatives (errors that were not flagged)", "",
              "| Incorrect | Correct | Accepted by |", "|---|---|---|"]
    lines += [f"| {r.item.error} | {r.item.correction} | {r.accepted_by} |"
              for r in ev.results if not r.detected]
    lines += ["", "## False positives in the test sentences", "",
              "| Word | Reason | Line |", "|---|---|---|"]
    lines += [f"| {f.word} | {f.method}: {f.detail} | {r.item.line} |"
              for r in ev.results for f in r.false_positives]
    if ev.clean_sentences:
        lines += ["", "## False alarms in the held-out clean sentences", "",
                  "| Word | Reason | Sentence |", "|---|---|---|"]
        lines += [f"| {f.word} | {f.method}: {f.detail} | {i} |" for i, f in ev.clean_flags]
    lines += ["", "## Detected, but the intended correction was not suggested", "",
              "| Incorrect | Intended | Suggestions |", "|---|---|---|"]
    for r in ev.results:
        if r.detected and not r.adequate:
            sugg = ", ".join(s.text for s in r.hit.suggestions) or "(none)"
            lines.append(f"| {r.item.error} | {r.item.correction} | {sugg} |")
    return "\n".join(lines) + "\n"


def tune(model, items: list[TestItem], thresholds: list[float],
         use_extensions: bool = True, clean: list[str] | None = None) -> list[Evaluation]:
    return [evaluate(SpellChecker(model, threshold=t, use_extensions=use_extensions), items, clean)
            for t in thresholds]
