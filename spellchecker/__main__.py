"""Command line interface:  python -m spellchecker <command> ...

  gui                 open the desktop spell checker
  check TEXT          check a sentence (or --file path.txt)
  train               rebuild the automata and the n-gram profile
  inflect             regenerate data/tagalog_inflections.txt
  evaluate            run the 100-sentence evaluation (recall, precision, ...)
  tune                sweep the n-gram threshold
  stem WORD...        show the stems the stemmer finds
  phonetic WORD...    show Filipino-metaphone codes and Dice similarity
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import config


def _checker(args):
    from .checker import SpellChecker
    from .modeling import load_or_train
    model = load_or_train(args.lexicon, verbose=True)
    return SpellChecker(model, threshold=args.threshold,
                        use_extensions=False if args.paper_only else None,
                        skip_proper_nouns=getattr(args, "skip_proper_nouns", False))


def cmd_check(args) -> int:
    text = Path(args.file).read_text(encoding="utf-8") if args.file else " ".join(args.text)
    if not text.strip():
        print("Nothing to check. Example: python -m spellchecker check \"Hindi parin siya dumating.\"")
        return 1
    checker = _checker(args)
    flags = checker.check(text)
    print(f"\n{text.strip()}\n")
    if not flags:
        print("No misspelled words found.")
        return 0
    print(f"{len(flags)} misspelled word(s):")
    for f in flags:
        print(f"  {f.word:<18} [{f.method}] {f.detail}")
        sugg = ", ".join(s.text for s in f.suggestions) or "(no suggestion)"
        print(f"  {'':<18} suggestions: {sugg}")
    return 0


def cmd_train(args) -> int:
    from .modeling import ensure_inflections, load_or_train
    from .ud import ensure_ud_lists, treebank_files
    lexicons = config.LEXICONS if args.lexicon == "all" else [args.lexicon or config.LEXICON]
    if any(lx in ("seed", "both") for lx in lexicons):
        ensure_inflections(force=True)
    if any(lx in ("ud", "both") for lx in lexicons) and treebank_files():
        ensure_ud_lists(force=True)
    for lexicon in lexicons:
        model = load_or_train(lexicon, force=True, verbose=True)
        print("Done.", {k: v for k, v in model.info.items() if k != "sources"}, "\n")
    return 0


def cmd_inflect(args) -> int:
    from .modeling import ensure_inflections, read_wordlist
    path = ensure_inflections(force=True)
    print(f"Wrote {len(read_wordlist(path)):,} inflected forms to {path}")
    return 0


def _clean(args) -> list[str]:
    from .evaluation import load_clean_set
    return [] if args.no_clean else load_clean_set(Path(args.clean))


def cmd_evaluate(args) -> int:
    from .evaluation import evaluate, format_report, load_test_set, summary_line
    checker = _checker(args)
    items = load_test_set(Path(args.test))
    ev = evaluate(checker, items, _clean(args))
    lexicon = checker.model.info.get("lexicon", "?")
    report = format_report(ev, f"Evaluation of the Filipino spell checker ({lexicon} word list)")
    if args.report:
        out = Path(args.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"Report written to {out}")
    print(report if args.verbose else "")
    print(summary_line(ev))
    return 0


def cmd_tune(args) -> int:
    from .evaluation import load_test_set, tune
    from .modeling import load_or_train
    model = load_or_train(args.lexicon, verbose=True)
    items = load_test_set(Path(args.test))
    thresholds = [float(t) for t in args.thresholds.split(",")]
    clean = _clean(args)
    print(f"\n{'':>9} {'':>8} {'test sentences only':^22} "
          f"{'+ clean sentences' if clean else '':^30}")
    print(f"{'threshold':>9} {'recall':>8} {'precision':>10} {'F-measure':>10} "
          f"{'adequacy':>9} {'false alarms':>13} {'precision':>10} {'F-measure':>10}")
    best = None
    for ev in tune(model, items, thresholds, use_extensions=not args.paper_only, clean=clean):
        print(f"{ev.threshold:>9.2f} {ev.recall:>8.2%} {ev.precision:>10.2%} "
              f"{ev.f_measure:>10.2%} {ev.adequacy:>9.2%} {ev.clean_fp:>13} "
              f"{ev.precision_all:>10.2%} {ev.f_measure_all:>10.2%}")
        if best is None or ev.f_measure_all > best.f_measure_all:
            best = ev
    which = "including the clean sentences" if clean else "on the test sentences"
    print(f"\nBest F-measure {which}: threshold {best.threshold:.2f}. "
          f"Set NGRAM_THRESHOLD in spellchecker/config.py to use it by default.")
    return 0


def cmd_stem(args) -> int:
    from .detection import ErrorDetector
    from .modeling import load_or_train
    detector = ErrorDetector(load_or_train(args.lexicon, verbose=True))
    for word in args.words:
        w = word.lower()
        print(f"{word:<20} dictionary stems: {', '.join(detector.stems(w)[:5]) or '-':<30} "
              f"greedy: {detector.stemmer.greedy(w)}")
    return 0


def cmd_phonetic(args) -> int:
    from .metaphone import RULES, dice, encode
    codes = [(w, encode(w)) for w in args.words]
    for w, c in codes:
        print(f"{w:<20} {c}")
    if len(codes) > 1:
        base_word, base = codes[0]
        print(f"\nDice similarity with '{base_word}':")
        for w, c in codes[1:]:
            print(f"  {w:<18} {dice(base, c):.3f}")
    print(f"\n({len(RULES)} encoding rules)")
    return 0


def cmd_gui(args) -> int:
    from .gui import main as gui_main
    gui_main(args.lexicon)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m spellchecker",
                                description="Filipino spell checker (Octaviano & Borra, TENCON 2017)")
    sub = p.add_subparsers(dest="command")

    def lexicon_option(sp, extra=()):
        sp.add_argument("--lexicon", choices=[*config.LEXICONS, *extra], default=None,
                        help=f"Tagalog word list: seed, ud (treebanks in data/ud/) or both "
                             f"(default {config.LEXICON})")

    def detection_options(sp):
        lexicon_option(sp)
        sp.add_argument("--threshold", type=float, default=None,
                        help=f"n-gram threshold (default {config.NGRAM_THRESHOLD})")
        sp.add_argument("--paper-only", action="store_true",
                        help="disable the bound-prefix and clitic-split extensions")

    sp = sub.add_parser("check", help="check a sentence or a text file")
    sp.add_argument("text", nargs="*")
    sp.add_argument("--file")
    sp.add_argument("--skip-proper-nouns", action="store_true")
    detection_options(sp)
    sp.set_defaults(func=cmd_check)

    sp = sub.add_parser("train", help="rebuild the model")
    lexicon_option(sp, extra=("all",))
    sp.set_defaults(func=cmd_train)
    sub.add_parser("inflect", help="regenerate the inflected Tagalog forms").set_defaults(func=cmd_inflect)

    def test_options(sp):
        sp.add_argument("--test", default=str(config.TEST_SET))
        sp.add_argument("--clean", default=str(config.CLEAN_SET),
                        help="held-out error-free sentences (flags there count as false positives)")
        sp.add_argument("--no-clean", action="store_true", help="ignore the clean sentences")

    sp = sub.add_parser("evaluate", help="recall / precision / F-measure / suggestion adequacy")
    test_options(sp)
    sp.add_argument("--report", help="write a Markdown report to this path")
    sp.add_argument("-v", "--verbose", action="store_true", help="print the full report")
    detection_options(sp)
    sp.set_defaults(func=cmd_evaluate)

    sp = sub.add_parser("tune", help="sweep the n-gram threshold")
    test_options(sp)
    lexicon_option(sp)
    sp.add_argument("--thresholds", default="0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0")
    sp.add_argument("--paper-only", action="store_true")
    sp.set_defaults(func=cmd_tune)

    sp = sub.add_parser("stem", help="show stems")
    sp.add_argument("words", nargs="+")
    lexicon_option(sp)
    sp.set_defaults(func=cmd_stem)

    sp = sub.add_parser("phonetic", help="show metaphone codes")
    sp.add_argument("words", nargs="+")
    sp.set_defaults(func=cmd_phonetic)

    sp = sub.add_parser("gui", help="open the desktop app")
    lexicon_option(sp)
    sp.set_defaults(func=cmd_gui)
    return p


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
