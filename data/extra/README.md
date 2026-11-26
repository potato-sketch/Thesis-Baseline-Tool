# Extra word lists

Put additional word lists here to grow the lexicon without editing the seed files:

- `tagalog/*.txt` — Tagalog words (roots or inflected forms)
- `english/*.txt` — English words (for code-switching such as *nag-download*)

Format: words separated by spaces or new lines; `#` starts a comment; a second
column of numbers (e.g. frequencies) is ignored. The model retrains itself the
next time it is loaded, or run `python -m spellchecker train`.

After adding a large list, run `python -m spellchecker tune` again: a bigger
trigram profile changes which n-gram threshold works best.
