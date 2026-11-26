"""Tagalog morphology shared by the stemmer, the detector, the corrector and
the inflection generator that builds part of the Tagalog word list.

Phenomena covered (Section III of the paper lists the same set):
prefixation, infixation (-um-, -in-), suffixation (-in/-hin, -an/-han),
circumfixation (ka-...-an, pag-...-an), partial reduplication (CV),
full reduplication (araw-araw), partial assimilation (pang-/pan-/pam-),
compound words and the linker -ng.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

VOWELS = frozenset("aeiou")


def is_vowel(ch: str) -> bool:
    return ch in VOWELS


def has_vowel(word: str) -> bool:
    return any(ch in VOWELS for ch in word)


# --------------------------------------------------------------------------
# Affix inventory
# --------------------------------------------------------------------------
PREFIXES: tuple[str, ...] = tuple(sorted({
    # stacked prefixes
    "nakikipag", "makikipag", "pakikipag", "nakipag", "makipag", "pakipag",
    "nagsipag", "magsipag", "nakapag", "makapag", "nagpaka", "magpaka",
    "magkasing", "kasing", "pinaka", "napaka", "pagka", "magka", "nagka",
    "nagpa", "magpa", "pagpa", "ipinag", "ipinang", "ipina", "pinag", "pinang",
    "makiki", "nakiki", "pakiki", "maki", "naki", "paki", "ipag", "ipang",
    "ipa", "pina",
    # nasal prefixes (partial assimilation: pang-/pan-/pam-, mang-/man-/mam-)
    "mang", "man", "mam", "nang", "nan", "nam", "pang", "pan", "pam",
    "sing", "sang",
    # simple prefixes
    "naka", "maka", "paka", "mapa", "napa", "taga", "ika",
    "mag", "nag", "pag", "ka", "ma", "na", "pa", "i",
}, key=lambda p: (-len(p), p)))
PREFIX_SET = frozenset(PREFIXES)
MAX_PREFIX_LENGTH = max(map(len, PREFIXES))

# Partial assimilation: the root's first consonant is replaced by the nasal.
ASSIMILATE_M = frozenset({"mam", "nam", "pam"})                 # mamili  <- pili / bili
ASSIMILATE_N = frozenset({"man", "nan", "pan"})                 # manahi  <- tahi, manakit <- sakit
ASSIMILATE_NG = frozenset({"mang", "nang", "pang", "sing", "sang",
                           "kasing", "magkasing", "ipang", "pinang", "ipinang"})

INFIXES = ("um", "in")
SUFFIXES = ("han", "hin", "nan", "nin", "an", "in")

# Enclitic particles (Schachter & Otanes 1972).  A closed grammatical class:
# never the root of an affixed word, always written as separate words.
ENCLITICS = frozenset({
    "na", "pa", "din", "rin", "daw", "raw", "lang", "lamang", "naman", "nga", "po", "ho",
    "ba", "kaya", "pala", "sana", "yata", "tuloy", "muna", "man", "kasi", "nawa",
})


# --------------------------------------------------------------------------
# Small phonological helpers
# --------------------------------------------------------------------------
def onset(word: str) -> str:
    """Initial consonant of a word, treating the digraph 'ng' as one sound."""
    if word.startswith("ng"):
        return "ng"
    if word and not is_vowel(word[0]):
        return word[0]
    return ""


# Consonant clusters that can begin a syllable (mostly in loanwords).
ONSET_CLUSTERS = frozenset({
    "bl", "br", "by", "bw", "dr", "dy", "dw", "gl", "gr", "gw", "kl", "kr", "ky", "kw",
    "ly", "my", "ny", "pl", "pr", "py", "sy", "sw", "sh", "ch", "tr", "ts", "ty", "tw",
})


def plausible_start(rest: str) -> bool:
    """Can `rest` begin a Tagalog root?  V, CV, ngV or a cluster + V.
    Rejects stems such as 'nsin' (from na-pansin) or 'mpeonato'."""
    if not rest:
        return False
    if is_vowel(rest[0]):
        return True
    if len(rest) > 1 and is_vowel(rest[1]):
        return True
    return len(rest) > 2 and (rest[:2] == "ng" or rest[:2] in ONSET_CLUSTERS) and is_vowel(rest[2])


def first_vowel(word: str) -> str:
    for ch in word:
        if ch in VOWELS:
            return ch
    return ""


def _last_vowel_index(word: str) -> int:
    for i in range(len(word) - 1, -1, -1):
        if word[i] in VOWELS:
            return i
    return -1


def raise_final_o(word: str) -> str:
    """luto -> lutu (lutuin), inom -> inum (inumin), sagot -> sagut (sagutin)."""
    i = _last_vowel_index(word)
    if i >= 0 and word[i] == "o":
        return word[:i] + "u" + word[i + 1:]
    return word


def lower_final_u(word: str) -> str:
    """Inverse of raise_final_o, used when stripping a suffix."""
    i = _last_vowel_index(word)
    if i >= 0 and word[i] == "u":
        return word[:i] + "o" + word[i + 1:]
    return word


def reduplicate(root: str) -> str:
    """Partial (CV) reduplication: kain -> kakain, alis -> aalis,
    trabaho -> tatrabaho, ngiti -> ngingiti."""
    v = first_vowel(root)
    if not v:
        return root
    return onset(root) + v + root


def add_infix(root: str, infix: str) -> str:
    """Insert -um-/-in- after the first consonant (k-um-ain, s-in-ulat).
    Vowel-initial roots take it as a prefix (umalis, inalis); -in- becomes
    ni- before l and y (niluto, niyakap)."""
    on = onset(root)
    if not on:
        return infix + root
    if infix == "in" and on in ("l", "y"):
        return "ni" + root
    return on + infix + root[len(on):]


def add_suffix(root: str, suffix: str, glottal: bool = False) -> str:
    """basa + in -> basahin, luto' + in -> lutuin, inom + in -> inumin."""
    base = raise_final_o(root)
    if is_vowel(base[-1]) and not glottal:
        return base + "h" + suffix
    return base + suffix


def attach_prefix(prefix: str, stem: str) -> str:
    """A consonant-final prefix takes a hyphen before a vowel-initial stem
    (mag-aral, pag-asa) and is written solid otherwise (magluto)."""
    if prefix and stem and not is_vowel(prefix[-1]) and is_vowel(stem[0]):
        return f"{prefix}-{stem}"
    return prefix + stem


def is_prefix_form(token: str, root: str | None = None) -> bool:
    """True for a prefix ('nag') or a prefix plus a reduplicated syllable
    ('nagte' in nagte-text, 'magpo' in magpo-post)."""
    if token in PREFIX_SET:
        return True
    for p in PREFIXES:
        if token.startswith(p) and len(token) > len(p):
            syl = token[len(p):]
            if len(syl) <= 3 and is_vowel(syl[-1]) and sum(map(is_vowel, syl)) == 1:
                if root is None or not onset(syl) or root.startswith(onset(syl)):
                    return True
    return False


def is_prefix_before_root(token: str, root: str) -> bool:
    """Stricter is_prefix_form for a known root: the reduplicated syllable
    must copy the root's first letters ('nagte' + text, 'nagu' + update),
    so 'maa' + gang is not one."""
    if token in PREFIX_SET:
        return True
    for p in PREFIXES:
        syl = token[len(p):]
        if (token.startswith(p) and syl and len(syl) <= 3 and is_vowel(syl[-1])
                and sum(map(is_vowel, syl)) == 1 and root.startswith(syl)):
            return True
    return False


# --------------------------------------------------------------------------
# Inflection generator (used by the modeling module to enlarge the lexicon)
# --------------------------------------------------------------------------
PARADIGM_CLASSES = {
    "um": "actor focus -um-        kumain, kumakain, kakain",
    "mag": "actor focus mag-        magluto, nagluto, nagluluto, magluluto, pagluluto",
    "ma": "ma- verbs               matulog, natulog, natutulog, matutulog",
    "maka": "abilitative maka-       makakain, nakakain, nakakakain",
    "in": "object focus -in        kainin, kinain, kinakain, kakainin",
    "an": "locative focus -an      puntahan, pinuntahan, pinupuntahan, pupuntahan",
    "i": "conveyance focus i-     isama, isinama, isinasama, isasama",
    "pagan": "circumfix pag-...-an    pag-aralan, pinag-aralan, pinag-aaralan",
    "adj": "adjective ma-           maganda, magaganda, napakaganda, pinakamaganda, kagandahan",
}


def inflect(root: str, classes: Iterable[str], suffix_stem: str | None = None) -> set[str]:
    """Generate inflected forms of a root.

    root         -- a trailing apostrophe marks a glottal-final root, which
                    takes -in/-an without the linking h (luto' -> lutuin).
    classes      -- paradigm class names, see PARADIGM_CLASSES.
    suffix_stem  -- irregular stem used before -in/-an (syncope or sound
                    change): dala -> dalh(in), bigay -> bigy(an), bayad -> bayar(an).
    """
    glottal = root.endswith("'")
    root = root.rstrip("'")
    red = reduplicate(root)

    def suffixed(suffix: str, redup: bool = False) -> str:
        if suffix_stem:
            return (reduplicate(suffix_stem) if redup else suffix_stem) + suffix
        return add_suffix(red if redup else root, suffix, glottal)

    forms = {root}
    for cls in classes:
        if cls == "um":
            forms.update({add_infix(root, "um"), add_infix(red, "um"), red})
        elif cls == "mag":
            for p in ("mag", "nag", "pag"):
                forms.update({attach_prefix(p, root), attach_prefix(p, red)})
        elif cls == "ma":
            forms.update({"ma" + root, "na" + root, "na" + red, "ma" + red})
        elif cls == "maka":
            forms.update({"maka" + root, "naka" + root, "naka" + red, "maka" + red})
        elif cls == "in":
            forms.update({suffixed("in"), add_infix(root, "in"),
                          add_infix(red, "in"), suffixed("in", True)})
        elif cls == "an":
            forms.update({suffixed("an"), add_infix(suffixed("an"), "in"),
                          add_infix(suffixed("an", True), "in"), suffixed("an", True)})
        elif cls == "i":
            if is_vowel(root[0]):
                forms.update({"i" + root, "ini" + root, "ini" + red, "i" + red})
            else:
                forms.update({"i" + root, "i" + add_infix(root, "in"),
                              "i" + add_infix(red, "in"), "i" + red})
        elif cls == "pagan":
            forms.update({attach_prefix("pag", suffixed("an")),
                          attach_prefix("pinag", suffixed("an")),
                          attach_prefix("pinag", suffixed("an", True)),
                          attach_prefix("pag", suffixed("an", True))})
        elif cls == "adj":
            forms.update({"ma" + root, "ma" + red, "napaka" + root,
                          "pinakama" + root, "ka" + suffixed("an")})
        else:
            raise ValueError(f"unknown paradigm class {cls!r} for root {root!r}")
    return forms


def load_paradigms(path: Path) -> list[tuple[str, list[str], str | None]]:
    """Read `root  classes  [suffix_stem]` lines (tab or space separated)."""
    entries = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            raise ValueError(f"{path.name}:{lineno}: expected 'root classes [suffix_stem]'")
        root, classes = parts[0].lower(), [c.strip() for c in parts[1].split(",") if c.strip()]
        suffix_stem = parts[2].lower() if len(parts) > 2 else None
        entries.append((root, classes, suffix_stem))
    return entries


def generate_inflections(path: Path) -> list[str]:
    forms: set[str] = set()
    for root, classes, suffix_stem in load_paradigms(path):
        forms |= inflect(root, classes, suffix_stem)
    return sorted(forms)
