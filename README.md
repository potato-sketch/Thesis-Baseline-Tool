# Filipino Spell Checker — replication of Octaviano & Borra (TENCON 2017)

A working Python implementation of the system in

> M. Octaviano Jr and A. Borra, *A Spell Checker for a Low-resourced and Morphologically
> Rich Language*, Proc. IEEE Region 10 Conference (TENCON), 2017, pp. 1853–1856.

It detects and corrects typographical errors in Filipino text, including inflected forms
(*isinasama, isasama, isinama* ← *sama*), borrowing and code-switching
(*nag-text, mag-research*; the solid *magtext* is corrected to *mag-text*), and ranks suggestions with a Filipino variant of the
metaphone algorithm. Pure Python standard library — nothing to install.

## Run it in VS Code

1. **File → Open Folder…** and choose this folder.
2. Install the recommended **Python** extension when VS Code asks (or from the Extensions view).
3. Select a Python 3.10+ interpreter (`Ctrl+Shift+P` → *Python: Select Interpreter*).
4. Open **Run and Debug** (`Ctrl+Shift+D`), pick a configuration, press **F5**:

| Configuration | What it does |
|---|---|
| Spell checker app (GUI) | Desktop app: misspellings underlined, click one for ranked suggestions |
| Check a sentence | Prompts for a sentence and prints flags + suggestions |
| Train model (modeling module) | Rebuilds the automata and the trigram profile from `data/` |
| Evaluate (100 test sentences) | Recall, precision, F-measure, suggestion adequacy → `results/evaluation.md` |
| Evaluate, paper-only pipeline | Same, with this project's extensions switched off |
| Evaluate with UD Ugnayan only | Same, with the treebank as the only Tagalog word list → `results/evaluation_ud.md` |
| Tune n-gram threshold | The threshold experiment of Section II-B |
| Unit tests | 37 tests, including every example given in the paper |

The tests also appear in the **Testing** view (beaker icon). The same commands work in the terminal:

```powershell
python -m spellchecker gui
python -m spellchecker check "Hindi parin siya pumasok dahil mganda ang panahon."
python -m spellchecker evaluate -v
python -m spellchecker evaluate --lexicon ud
python -m spellchecker tune
python -m spellchecker stem isinasama nagtetext kagandahan
python -m spellchecker phonetic aksion aksiyon aksyon
python -m unittest discover -s tests -t .
```

On **macOS / Linux**, go to the project folder first and type `python3` instead of `python`
(VS Code's integrated terminal already opens in the project folder):

```bash
cd ~/Documents/GitHub/Thesis-Baseline-Tool   # wherever you cloned it
python3 -m spellchecker gui
python3 -m spellchecker check "Hindi parin siya pumasok dahil mganda ang panahon."
python3 -m unittest discover -s tests -t .
```

The **Terminal → Run Task…** entries pick `python3` automatically on a Mac.

## How the paper maps to the code (Fig. 1)

| Paper | File | Notes |
|---|---|---|
| **Modeling module** | [spellchecker/modeling.py](spellchecker/modeling.py) | Builds everything from `data/`; retrains automatically when a word list (or the stemmer) changes |
| Tagalog word list from a UD treebank | [spellchecker/ud.py](spellchecker/ud.py) | Optional source: see *Using a Universal Dependencies treebank* |
| English and Tagalog word lists → two deterministic acyclic FSAs | [spellchecker/dafsa.py](spellchecker/dafsa.py) | Minimal DAFSA, incremental construction of Daciuk et al. (2000) |
| Stemmer for Filipino phenomena | [spellchecker/stemmer.py](spellchecker/stemmer.py), [morphology.py](spellchecker/morphology.py) | Prefixes with partial assimilation (pang-/pan-/pam-), -um-/-in- infixes, CV reduplication, suffixes with o→u, d→r and syncope, circumfixes, linker -ng, full reduplication, compounds |
| Stemmed character-trigram profile | [spellchecker/ngram.py](spellchecker/ngram.py) | Type frequencies; "top X%" threshold |
| **Error detection module** | [spellchecker/detection.py](spellchecker/detection.py) | Dictionary look-up → stem and look up again → code-switching & compound check for hyphenated words → n-gram look-up |
| Tokenization | [spellchecker/tokenizer.py](spellchecker/tokenizer.py) | Words vs punctuation; keeps *araw-araw*, *pagka't*, *mag-* |
| **Error correction module** | [spellchecker/correction.py](spellchecker/correction.py) | Space-dash correction (merge test, split test, hyphen rules) → edit distance |
| Levenshtein automaton (≤ 2 edits) traversed in parallel with the Tagalog automaton | [spellchecker/levenshtein.py](spellchecker/levenshtein.py) | Schulz & Mihov (2002), built lazily as a DFA |
| Modified metaphone + Dice coefficient ranking | [spellchecker/metaphone.py](spellchecker/metaphone.py) | 37 ordered rules (the paper's had 56; its rules were not published) |
| Evaluation metrics of Van Zaanen & Van Huyssteen (2003) | [spellchecker/evaluation.py](spellchecker/evaluation.py) | |
| Interface (not described in the paper) | [spellchecker/gui.py](spellchecker/gui.py), [`__main__.py`](spellchecker/__main__.py) | Tkinter app and command line |

## Results

The paper tested 100 sentences from students' translation exercises, each with one error.
Those sentences and the paper's word lists were not published, so this replication ships
its own resources (see *Assumptions*). [data/test_sentences.tsv](data/test_sentences.tsv) has
100 sentences with **exactly the error-type distribution of Table I** (8 insertion,
28 deletion, 37 substitution, 9 space deletion, 12 hyphen insertion, 6 space insertion),
including the six example pairs of Table I.

The test sentences and the seed lexicon were written together, so every correct word in them
is in the lexicon, which makes precision on them unrealistically perfect. For a fair
precision figure, [data/clean_sentences.txt](data/clean_sentences.txt) holds 40 **held-out
error-free sentences** on other topics whose vocabulary was deliberately *not* added to the
lexicon; every flag on them is a false positive (out-of-vocabulary words — the same cause the
paper gives for its false positives).

n-gram threshold 0.20, English word list from UD English-EWT (see below), precision counted
over the test sentences plus the held-out clean sentences:

| Tagalog word list | Recall | Precision | F-measure | Suggestion adequacy | Right word first |
|---|---|---|---|---|---|
| **both** (seed + UD Ugnayan), default | 97.00% | 64.67% | 77.60% | 98.97% | 89.69% |
| both, paper-only pipeline | 87.00% | 64.44% | 74.04% | 91.95% | 81.61% |
| seed only | 97.00% | 63.40% | 76.68% | 98.97% | 89.69% |
| UD Ugnayan only | 100.00% | 20.53% | 34.07% | 31.00% | |
| *Paper (Octaviano & Borra, 2017)* | *81%* | *53.64%* | *64.53%* | *87.78%* | |

Full tables (per error type, false negatives, false alarms, failed suggestions) are in
[results/](results/): `evaluation.md` (both), `evaluation_paper_only.md`,
`evaluation_seed.md`, `evaluation_ud.md` and `evaluation_ud_paper_only.md`. These numbers
are not directly comparable with the paper's: different lexicon, different sentences. The
threshold was chosen on the same data it is reported on. The *behaviour* matches what the
paper describes:

- Missed errors come from the stemmer or the trigram profile: *kalabay* passes because all
  trigrams of its stem *labay* are frequent, and *maintindhan* passes because the stemmer
  reads it as *ma-intindi-han*.
- False positives are out-of-vocabulary words: loanwords (*henerasyon, eksperto*), proper
  nouns (*Rizal, Palawan*), roots missing from the seed lexicon.
- The right word is not always ranked first, because ranking is phonetic. *meron* → *mayroon*
  is never suggested: it is 3 edits away.

`python -m spellchecker tune` reproduces the threshold experiment: lower thresholds raise
recall and also false alarms.

## Using a Universal Dependencies treebank as the word list

Every `*.conllu` file in [data/ud/](data/ud/) is converted by
[spellchecker/ud.py](spellchecker/ud.py) into `tagalog_ud_words.txt` (written forms +
lemmas) and `tagalog_ud_function_words.txt` (closed-class words). Choose the word list with
`LEXICON` in [config.py](spellchecker/config.py), `--lexicon seed|ud|both` on the command
line, or the **Word list** dropdown in the app.

| CoNLL-U column | Used for |
|---|---|
| FORM | Every written word, lower-cased. For a fused token such as *akong* (*ako* + *-ng*) the written form is kept and the pieces `-ng`, `'y`, `'t` are dropped |
| LEMMA | Added as well (*sumama* → *sama*); `_` and `null` are skipped |
| UPOS | PUNCT/SYM are skipped. ADP, AUX, CCONJ, DET, PART, PRON and SCONJ are function words, and so are enclitic particles tagged ADV (*rin, lang, pa, naman*). PROPN is kept (`UD_INCLUDE_PROPER_NOUNS`) |

A word that is also used as a content word somewhere is not treated as a function word.
UD tags *bago* "before" as SCONJ, but *bago* "new" takes the linker (*bagong*) and affixes.

**Included: [UD_Tagalog-Ugnayan](https://github.com/UniversalDependencies/UD_Tagalog-Ugnayan)**
(Angelina Aquino, University of the Philippines; CC BY-NC-SA 4.0; its README and license are
in `data/ud/`). It has 94 sentences and 1,011 tokens of DepEd educational text, which give
**427 Tagalog words** (356 content words and lemmas, 71 function words). On its own that is
far too small for a spell checker: almost every word is unknown, so recall is high only
because nearly everything is flagged. Only 31% of errors get the intended correction, since
it usually isn't among the 427 words. Combined with the seed list it helps, with fewer false
alarms on the held-out text than the seed list alone (54 vs 57).

For a UD-based word list of useful size,
[UD_Tagalog-NewsCrawl](https://github.com/UniversalDependencies/UD_Tagalog-NewsCrawl)
(15,619 sentences, 320,646 tokens, CC BY-SA 4.0; data files on its `dev` branch) is about
300× larger. Drop its `.conllu` files into `data/ud/` and retrain. Keep any sentences you
evaluate on out of the word list.

## English word list: UD English-EWT

The English automaton (code-switching: *nag-text, mag-research*) is built from
[UD_English-EWT](https://github.com/UniversalDependencies/UD_English-EWT) (CC BY-SA 4.0;
its README and license are in [data/ud_english/](data/ud_english/)): 16,622 sentences and
254,820 words of blogs, reviews, e-mail and web text. Every `*.conllu` file in that folder
is converted by [spellchecker/ud.py](spellchecker/ud.py) into `english_ud_words.txt`
(14,103 words). Web text is noisy, so the converter keeps only plain alphabetic words:

| Skipped | Why |
|---|---|
| Tokens marked `Typo=Yes` (*accomodate, actualy*) | EWT annotates misspellings; the corrected lemma (*accommodate*) is kept |
| `Foreign=Yes`, and UPOS PUNCT, SYM, NUM, X | Not English words |
| PROPN (`UD_ENGLISH_INCLUDE_PROPER_NOUNS`) | Names (*Enron, Houston*) would accept misspellings |
| Pieces of multiword tokens (*gonna* = *gon* + *na*) | Only the written form is kept; *na* is Tagalog, not English |
| Digits, apostrophes, one-letter words other than *a* and *i* | |

Choose the English list with `ENGLISH_LEXICON` in [config.py](spellchecker/config.py),
`--english seed|ud|both` on the command line, or the **English list** dropdown in the app.
`seed` is the earlier hand-written [data/english_words.txt](data/english_words.txt) (~700 words).
With the default Tagalog list:

| English word list | Recall | Precision | F-measure | Suggestion adequacy |
|---|---|---|---|---|
| seed (700 words) | 97.00% | 64.24% | 77.29% | 98.97% |
| **ud** (EWT, 14,103 words), default | 97.00% | 64.67% | 77.60% | 98.97% |
| both | 97.00% | 65.10% | 77.91% | 98.97% |

A larger English list also contains words that are Tagalog prefixes (*nag* "to nag", *pan*,
*sing*). Extension 1 below therefore flags a prefix of three or more letters written alone
even when the English list knows it. In paper-only mode the split test uses both word
lists, so it now finds splits such as *nag aral* and *par in*. Because the paper computes
edit-distance candidates only when space-dash finds nothing, paper-only suggestion adequacy
drops (96.59% with the seed English list, 91.95% with EWT). That is the paper's rule
applied to a bigger dictionary.

## Assumptions and deviations

The paper leaves several details open. Every choice made here is listed below.

**Resources (the biggest difference).** The paper's word lists are not public. This project
ships a seed lexicon: [data/tagalog_words.txt](data/tagalog_words.txt) (~900 content
words), [data/tagalog_function_words.txt](data/tagalog_function_words.txt),
[data/tagalog_paradigms.tsv](data/tagalog_paradigms.tsv) (≈ 250 roots with their
affixation classes, expanded to ~2,300 inflected forms in `tagalog_inflections.txt`), and
[data/english_words.txt](data/english_words.txt) (~700 words; the default English list is
now UD English-EWT, see above). That is 3,500 Tagalog words in total, far smaller than a
real dictionary. The default word list adds the UD
Ugnayan treebank (see above). Put bigger lists in `data/extra/` (see its README) or more
treebanks in `data/ud/`, and retrain.

**Extensions** (on by default; `--paper-only` or the GUI checkbox turns them off):

1. *Bound-prefix check.* A prefix written as its own word (*pag bigay*) is flagged, even when
   it is also an English word (*nag*). Without it,
   the merge test can never run, because detection accepts *pag* by its trigrams
   (paper-only: 0 of 6 space insertions detected).
2. *Clitic-split check.* A function word fused with a neighbour (*parin, nalang, kana*) is
   flagged. It costs occasional false alarms on unknown words that happen to split that way
   (*palaka* → "pala ka").
3. *More suggestions.* Edit-distance candidates are listed after the space-dash suggestions.
   The paper only computes them when space-dash finds nothing, so *bahaay* gets only
   "baha ay".
4. *Dash test.* Space-dash correction also drops a hyphen that Filipino orthography doesn't
   allow (*magka-ugnay* → *magkaugnay*) or adds one it requires (*nagaral* → *nag-aral*).
   In paper-only mode the hyphen-insertion errors of Table I are corrected by edit distance
   instead (deleting the hyphen is one edit).
5. *Contractions.* *ako'y*, *ganito't* are accepted when the bare word is known. In
   paper-only mode the stemmer handles them.
6. *English roots under Tagalog affixes* must have ≥ 4 letters, so *pa-ka-i-not* and
   *ka-i-big* don't validate misspellings. The paper maps every stem into both automata;
   in paper-only mode *napakainot* is accepted as *napaka-* + *not*.
7. *Stricter hyphen checks.* The code-switching check also accepts a prefix plus a
   reduplicated syllable (*nagte-text*); the compound check rejects function words. In
   paper-only mode the check is literally "Tagalog prefix + English word" and then
   "both parts in the Tagalog word list".
8. *Split test on the Tagalog list.* The paper says the split pairs get "a dictionary
   look-up", which in its detection module means both word lists. Paper-only mode uses
   both, so *aklatam* gets "aklat am" (*am* is English) and, since space-dash found
   something, no edit-distance candidates.
9. *English root set off with a hyphen.* Filipino orthography (KWF, *Ortograpiyang
   Pambansa*) writes an English word that keeps its English spelling apart from a Tagalog
   affix: *i-check, nag-text, ma-save*. A solid form such as *nagreply*, *ipost* or
   *nagtetext* is flagged (`english-hyphen`) and corrected to *nag-reply*, *i-post*,
   *nagte-text*. The merge test does the same for a prefix written apart: *nag binge* →
   *nag-binge* instead of *nagbinge*. A root counts as English when it is in the English
   word list and not in the Tagalog one. In the merge test, a word in neither list gets
   both spellings, the hyphenated one first when its trigrams are rare in Tagalog
   (*nag binge* → *nag-binge, nagbinge*). A word with a Tagalog analysis is never
   hyphenated, and neither are the assimilated nasal prefixes *pan-, man-, pam-* (so
   *manpower* is not *man-power*). A reduplicated syllable must copy the root's first
   letters (*nagte-text*, not *maa-gang*). Infixed forms (*tinry, chineck*) are left as
   they are. The rule needs a good Tagalog word list: with UD Ugnayan alone, *mabait* is
   missing and is read as *ma-* + English *bait*. The paper accepts both *magtext* and
   *nag-text*; in paper-only mode *magtext* is
   still accepted and *nag binge* still merges to *nagbinge*.

With the extensions off, every step the paper describes runs exactly as written. Only the
details the paper leaves open (below) are shared by both modes.

**Other choices**

- *Hyphen rule in the stemmer.* A hyphen after a prefix is only accepted before a vowel
  (*mag-aral*). That keeps *pag-kain* detectable.
- *Metaphone.* Filipino vowels are phonemic, so they are kept in three classes (e~i, o~u, a)
  instead of being dropped as in English metaphone.
- *Trigrams.* Padded with `_` on both sides; frequencies count the distinct stems containing
  each trigram.

## Project layout

```
spellchecker/      the three modules + CLI + GUI
data/              word lists, paradigms, test sentences, held-out clean sentences
data/ud/           Tagalog UD treebanks (*.conllu) and the word lists generated from them
data/ud_english/   English UD treebank (EWT) and the English word list generated from it
data/extra/        drop-in folders for larger word lists
results/           evaluation reports (Markdown)
tests/             unittest suite
models/            trained model (generated, git-ignored)
.vscode/           run/debug configurations, tasks, test settings
```
