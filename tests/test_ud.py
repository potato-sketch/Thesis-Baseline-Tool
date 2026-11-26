"""Tests for the Universal Dependencies (CoNLL-U) word-list converter."""
import tempfile
import unittest
from pathlib import Path

from spellchecker.ud import read_treebanks

# Modelled on the first sentence of UD_Tagalog-Ugnayan.
SAMPLE = """# sent_id = s1
# text = "Tay, pwede ba akong sumama sa pasada ninyo?" tanong ko kay Tatay.
1\t"\t"\tPUNCT\t_\t_\t8\tpunct\t_\t_
2\tTay\tTay\tPROPN\t_\t_\t8\tvocative\t_\t_
3\t,\t,\tPUNCT\t_\t_\t8\tpunct\t_\t_
4\tpwede\tpwede\tADJ\t_\t_\t8\tadvmod\t_\t_
5\tba\tba\tPART\t_\t_\t8\tmark\t_\t_
6-7\takong\t_\t_\t_\t_\t_\t_\t_\t_
6\tako\tako\tPRON\t_\t_\t8\tnsubj\t_\t_
7\t-ng\tna\tPART\t_\t_\t4\tmark\t_\t_
8\tsumama\tsama\tVERB\t_\t_\t0\troot\t_\t_
9\tsa\tsa\tADP\t_\t_\t10\tcase\t_\t_
10\tpasada\tpasada\tNOUN\t_\t_\t8\tobl\t_\t_
11\tninyo\tinyo\tPRON\t_\t_\t10\tnmod\t_\t_
12\t?\t?\tPUNCT\t_\t_\t8\tpunct\t_\t_
13\trin\trin\tADV\t_\t_\t8\tadvmod\t_\t_
14\tko\tnull\tADP\t_\t_\t8\tobj\t_\t_

# sent_id = s2
1-2\testudyanteng\t_\t_\t_\t_\t_\t_\t_\t_
1\testudyante\testudyante\tNOUN\t_\t_\t0\troot\t_\t_
2\t-ng\tna\tPART\t_\t_\t1\tmark\t_\t_
3\t12\t12\tNUM\t_\t_\t1\tnummod\t_\t_
"""


class UDReaderTest(unittest.TestCase):
    def read(self, **kwargs):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.conllu"
            path.write_text(SAMPLE, encoding="utf-8")
            return read_treebanks([path], **kwargs)

    def test_forms_lemmas_and_classes(self):
        lex = self.read()
        self.assertEqual(lex.sentences, 2)
        self.assertTrue({"pwede", "sumama", "sama", "pasada", "estudyante", "estudyanteng", "tay"}
                        <= lex.words)                          # forms, lemmas, proper nouns
        self.assertTrue({"ba", "ako", "akong", "sa", "ninyo", "inyo", "rin", "ko"}
                        <= lex.function_words)                 # closed classes + enclitic ADV
        everything = lex.words | lex.function_words
        for junk in ['"', ",", "?", "-ng", "null", "12", "na"]:
            self.assertNotIn(junk, everything, junk)          # punctuation, clitic pieces, digits

    def test_without_proper_nouns(self):
        self.assertNotIn("tay", self.read(include_proper_nouns=False).words)


if __name__ == "__main__":
    unittest.main()
