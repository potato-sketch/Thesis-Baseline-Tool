"""Paths and tunable parameters of the spell checker.

Everything the paper calls a "predefined" value lives here so experiments
(e.g. the n-gram threshold sweep in Section II-B) only need one edit.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"
RESULTS_DIR = PROJECT_ROOT / "results"

# --- Language resources -----------------------------------------------------
# Word lists: whitespace-separated words, '#' starts a comment.
TAGALOG_WORDLIST = DATA_DIR / "tagalog_words.txt"
TAGALOG_FUNCTION_WORDS = DATA_DIR / "tagalog_function_words.txt"
TAGALOG_PARADIGMS = DATA_DIR / "tagalog_paradigms.tsv"
TAGALOG_INFLECTIONS = DATA_DIR / "tagalog_inflections.txt"  # generated from TAGALOG_PARADIGMS
ENGLISH_WORDLIST = DATA_DIR / "english_words.txt"

# Drop any extra *.txt word list into these folders and run `train`.
EXTRA_TAGALOG_DIR = DATA_DIR / "extra" / "tagalog"
EXTRA_ENGLISH_DIR = DATA_DIR / "extra" / "english"

# Universal Dependencies treebanks: every data/ud/*.conllu is converted into
# the two lists below (see spellchecker/ud.py).
UD_DIR = DATA_DIR / "ud"
UD_WORDS = UD_DIR / "tagalog_ud_words.txt"                    # generated
UD_FUNCTION_WORDS = UD_DIR / "tagalog_ud_function_words.txt"  # generated
UD_INCLUDE_PROPER_NOUNS = True

# Which Tagalog word list the modeling module uses:
#   "seed" -- the hand-written lists in data/ (+ generated inflections)
#   "ud"   -- only the UD treebank(s) in data/ud/
#   "both" -- the union of the two
# The English list (code-switching) and data/extra/ are used in every mode.
LEXICONS = ("seed", "ud", "both")
LEXICON = "both"

TEST_SET = DATA_DIR / "test_sentences.tsv"
CLEAN_SET = DATA_DIR / "clean_sentences.txt"   # held-out error-free sentences


def model_path(lexicon: str) -> Path:
    return MODEL_DIR / f"model-{lexicon}.json"

# --- Modeling module ----------------------------------------------------------
NGRAM_SIZE = 3          # character trigrams
NGRAM_PAD = "_"         # word-boundary marker ('_be' in Table II of the paper)
MIN_STEM_LENGTH = 3     # shortest string the stemmer may return as a root
MIN_ENGLISH_STEM_LENGTH = 4   # English roots under Tagalog affixes (magtext -> text)

# --- Error detection module ---------------------------------------------------
# Fraction of the most frequent trigrams treated as "the language".
# 0.10 means "top 10% of the language model" (the paper's example).
# 0.20 gave the best F-measure in `python -m spellchecker tune` (test set +
# held-out clean sentences); re-run the sweep after changing the word lists.
NGRAM_THRESHOLD = 0.20

# Extensions that are NOT in the paper.  Turn them off with --paper-only
# (or the GUI checkbox) to run the paper's pipeline exactly as Section II
# describes it:
#   * detection: a prefix written as a separate word ("pag bigay") and a
#     function word fused with its neighbour ("parin") are flagged -- needed
#     to reach the space-insertion and space-deletion errors of Table I;
#   * detection: contractions ("ako'y") are accepted when the bare word is
#     known; English roots under Tagalog affixes need MIN_ENGLISH_STEM_LENGTH
#     letters; the code-switching check accepts a prefix + reduplicated
#     syllable (nagte-text); the compound check rejects function words;
#   * correction: the dash test (magka-ugnay -> magkaugnay, nagaral ->
#     nag-aral); edit-distance candidates are listed after the space-dash
#     suggestions instead of only when space-dash finds nothing; the split
#     test uses the Tagalog list only (the paper: "a dictionary look-up").
# Choices the paper leaves open (stemmer rules, metaphone rules, trigram
# padding and counting, the threshold, tokenisation) are the same in both modes.
USE_EXTENSIONS = True

# --- Error correction module --------------------------------------------------
MAX_EDIT_DISTANCE = 2   # Levenshtein automaton with "at most two edit distance"
MIN_SPLIT_LENGTH = 2    # split test keeps at least two letters per part
MAX_SUGGESTIONS = 8
