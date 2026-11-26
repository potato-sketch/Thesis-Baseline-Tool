"""Build the Tagalog word lists from Universal Dependencies treebanks (CoNLL-U).

Every *.conllu file in data/ud/ is read (e.g. UD_Tagalog-Ugnayan, -TRG,
-NewsCrawl) and turned into two plain word lists that the modeling module
uses like any other:

  data/ud/tagalog_ud_words.txt           written word forms + lemmas
  data/ud/tagalog_ud_function_words.txt  closed-class words

How the CoNLL-U columns are used
  FORM   every written word, lower-cased.  For a multiword token such as
         "akong" (ako + -ng) the written form on the range line is kept and
         the clitic pieces '-ng', "'y", "'t" are dropped.
  LEMMA  added as well (roots such as 'sama' for 'sumama'); '_' and 'null' skipped.
  UPOS   PUNCT/SYM are skipped.  ADP, AUX, CCONJ, DET, PART, PRON, SCONJ are
         function words, and so are enclitic particles tagged ADV (rin, lang, pa).
         PROPN is kept unless include_proper_nouns is False.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from . import config
from .morphology import ENCLITICS
from .tokenizer import normalize

CLOSED_CLASS = frozenset({"ADP", "AUX", "CCONJ", "DET", "PART", "PRON", "SCONJ"})
SKIPPED = frozenset({"PUNCT", "SYM"})


@dataclass
class UDLexicon:
    words: set[str] = field(default_factory=set)
    function_words: set[str] = field(default_factory=set)
    sentences: int = 0
    tokens: int = 0
    files: list[str] = field(default_factory=list)


def _clean(text: str) -> str | None:
    """A lower-cased written word, or None for punctuation, digits and clitic pieces."""
    w = normalize(text.strip())
    if not w or w in ("_", "null") or w[0] in "-'" or not any(ch.isalpha() for ch in w):
        return None
    return w


def _is_function(upos: str, form: str) -> bool:
    return upos in CLOSED_CLASS or (upos == "ADV" and form in ENCLITICS)


def read_treebanks(paths: list[Path], include_proper_nouns: bool = True) -> UDLexicon:
    lex = UDLexicon()
    for path in paths:
        lex.files.append(path.name)
        fused: tuple[int, int, str] | None = None     # (first id, last id, written form)
        fused_function = True
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# sent_id"):
                lex.sentences += 1
            if not line or line.startswith("#"):
                continue
            cols = line.split("\t")
            if len(cols) != 10 or "." in cols[0]:      # skip malformed lines and empty nodes
                continue
            if "-" in cols[0]:                           # multiword token range "6-7"
                first, last = (int(x) for x in cols[0].split("-"))
                fused, fused_function = (first, last, cols[1]), True
                continue
            index, form, lemma, upos = int(cols[0]), cols[1], cols[2], cols[3]
            lex.tokens += 1
            if fused and fused[0] <= index <= fused[1]:
                if index == fused[0]:
                    fused_function = _is_function(upos, (_clean(form) or ""))
                if index == fused[1]:
                    surface = _clean(fused[2])
                    if surface and (include_proper_nouns or upos != "PROPN"):
                        (lex.function_words if fused_function else lex.words).add(surface)
                    fused = None
            if upos in SKIPPED or (upos == "PROPN" and not include_proper_nouns):
                continue
            w = _clean(form)
            if not w:                                    # punctuation, digits, '-ng' pieces
                continue
            function = _is_function(upos, w)
            (lex.function_words if function else lex.words).add(w)
            root = _clean(lemma)
            if root and upos != "PROPN":                 # ninyo -> inyo, sumama -> sama
                (lex.function_words if function else lex.words).add(root)
    return lex


def treebank_files() -> list[Path]:
    return sorted(config.UD_DIR.glob("*.conllu")) if config.UD_DIR.exists() else []


def ensure_ud_lists(force: bool = False) -> tuple[Path, Path]:
    """(Re)generate the two UD word lists when a treebank is newer than them."""
    files = treebank_files()
    words_path, fw_path = config.UD_WORDS, config.UD_FUNCTION_WORDS
    if not files:
        raise FileNotFoundError(
            f"No *.conllu treebank found in {config.UD_DIR}. Download one, e.g. "
            "tl_ugnayan-ud-test.conllu from github.com/UniversalDependencies/UD_Tagalog-Ugnayan")
    newest = max(p.stat().st_mtime for p in files)
    stale = force or not words_path.exists() or not fw_path.exists() or \
        min(words_path.stat().st_mtime, fw_path.stat().st_mtime) < newest
    if stale:
        lex = read_treebanks(files, config.UD_INCLUDE_PROPER_NOUNS)
        header = (f"# GENERATED from {', '.join(lex.files)} ({lex.sentences} sentences, "
                  f"{lex.tokens} syntactic words) by spellchecker/ud.py.\n"
                  "# Do not edit by hand: replace or add .conllu files and retrain instead.\n")
        words_path.write_text(header + "\n".join(sorted(lex.words)) + "\n", encoding="utf-8")
        fw_path.write_text(header + "\n".join(sorted(lex.function_words)) + "\n", encoding="utf-8")
    return words_path, fw_path
