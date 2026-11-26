"""Unit tests for the building blocks (no trained model needed)."""
import random
import string
import unittest

from spellchecker.dafsa import DAFSA
from spellchecker.levenshtein import edit_distance, fuzzy_search
from spellchecker.metaphone import dice, encode
from spellchecker.morphology import inflect, reduplicate
from spellchecker.ngram import NGramProfile
from spellchecker.stemmer import Stemmer
from spellchecker.tokenizer import tokenize


class DafsaTest(unittest.TestCase):
    WORDS = ["kain", "kainan", "kumain", "kumakain", "luto", "lutuin", "niluto", "tap", "taps",
             "top", "tops"]

    def test_membership(self):
        d = DAFSA.build(self.WORDS)
        for w in self.WORDS:
            self.assertIn(w, d)
        for w in ["ka", "kai", "kumai", "lutu", "", "topss"]:
            self.assertNotIn(w, d)
        self.assertEqual(sorted(d), sorted(self.WORDS))

    def test_minimal(self):
        # tap/taps/top/tops share the suffix states: 4 transitions after the root branch
        d = DAFSA.build(["tap", "taps", "top", "tops"])
        self.assertEqual(d.num_states, 5)

    def test_round_trip(self):
        d = DAFSA.build(self.WORDS)
        self.assertEqual(sorted(DAFSA.from_dict(d.to_dict())), sorted(self.WORDS))


class LevenshteinTest(unittest.TestCase):
    def test_matches_brute_force(self):
        rng = random.Random(7)
        words = {"".join(rng.choice("aeiknlmst") for _ in range(rng.randint(1, 7)))
                 for _ in range(400)}
        d = DAFSA.build(words)
        for query in ["kain", "mata", "a", "sinta", "tnago", "lamesa"]:
            expected = {w: edit_distance(query, w) for w in words if edit_distance(query, w) <= 2}
            self.assertEqual(fuzzy_search(d, query, 2), expected, query)

    def test_paper_example(self):
        d = DAFSA.build(["itinago", "tago", "bahay"])
        self.assertEqual(fuzzy_search(d, "tnago", 2), {"itinago": 2, "tago": 1})


class MetaphoneTest(unittest.TestCase):
    def test_paper_example_same_code(self):
        # "make words with similar sound (e.g. aksion, aksiyon, and aksyon) have similar code"
        self.assertEqual(encode("aksion"), encode("aksiyon"))
        self.assertEqual(encode("aksiyon"), encode("aksyon"))

    def test_filipino_variants(self):
        for a, b in [("meron", "mayroon"), ("kuwento", "kwento"), ("Filipino", "Pilipino"),
                     ("vakasyon", "bakasyon"), ("cine", "sine"), ("calle", "kalye")]:
            self.assertEqual(encode(a), encode(b), (a, b))

    def test_dice(self):
        self.assertEqual(dice("BAHAY", "BAHAY"), 1.0)
        self.assertGreater(dice(encode("bhay"), encode("bahay")), dice(encode("bhay"), encode("ba")))


class MorphologyTest(unittest.TestCase):
    def test_paper_examples(self):
        # isinasama, isasama, isinama with the base form sama
        self.assertTrue({"isinasama", "isasama", "isinama", "sumama"} <= inflect("sama", ["i", "um"]))

    def test_paradigms(self):
        self.assertTrue({"kumain", "kumakain", "kakain", "kainin", "kinain", "kinakain"}
                        <= inflect("kain", ["um", "in"]))
        self.assertTrue({"nagluto", "nagluluto", "lutuin", "niluto"} <= inflect("luto'", ["mag", "in"]))
        self.assertTrue({"mag-aral", "nag-aaral", "pag-aralan", "pinag-aralan"}
                        <= inflect("aral", ["mag", "pagan"]))
        self.assertIn("bigyan", inflect("bigay", ["an"], "bigy"))
        self.assertEqual(reduplicate("trabaho"), "tatrabaho")


class StemmerTest(unittest.TestCase):
    LEXICON = {"kain", "sama", "luto", "aral", "ganda", "text", "bigay", "dala", "bili", "pili",
               "rin", "pa", "bahay"}

    def setUp(self):
        self.s = Stemmer()

    def stem(self, word):
        return self.s.stem(word, self.LEXICON.__contains__, exclude={"rin", "pa"})

    def test_inflections(self):
        cases = {"kumain": "kain", "kinakain": "kain", "isinasama": "sama", "nagluluto": "luto",
                 "lutuin": "luto", "kagandahan": "ganda", "pinag-aralan": "aral",
                 "nag-aaral": "aral", "bigyan": "bigay", "dalhin": "dala", "mamili": "bili",
                 "magandang": "ganda", "araw-araw": "araw", "paulit-ulit": "ulit"}
        for word, root in cases.items():
            self.assertEqual(self.stem(word), root, word)

    def test_code_switching(self):
        for word in ["magtext", "nagtetext", "nagtext"]:
            self.assertEqual(self.stem(word), "text", word)

    def test_function_words_are_not_roots(self):
        self.assertNotIn("rin", self.s.valid_stems("parin", self.LEXICON.__contains__, {"rin", "pa"}))

    def test_hyphen_before_consonant_not_stemmed(self):
        self.assertEqual(self.s.valid_stems("mag-luto", self.LEXICON.__contains__), [])


class NGramTest(unittest.TestCase):
    def test_threshold(self):
        p = NGramProfile(3, "_").train(["mano", "mana", "mani", "tao"])
        self.assertEqual(p.ngrams("yan"), ["_ya", "yan", "an_"])
        self.assertEqual(p.missing("mano", 1.0), [])
        self.assertIn("_ta", p.missing("tao", 0.10))


class TokenizerTest(unittest.TestCase):
    def test_paper_example(self):
        # "Ang bahay ko." -> Ang <space> bahay <space> ko .
        toks = [(t.text, t.kind) for t in tokenize("Ang bahay ko.")]
        self.assertEqual(toks, [("Ang", "word"), (" ", "space"), ("bahay", "word"), (" ", "space"),
                                ("ko", "word"), (".", "punct")])

    def test_hyphen_and_apostrophe(self):
        words = [t.text for t in tokenize("Nag-text siya pagka't araw-araw, mag- kasama")
                 if t.kind == "word"]
        self.assertEqual(words, ["Nag-text", "siya", "pagka't", "araw-araw", "mag-", "kasama"])


if __name__ == "__main__":
    unittest.main()
