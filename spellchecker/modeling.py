"""Modeling module: prepares every resource the other two modules need.

1. Tagalog and English word lists -> two minimal DAFSAs.
2. Tagalog word list -> stemmed character-trigram profile.
3. Retraining: the model is rebuilt whenever a word list is newer than the
   saved model ("considering the highly dynamic nature of Filipino, the
   module is capable to retrain the resources").
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path

from . import config
from .dafsa import DAFSA
from .morphology import generate_inflections
from .ngram import NGramProfile
from .stemmer import Stemmer
from .tokenizer import normalize

MODEL_VERSION = 1


@dataclass
class LanguageModel:
    tagalog: DAFSA
    english: DAFSA
    function_words: frozenset[str]
    ngrams: NGramProfile
    info: dict = field(default_factory=dict)

    def is_tagalog(self, word: str) -> bool:
        return word in self.tagalog

    def is_english(self, word: str) -> bool:
        return word in self.english

    def in_dictionary(self, word: str) -> bool:
        return word in self.tagalog or word in self.english


# ---------------------------------------------------------------- word lists
def read_wordlist(path: Path) -> list[str]:
    """Whitespace-separated words; '#' starts a comment; tokens without a
    letter (e.g. frequency columns) are ignored."""
    words = []
    for line in path.read_text(encoding="utf-8").splitlines():
        for token in line.split("#", 1)[0].split():
            token = normalize(token)
            if any(ch.isalpha() for ch in token):
                words.append(token)
    return words


def ensure_inflections(force: bool = False) -> Path:
    """(Re)generate tagalog_inflections.txt from tagalog_paradigms.tsv."""
    src, dst = config.TAGALOG_PARADIGMS, config.TAGALOG_INFLECTIONS
    if src.exists() and (force or not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime):
        forms = generate_inflections(src)
        header = ("# GENERATED from tagalog_paradigms.tsv by `python -m spellchecker inflect`.\n"
                  "# Do not edit by hand: edit the .tsv file and retrain instead.\n")
        dst.write_text(header + "\n".join(forms) + "\n", encoding="utf-8")
    return dst


def _extra(folder: Path) -> list[Path]:
    return sorted(folder.glob("*.txt")) if folder.exists() else []


def _check_lexicon(lexicon: str | None) -> str:
    lexicon = lexicon or config.LEXICON
    if lexicon not in config.LEXICONS:
        raise ValueError(f"lexicon must be one of {config.LEXICONS}, not {lexicon!r}")
    return lexicon


def _uses_seed(lexicon: str) -> bool:
    return lexicon in ("seed", "both")


def _uses_ud(lexicon: str) -> bool:
    return lexicon in ("ud", "both")


def tagalog_sources(lexicon: str) -> list[Path]:
    paths = []
    if _uses_seed(lexicon):
        paths += [config.TAGALOG_WORDLIST, config.TAGALOG_INFLECTIONS]
    if _uses_ud(lexicon):
        paths.append(config.UD_WORDS)
    return [*paths, *_extra(config.EXTRA_TAGALOG_DIR)]


def function_word_sources(lexicon: str) -> list[Path]:
    paths = []
    if _uses_seed(lexicon):
        paths.append(config.TAGALOG_FUNCTION_WORDS)
    if _uses_ud(lexicon):
        paths.append(config.UD_FUNCTION_WORDS)
    return paths


def english_sources() -> list[Path]:
    return [config.ENGLISH_WORDLIST, *_extra(config.EXTRA_ENGLISH_DIR)]


def all_sources(lexicon: str) -> list[Path]:
    """Every file the model of this lexicon is built from (for retraining)."""
    from .ud import treebank_files
    generators = []
    if _uses_seed(lexicon):
        generators.append(config.TAGALOG_PARADIGMS)
    if _uses_ud(lexicon):
        generators += treebank_files()
    return [*tagalog_sources(lexicon), *function_word_sources(lexicon), *english_sources(),
            *generators]


# ------------------------------------------------------------------ training
def train(lexicon: str | None = None, verbose: bool = False) -> LanguageModel:
    lexicon = _check_lexicon(lexicon)
    t0 = time.perf_counter()
    if _uses_seed(lexicon):
        ensure_inflections()
    if _uses_ud(lexicon):
        from .ud import ensure_ud_lists
        ensure_ud_lists()

    function_words: set[str] = set()
    for path in function_word_sources(lexicon):
        function_words.update(read_wordlist(path))
    content: set[str] = set()
    for path in tagalog_sources(lexicon):
        if path.exists():
            content.update(read_wordlist(path))
    tagalog = content | function_words
    # A homograph that is also a content word is not a *pure* function word:
    # UD tags 'bago' "before" as SCONJ, but 'bago' "new" takes affixes and the
    # linker (bagong, baguhin), so it must stay usable as a stem.
    function_words -= content
    english: set[str] = set()
    for path in english_sources():
        if path.exists():
            english.update(read_wordlist(path))
    if verbose:
        print(f"  word lists ({lexicon}): {len(tagalog):,} Tagalog, {len(english):,} English, "
              f"{len(function_words):,} function words")

    tl_automaton = DAFSA.build(tagalog)
    en_automaton = DAFSA.build(english)
    if verbose:
        print(f"  Tagalog DAFSA: {tl_automaton.num_states:,} states, "
              f"{tl_automaton.num_transitions:,} transitions")
        print(f"  English DAFSA: {en_automaton.num_states:,} states, "
              f"{en_automaton.num_transitions:,} transitions")

    # Stemmed n-gram profile of the Tagalog word list.
    stemmer = Stemmer(config.MIN_STEM_LENGTH)
    stems = {stemmer.stem(w, tagalog.__contains__, function_words) for w in tagalog}
    profile = NGramProfile(config.NGRAM_SIZE, config.NGRAM_PAD).train(stems)
    if verbose:
        print(f"  stemmed trigram profile: {len(stems):,} stems, {len(profile.counts):,} trigram types")

    info = {
        "version": MODEL_VERSION,
        "lexicon": lexicon,
        "trained_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "seconds": round(time.perf_counter() - t0, 2),
        "tagalog_words": len(tagalog),
        "english_words": len(english),
        "function_words": len(function_words),
        "stems": len(stems),
        "trigram_types": len(profile.counts),
        "tagalog_states": tl_automaton.num_states,
        "english_states": en_automaton.num_states,
        "sources": [str(p.relative_to(config.PROJECT_ROOT)) for p in all_sources(lexicon)
                    if p.exists()],
    }
    return LanguageModel(tl_automaton, en_automaton, frozenset(function_words), profile, info)


# ----------------------------------------------------------- persistence
def save(model: LanguageModel, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "info": model.info,
        "function_words": sorted(model.function_words),
        "tagalog": model.tagalog.to_dict(),
        "english": model.english.to_dict(),
        "ngrams": model.ngrams.to_dict(),
    }
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return path


def load(path: Path) -> LanguageModel:
    data = json.loads(path.read_text(encoding="utf-8"))
    return LanguageModel(
        tagalog=DAFSA.from_dict(data["tagalog"]),
        english=DAFSA.from_dict(data["english"]),
        function_words=frozenset(data["function_words"]),
        ngrams=NGramProfile.from_dict(data["ngrams"]),
        info=data.get("info", {}),
    )


_MODEL_CODE = [Path(__file__).with_name(n) for n in
               ("modeling.py", "morphology.py", "stemmer.py", "ngram.py", "dafsa.py",
                "config.py", "ud.py")]


def is_stale(lexicon: str | None = None) -> bool:
    """True if a word list, or code that shapes the model, changed since training."""
    lexicon = _check_lexicon(lexicon)
    path = config.model_path(lexicon)
    if not path.exists():
        return True
    built = path.stat().st_mtime
    return any(p.exists() and p.stat().st_mtime > built
               for p in [*all_sources(lexicon), *_MODEL_CODE])


def load_or_train(lexicon: str | None = None, force: bool = False,
                  verbose: bool = False) -> LanguageModel:
    """Load the saved model of a lexicon ("seed", "ud" or "both"; default
    config.LEXICON), retraining first if one of its resources changed."""
    lexicon = _check_lexicon(lexicon)
    path = config.model_path(lexicon)
    if not force and not is_stale(lexicon):
        try:
            model = load(path)
            if model.info.get("version") == MODEL_VERSION:
                return model
        except (OSError, ValueError, KeyError):
            pass
    if verbose:
        print(f"Training the language model ({lexicon} word list) ...")
    model = train(lexicon, verbose=verbose)
    save(model, path)
    if verbose:
        print(f"  saved to {path} in {model.info['seconds']} s")
    return model
