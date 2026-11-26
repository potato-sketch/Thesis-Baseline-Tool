"""End-to-end tests on the examples given in the paper (uses the trained model)."""
import unittest

from spellchecker import SpellChecker, load_or_train

MODEL = None


def setUpModule():
    global MODEL
    MODEL = load_or_train()


class DetectionTest(unittest.TestCase):
    def setUp(self):
        self.sc = SpellChecker(MODEL)

    def flagged(self, text):
        return [f.word for f in self.sc.check(text)]

    def test_inflected_forms_are_correct(self):
        # isinasama, isasama, isinama (base form sama) -- abstract of the paper
        self.assertEqual(self.flagged("Isinasama niya ako. Isasama niya ako. Isinama niya ako."), [])

    def test_code_switching_is_correct(self):
        # magtext, nag-text (base form text), mag-research
        self.assertEqual(self.flagged("Magtext ka. Nag-text siya. Mag-research tayo."), [])

    def test_non_word_errors(self):
        self.assertEqual(self.flagged("Ang bulaklak ay mganda."), ["mganda"])
        self.assertEqual(self.flagged("Tnago ng bata ang laruan."), ["Tnago"])

    def test_compound_and_reduplication(self):
        self.assertEqual(self.flagged("Araw-araw siyang pumapasok sa paaralan."), [])


class CorrectionTest(unittest.TestCase):
    def setUp(self):
        self.sc = SpellChecker(MODEL)

    def suggestions(self, text, word):
        for f in self.sc.check(text):
            if f.word == word:
                return [s.text for s in f.suggestions]
        self.fail(f"{word!r} was not flagged in {text!r}")

    def test_merge_test(self):
        # mag- + kasama -> magkasama ; mag- + asawa -> mag-asawa
        self.assertEqual(self.suggestions("Sila ay mag kasama.", "mag")[0], "magkasama")
        self.assertEqual(self.suggestions("Sila ay mag asawa.", "mag")[0], "mag-asawa")

    def test_split_test(self):
        # palang -> (pa, lang) ... ; parin -> pa rin
        self.assertIn("pa lang", self.suggestions("Ngayon palang ako dumating.", "palang"))
        self.assertEqual(self.suggestions("Hindi parin siya dumating.", "parin")[0], "pa rin")

    def test_dash_test(self):
        self.assertEqual(self.suggestions("Sila ay magka-ugnay.", "magka-ugnay")[0], "magkaugnay")

    def test_edit_distance(self):
        self.assertIn("itinago", [s.lower() for s in self.suggestions("Tnago ng bata ang laruan.", "Tnago")])
        self.assertEqual(self.suggestions("Hindi siya pumasok pagka't siya ay may sakit.", "pagka't")[0],
                         "pagkat")

    def test_case_is_kept(self):
        self.assertEqual(self.suggestions("Mganda ang araw.", "Mganda")[0], "Maganda")


class PaperOnlyModeTest(unittest.TestCase):
    def setUp(self):
        self.sc = SpellChecker(MODEL, use_extensions=False)

    def test_extensions_off(self):
        flags = {f.word: f.method for f in self.sc.check("Ang pag bigay ay mabuti.")}
        self.assertNotIn("pag", flags)          # bound prefix is not a paper rule

    def test_no_dash_test(self):
        # The paper has no hyphen rule: magka-ugnay is corrected by edit distance.
        sources = {s.source for s in self.sc.suggest("magka-ugnay")}
        self.assertNotIn("dash", sources)
        self.assertEqual(self.sc.corrector.space_dash("nagaral"), [])

    def test_no_edit_distance_after_space_dash(self):
        self.assertEqual([s.text for s in self.sc.suggest("parin")], ["pa rin"])

    def test_paper_examples_still_pass(self):
        flagged = [f.word for f in self.sc.check(
            "Isinasama niya ako. Magtext ka. Nag-text siya. Mag-research tayo. Araw-araw.")]
        self.assertEqual(flagged, [])

    def test_hyphen_checks_follow_the_paper(self):
        det = self.sc.detector
        self.assertEqual(det.check("nag-text").method, "code-switching")    # prefix + English
        self.assertEqual(det.check("bahay-araw").method, "compound")        # Tagalog + Tagalog


if __name__ == "__main__":
    unittest.main()
