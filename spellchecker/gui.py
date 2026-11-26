"""Desktop front end (Tkinter, part of the Python standard library).

Type or open a Filipino text, press Check: misspelled words are underlined
in red. Click one to see why it was flagged and its ranked suggestions;
double-click a suggestion (or press Replace) to apply it.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from . import config
from .checker import Flag, SpellChecker
from .modeling import load_or_train

SAMPLE_TEXT = (
    "Nag-text ako sa kanya pero hindi parin siya sumasagot. "
    "Ang mga bulaklak sa hardin ay mganda. "
    "Gusto kong mag luto ng adobo mamaya para sa aming hpunan. "
    "Masarap ang pag-kain sa handaan kagabi. "
    "Hindi siya pumasok sa paaralan pagka't siya ay may sakit. "
    "Isinama niya ang kanyang kapatid at magtetext daw siya mamaya."
)


class SpellCheckerApp:
    def __init__(self, root: tk.Tk, lexicon: str | None = None,
                 english: str | None = None) -> None:
        self.root = root
        self.lexicon = tk.StringVar(value=lexicon or config.LEXICON)
        self.english = tk.StringVar(value=english or config.ENGLISH_LEXICON)
        self.model = None
        self.checker: SpellChecker | None = None
        self.flags: list[Flag] = []
        self.current: int | None = None
        self.ignored: set[str] = set()

        root.title("Filipino Spell Checker - Octaviano & Borra (TENCON 2017) replication")
        # Sizes are given for a 96-dpi screen and scaled, so the window keeps its
        # proportions at 125 %/150 % display scaling (fonts scale automatically).
        self.scale = max(1.0, root.winfo_fpixels("1i") / 96)
        screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry(f"{min(self._px(1100), int(screen_w * 0.95))}x"
                      f"{min(self._px(640), int(screen_h * 0.85))}")
        root.minsize(min(self._px(820), int(screen_w * 0.8)),
                     min(self._px(480), int(screen_h * 0.7)))
        style = ttk.Style(root)
        if "vista" in style.theme_names():
            style.theme_use("vista")

        self.threshold = tk.DoubleVar(value=config.NGRAM_THRESHOLD)
        self.extensions = tk.BooleanVar(value=config.USE_EXTENSIONS)
        self.skip_names = tk.BooleanVar(value=False)
        self.status = tk.StringVar(value="Loading the language model ...")

        self._build_toolbar()
        # packed before the body so a tall text area can never push it off-screen
        ttk.Label(root, textvariable=self.status, anchor="w", padding=(10, 4)).pack(
            side="bottom", fill="x")
        body = ttk.Frame(root, padding=(10, 0, 10, 0))
        body.pack(fill="both", expand=True)
        # sidebar first: pack gives space in packing order, so a wide editor
        # could otherwise squeeze the suggestions panel down to nothing
        self._build_sidebar(body)
        self._build_editor(body)

        self.text.insert("1.0", SAMPLE_TEXT)
        root.after(100, self._load_model)

    def _px(self, pixels: int) -> int:
        return round(pixels * self.scale)

    # ---------------------------------------------------------------- layout
    def _build_toolbar(self) -> None:
        bar = ttk.Frame(self.root, padding=10)
        bar.pack(fill="x")
        ttk.Button(bar, text="Check", command=self.check).pack(side="left")
        ttk.Button(bar, text="Open file...", command=self.open_file).pack(side="left", padx=6)
        ttk.Button(bar, text="Clear", command=self.clear).pack(side="left")
        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=10)
        for label, var, values in (("Tagalog list", self.lexicon, config.LEXICONS),
                                   ("English list", self.english, config.ENGLISH_LEXICONS)):
            ttk.Label(bar, text=label).pack(side="left")
            combo = ttk.Combobox(bar, textvariable=var, values=values, state="readonly", width=6)
            combo.pack(side="left", padx=(4, 10))
            combo.bind("<<ComboboxSelected>>", lambda _e: self._load_model())
        ttk.Label(bar, text="n-gram threshold").pack(side="left")
        scale = ttk.Scale(bar, from_=0.05, to=1.0, variable=self.threshold, length=160,
                          command=lambda _v: self.threshold_label.config(
                              text=f"{self.threshold.get():.2f}"))
        scale.pack(side="left", padx=4)
        scale.bind("<ButtonRelease-1>", lambda _e: self.rebuild_checker())
        self.threshold_label = ttk.Label(bar, text=f"{self.threshold.get():.2f}", width=5)
        self.threshold_label.pack(side="left")
        ttk.Checkbutton(bar, text="Extensions (bound prefix, clitic split)",
                        variable=self.extensions, command=self.rebuild_checker).pack(side="left", padx=8)
        ttk.Checkbutton(bar, text="Skip proper nouns", variable=self.skip_names,
                        command=self.rebuild_checker).pack(side="left")
        ttk.Button(bar, text="Retrain model", command=self.retrain).pack(side="right")

    def _build_editor(self, parent: ttk.Frame) -> None:
        frame = ttk.Frame(parent)
        frame.pack(side="left", fill="both", expand=True)
        # width=40: a small requested width; the editor still expands to fill the window
        self.text = tk.Text(frame, wrap="word", font=("Segoe UI", 13), undo=True, width=40,
                            padx=10, pady=10, relief="solid", borderwidth=1)
        scroll = ttk.Scrollbar(frame, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        self.text.tag_configure("error", underline=True, foreground="#c62828")
        self.text.tag_configure("current", background="#ffe0b2")
        self.text.tag_bind("error", "<Button-1>", self._on_error_click)
        self.text.tag_bind("error", "<Enter>", lambda _e: self.text.config(cursor="hand2"))
        self.text.tag_bind("error", "<Leave>", lambda _e: self.text.config(cursor="xterm"))
        self.text.bind("<Control-Return>", lambda _e: (self.check(), "break")[1])

    def _build_sidebar(self, parent: ttk.Frame) -> None:
        side = ttk.Frame(parent, width=self._px(320), padding=(self._px(12), 0, 0, 0))
        side.pack(side="right", fill="y")
        side.pack_propagate(False)
        ttk.Label(side, text="Flagged words", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.flag_list = tk.Listbox(side, height=8, activestyle="none", exportselection=False,
                                    font=("Segoe UI", 10))
        self.flag_list.pack(fill="x", pady=(2, 10))
        self.flag_list.bind("<<ListboxSelect>>", self._on_flag_select)

        self.word_label = ttk.Label(side, text="", font=("Segoe UI", 14, "bold"))
        self.word_label.pack(anchor="w")
        self.reason_label = ttk.Label(side, text="", wraplength=self._px(300), foreground="#555")
        self.reason_label.pack(anchor="w", pady=(0, 8))

        ttk.Label(side, text="Suggestions (ranked)", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.sugg_list = tk.Listbox(side, height=9, activestyle="none", exportselection=False,
                                    font=("Segoe UI", 11))
        self.sugg_list.pack(fill="x", pady=(2, 6))
        self.sugg_list.bind("<Double-Button-1>", lambda _e: self.replace())
        buttons = ttk.Frame(side)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Replace", command=self.replace).pack(side="left")
        ttk.Button(buttons, text="Ignore", command=self.ignore).pack(side="left", padx=6)

    # ----------------------------------------------------------------- model
    def _load_model(self) -> None:
        self.status.set(f"Loading the '{self.lexicon.get()}' Tagalog and "
                        f"'{self.english.get()}' English word lists ...")
        self.root.config(cursor="watch")
        self.root.update_idletasks()
        try:
            self.model = load_or_train(self.lexicon.get(), english=self.english.get())
        except Exception as exc:  # show the problem instead of a silent crash
            messagebox.showerror("Could not load the model", str(exc))
            self.status.set("Model not loaded.")
            return
        finally:
            self.root.config(cursor="")
        self.rebuild_checker()

    def rebuild_checker(self) -> None:
        if self.model is None:
            return
        self.checker = SpellChecker(self.model, threshold=round(self.threshold.get(), 2),
                                    use_extensions=self.extensions.get(),
                                    skip_proper_nouns=self.skip_names.get())
        self.check()

    def retrain(self) -> None:
        self.status.set("Retraining from the word lists ...")
        self.root.config(cursor="watch")
        self.root.update_idletasks()
        try:
            self.model = load_or_train(self.lexicon.get(), force=True, english=self.english.get())
        finally:
            self.root.config(cursor="")
        info = self.model.info
        self.status.set(f"Retrained: {info['tagalog_words']:,} Tagalog and "
                        f"{info['english_words']:,} English words in {info['seconds']} s.")
        self.rebuild_checker()

    # ---------------------------------------------------------------- actions
    def check(self) -> None:
        if self.checker is None:
            return
        content = self.text.get("1.0", "end-1c")
        self.flags = [f for f in self.checker.check(content) if f.word.lower() not in self.ignored]
        self.text.tag_remove("error", "1.0", "end")
        self.text.tag_remove("current", "1.0", "end")
        self.flag_list.delete(0, "end")
        for f in self.flags:
            self.text.tag_add("error", f"1.0+{f.start}c", f"1.0+{f.end}c")
            first = f.suggestions[0].text if f.suggestions else "?"
            self.flag_list.insert("end", f"{f.word}  ->  {first}")
        self._show(None)
        words = len([t for t in content.split() if t.strip()])
        self.status.set(f"{len(self.flags)} misspelled word(s) in {words} words  |  "
                        f"threshold {self.checker.threshold:.2f}  |  '{self.lexicon.get()}' "
                        f"Tagalog: {self.model.info.get('tagalog_words', 0):,} words  |  "
                        f"'{self.english.get()}' English: "
                        f"{self.model.info.get('english_words', 0):,} words")

    def _show(self, index: int | None) -> None:
        self.current = index
        self.sugg_list.delete(0, "end")
        self.text.tag_remove("current", "1.0", "end")
        if index is None:
            self.word_label.config(text="")
            self.reason_label.config(text="Click an underlined word." if self.flags else "")
            return
        f = self.flags[index]
        self.text.tag_add("current", f"1.0+{f.start}c", f"1.0+{f.end}c")
        self.text.see(f"1.0+{f.start}c")
        self.word_label.config(text=f.word)
        self.reason_label.config(text=f"{f.method}: {f.detail}")
        for s in f.suggestions:
            edits = f"{s.distance} edit" + ("" if s.distance == 1 else "s")
            extra = f"  (Dice {s.score:.2f}, {edits})" if s.source == "edit-distance" \
                else f"  ({s.source})"
            self.sugg_list.insert("end", s.text + extra)
        if f.suggestions:
            self.sugg_list.selection_set(0)
        self.flag_list.selection_clear(0, "end")
        self.flag_list.selection_set(index)

    def _on_error_click(self, event) -> None:
        offset = self.text.count("1.0", self.text.index(f"@{event.x},{event.y}"), "chars")
        offset = offset[0] if offset else 0
        for i, f in enumerate(self.flags):
            if f.start <= offset < f.end:
                self._show(i)
                break

    def _on_flag_select(self, _event) -> None:
        sel = self.flag_list.curselection()
        if sel:
            self._show(sel[0])

    def replace(self) -> None:
        if self.current is None:
            return
        f = self.flags[self.current]
        sel = self.sugg_list.curselection()
        if not sel or not f.suggestions:
            return
        s = f.suggestions[sel[0]]
        end = s.end if s.end is not None else f.end
        self.text.delete(f"1.0+{f.start}c", f"1.0+{end}c")
        self.text.insert(f"1.0+{f.start}c", s.text)
        self.check()

    def ignore(self) -> None:
        if self.current is not None:
            self.ignored.add(self.flags[self.current].word.lower())
            self.check()

    def open_file(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if path:
            with open(path, encoding="utf-8", errors="replace") as fh:
                self.text.delete("1.0", "end")
                self.text.insert("1.0", fh.read())
            self.check()

    def clear(self) -> None:
        self.text.delete("1.0", "end")
        self.check()


def main(lexicon: str | None = None, english: str | None = None) -> None:
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)   # crisp text on high-DPI Windows screens
    except Exception:
        pass
    root = tk.Tk()
    SpellCheckerApp(root, lexicon, english)
    root.mainloop()


if __name__ == "__main__":
    main()
