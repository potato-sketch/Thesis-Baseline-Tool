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
        # nag-text (base form text), mag-research, nagte-text, i-submit
        self.assertEqual(self.flagged(
            "Mag-text ka. Nag-text siya. Mag-research tayo. Nagte-text siya. I-submit mo."), [])

    def test_english_root_needs_hyphen(self):
        # extension: an English root under a Tagalog prefix is set off with a hyphen
        flags = {f.word: f for f in self.sc.check("Magtext ka. Nagreply siya at nagtetext pa.")}
        self.assertEqual(set(flags), {"Magtext", "Nagreply", "nagtetext"})
        self.assertEqual(flags["Magtext"].method, "english-hyphen")
        self.assertEqual(flags["Magtext"].suggestions[0].text, "Mag-text")
        self.assertEqual(flags["Nagreply"].suggestions[0].text, "Nag-reply")
        self.assertEqual(flags["nagtetext"].suggestions[0].text, "nagte-text")

    def test_tagalog_words_take_no_hyphen(self):
        det = self.sc.detector
        for word in ["maganda", "nagluto", "isinasama", "magkasama"]:
            self.assertEqual(det.hyphenations(word), [], word)
        self.assertEqual(det.hyphenations("manpower"), [])     # man- is an assimilated prefix

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

    def test_merge_test_english_root(self):
        # extension: the English root stays apart with a hyphen
        self.assertEqual(self.suggestions("Mag update ka.", "Mag")[0], "Mag-update")
        self.assertEqual(self.suggestions("Nag text siya.", "Nag")[0], "Nag-text")
        # 'binge' is in neither word list; its trigrams are rare in Tagalog
        self.assertEqual(self.suggestions("Nag binge watch kami.", "Nag")[0], "Nag-binge")

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
        # no hyphen is added; the split test may still find "nag aral" ('nag' is English)
        self.assertNotIn("nag-aral", [s.text for s in self.sc.corrector.space_dash("nagaral")])

    def test_no_edit_distance_after_space_dash(self):
        suggestions = self.sc.suggest("parin")
        self.assertEqual(suggestions[0].text, "pa rin")
        self.assertNotIn("edit-distance", {s.source for s in suggestions})

    def test_paper_examples_still_pass(self):
        flagged = [f.word for f in self.sc.check(
            "Isinasama niya ako. Magtext ka. Nag-text siya. Mag-research tayo. Araw-araw.")]
        self.assertEqual(flagged, [])

    def test_no_english_root_hyphen(self):
        # The paper merges by the Tagalog prefix rules only: nag + binge -> nagbinge.
        self.assertEqual(self.sc.corrector.merge_test("nag", "binge")[0].text, "nagbinge")
        self.assertFalse(self.sc.detect("nagreply").is_error)

    def test_hyphen_checks_follow_the_paper(self):
        det = self.sc.detector
        self.assertEqual(det.check("nag-text").method, "code-switching")    # prefix + English
        self.assertEqual(det.check("bahay-araw").method, "compound")        # Tagalog + Tagalog


if __name__ == "__main__":
    unittest.main()
