"""A metaphone variant for Filipino and the Dice coefficient used for ranking.

"A customized metaphone phonetic algorithm for the Filipino language is
created and used for encoding the misspelled word and its suggestions. The
idea of the encoding is to make words with similar sound (e.g. aksion,
aksiyon, and aksyon 'action') have similar code representation ... After
encoding, the dice coefficient score is computed between the encoded
misspelled word and each suggestion."

Differences from Philips' (1990) English metaphone, motivated by Filipino:
* vowels are phonemic, so they are kept, but merged into the classes that
  Filipino spelling confuses: e~i -> I, o~u -> U, a -> A;
* glide spellings are unified (siya/sya, kuwento/kwento, aksion/aksyon);
* Spanish/English loan spellings map to Abakada sounds (f->P, v->B, z->S,
  c->K/S, qu->K, ch/ts->C, sh/sy->X, dy/j->J, ll->LY, ñ->NY);
* 'ng' is its own sound (Q) and 'mga' is read 'manga'.

The paper's implementation had 56 rules; this one has len(RULES).
"""
from __future__ import annotations

import re
from typing import Callable

_C = "bcdfghjklmnpqrstvwxyzñ"   # consonant letters

_RAW_RULES: list[tuple[str, str, str | Callable]] = [
    # --- normalisation
    ("drop hyphens, apostrophes and digits", r"[^a-zñ]", ""),
    ("'mga' is pronounced 'manga'", r"^mga$", "manga"),
    # --- glide spellings and diphthongs
    ("C+iy+V -> Cy (siya/sya, diyan/dyan, aksiyon/aksyon)", rf"(?<=[{_C}])iy(?=[aeiou])", "y"),
    ("C+uw+V -> Cw (kuwento/kwento, buwan/bwan)", rf"(?<=[{_C}])uw(?=[aeiou])", "w"),
    ("C+i+V -> Cy (aksion/aksyon, piano/pyano)", rf"(?<=[{_C}])i(?=[aou])", "y"),
    ("C+u+V -> Cw (kuarto/kwarto)", rf"(?<=[{_C}])u(?=[aei])", "w"),
    ("ay before a consonant is said e (mayroon/meron, kaysa/kesa)", rf"ay(?=[{_C}])", "e"),
    ("final ao -> aw (arao/araw)", r"ao$", "aw"),
    ("final ai -> ay (bahai/bahay)", r"ai$", "ay"),
    # --- loan-word spellings
    ("ch -> C (chismis/tsismis)", r"ch", "C"),
    ("ts -> C (tsinelas)", r"ts", "C"),
    ("sh -> X (shampoo/syampu)", r"sh", "X"),
    ("sy+V -> X (syampu)", r"sy(?=[aeiou])", "X"),
    ("dy+V -> J (dyip/jeep)", r"dy(?=[aeiou])", "J"),
    ("j -> J", r"j", "J"),
    ("ph -> P (pharmacy/parmasya)", r"ph", "P"),
    ("f -> P (Filipino/Pilipino)", r"f", "P"),
    ("v -> B (vakasyon/bakasyon)", r"v", "B"),
    ("z -> S (zero/sero)", r"z", "S"),
    ("ck -> K", r"ck", "K"),
    ("qu before e/i -> K (queso/keso)", r"qu(?=[ei])", "K"),
    ("q -> K", r"q", "K"),
    ("c before e/i/y -> S (cine/sine)", r"c(?=[eiy])", "S"),
    ("c -> K (carro/karo)", r"c", "K"),
    ("x -> KS (taxi/taksi)", r"x", "KS"),
    ("ñ -> NY (niño/ninyo)", r"ñ", "NY"),
    ("ll -> LY (calle/kalye)", r"ll", "LY"),
    ("gu before e/i -> G (guerra/gera)", r"gu(?=[ei])", "G"),
    ("th -> T (theater/teatro)", r"th", "T"),
    # --- native consonants
    ("ng (velar nasal) -> Q", r"ng", "Q"),
    ("h after a consonant is silent", rf"(?<=[{_C}A-Z])h", ""),
    ("final h is silent", r"h$", ""),
    # --- vowel classes (e~i and o~u alternate in Filipino spelling)
    ("e, i -> I", r"[ei]", "I"),
    ("o, u -> U", r"[ou]", "U"),
    ("a -> A", r"a", "A"),
    # --- remaining letters and clean-up
    ("b d g h k l m n p r s t w y -> upper case", r"[bdghklmnprstwy]", lambda m: m.group(0).upper()),
    ("collapse repeated codes (rr, maaari)", r"(.)\1+", r"\1"),
]

RULES = [(desc, re.compile(pattern), repl) for desc, pattern, repl in _RAW_RULES]


def encode(word: str) -> str:
    """Phonetic code of a word, e.g. encode('aksiyon') == encode('aksion') == 'AKXUN'."""
    code = word.lower().replace("’", "'")
    for _, pattern, repl in RULES:
        code = pattern.sub(repl, code)
    return code


def bigrams(code: str) -> set[str]:
    padded = f"#{code}#"
    return {padded[i:i + 2] for i in range(len(padded) - 1)}


def dice(code_a: str, code_b: str) -> float:
    """Dice coefficient of two codes over their (padded) bigram sets."""
    a, b = bigrams(code_a), bigrams(code_b)
    return 2 * len(a & b) / (len(a) + len(b))


def similarity(word_a: str, word_b: str) -> float:
    return dice(encode(word_a), encode(word_b))
