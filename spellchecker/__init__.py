"""Filipino spell checker -- a replication of

    M. Octaviano Jr and A. Borra, "A Spell Checker for a Low-resourced and
    Morphologically Rich Language", Proc. IEEE TENCON 2017, pp. 1853-1856.

Modules (Fig. 1 of the paper):
    modeling    -- word lists -> DAFSAs + stemmed trigram profile (retrainable)
    detection   -- dictionary / stemming, code-switching & compound, n-gram look-up
    correction  -- space-dash correction, Levenshtein automaton, metaphone + Dice ranking
"""
from .checker import Flag, SpellChecker
from .modeling import LanguageModel, load_or_train, train

__all__ = ["SpellChecker", "Flag", "LanguageModel", "load_or_train", "train"]
