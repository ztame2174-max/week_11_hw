import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class RegexTextGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RE Module Text Processor")
        self.root.geometry("900x650")
        self.root.resizable(True, True)

        self.make_gui()

    def make_gui(self):
        # Main border/frame - similar to the requested drawing
        main = tk.Frame(self.root, bd=2, relief="solid", padx=28, pady=20)
        main.pack(fill="both", expand=True, padx=35, pady=30)

        # INPUT
        tk.Label(main, text="INPUT", font=("Arial", 15, "bold")).pack(anchor="w")

        input_frame = tk.Frame(main)
        input_frame.pack(fill="both", expand=True, pady=(5, 12))

        self.input_box = tk.Text(
            input_frame, height=7, font=("Consolas", 11),
            bd=2, relief="solid", wrap="word"
        )
        self.input_box.pack(side="left", fill="both", expand=True)

        scroll1 = ttk.Scrollbar(input_frame, command=self.input_box.yview)
        scroll1.pack(side="right", fill="y")
        self.input_box.config(yscrollcommand=scroll1.set)

        # Load/Clear buttons
        tool_frame = tk.Frame(main)
        tool_frame.pack(fill="x", pady=(0, 8))

        ttk.Button(tool_frame, text="Load Text", command=self.load_text).pack(
            side="left", padx=(0, 5)
        )
        ttk.Button(tool_frame, text="Clear", command=self.clear_all).pack(side="left")

        # PARAMETERS
        parameter_frame = tk.LabelFrame(
            main, text="Parameters", padx=8, pady=7
        )
        parameter_frame.pack(fill="x", pady=5)

        tk.Label(parameter_frame, text="Pattern:").grid(row=0, column=0, sticky="w")
        self.pattern_var = tk.StringVar(value=r"\d+")
        tk.Entry(
            parameter_frame, textvariable=self.pattern_var, width=42
        ).grid(row=0, column=1, padx=5, sticky="ew")

        tk.Label(parameter_frame, text="Replace:").grid(row=0, column=2, sticky="w")
        self.replace_var = tk.StringVar(value="[REPLACED]")
        tk.Entry(
            parameter_frame, textvariable=self.replace_var, width=20
        ).grid(row=0, column=3, padx=5, sticky="ew")

        tk.Label(parameter_frame, text="Flags:").grid(row=0, column=4, sticky="w")
        self.flags_var = tk.StringVar(value="")
        tk.Entry(
            parameter_frame, textvariable=self.flags_var, width=18
        ).grid(row=0, column=5, padx=5, sticky="ew")

        tk.Label(
            parameter_frame,
            text="Flags: IGNORECASE, MULTILINE, DOTALL, ASCII, VERBOSE"
        ).grid(row=1, column=0, columnspan=6, sticky="w", pady=(5, 0))

        parameter_frame.columnconfigure(1, weight=1)
        parameter_frame.columnconfigure(3, weight=1)

        # OUTPUT
        tk.Label(main, text="OUTPUT", font=("Arial", 15, "bold")).pack(anchor="w")

        output_frame = tk.Frame(main)
        output_frame.pack(fill="both", expand=True, pady=(5, 12))

        self.output_box = tk.Text(
            output_frame, height=7, font=("Consolas", 11),
            bd=2, relief="solid", wrap="word"
        )
        self.output_box.pack(side="left", fill="both", expand=True)

        scroll2 = ttk.Scrollbar(output_frame, command=self.output_box.yview)
        scroll2.pack(side="right", fill="y")
        self.output_box.config(yscrollcommand=scroll2.set)

        # 10 functions: 5 columns x 2 rows
        button_frame = tk.Frame(main)
        button_frame.pack(fill="x", pady=4)

        buttons = [
            ("f1\nfindall", self.f1_findall),
            ("f2\nsearch", self.f2_search),
            ("f3\nmatch", self.f3_match),
            ("f4\nfullmatch", self.f4_fullmatch),
            ("f5\nsplit", self.f5_split),
            ("f6\nsub", self.f6_sub),
            ("f7\nsubn", self.f7_subn),
            ("f8\nfinditer", self.f8_finditer),
            ("f9\nescape", self.f9_escape),
            ("f10\ncompile", self.f10_compile),
        ]

        for i, (text, command) in enumerate(buttons):
            row = i // 5
            col = i % 5

            b = tk.Button(
                button_frame,
                text=text,
                command=command,
                width=11,
                height=2,
                font=("Arial", 10, "bold")
            )
            b.grid(row=row, column=col, padx=4, pady=4, sticky="ew")
            button_frame.columnconfigure(col, weight=1)

        self.status = tk.StringVar(value="Ready")
        tk.Label(main, textvariable=self.status, anchor="w").pack(fill="x")

    # -------------------- Helpers --------------------

    def get_input(self):
        text = self.input_box.get("1.0", "end-1c")
        if not text.strip():
            raise ValueError("Please enter or load text first.")
        return text

    def get_pattern(self):
        pattern = self.pattern_var.get()
        if pattern == "":
            raise ValueError("Pattern cannot be empty.")
        return pattern

    def get_flags(self):
        """Convert text flags entered by the user to re module flags."""
        flag_map = {
            "IGNORECASE": re.IGNORECASE, "I": re.IGNORECASE,
            "MULTILINE": re.MULTILINE, "M": re.MULTILINE,
            "DOTALL": re.DOTALL, "S": re.DOTALL,
            "ASCII": re.ASCII, "A": re.ASCII,
            "VERBOSE": re.VERBOSE, "X": re.VERBOSE
        }

        flags = 0
        value = self.flags_var.get().strip()

        if not value:
            return flags

        for item in value.replace("|", ",").split(","):
            name = item.strip().upper()
            if name:
                if name not in flag_map:
                    raise ValueError("Unknown flag: " + name)
                flags |= flag_map[name]

        return flags

    def result(self, text, status):
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", text)
        self.status.set(status)

    def safe(self, operation):
        # Required try-except error handling
        try:
            operation()
        except re.error as error:
            messagebox.showerror(
                "Regular Expression Error",
                "Invalid pattern:\n" + str(error)
            )
            self.status.set("Regex Error")
        except ValueError as error:
            messagebox.showwarning("Input Error", str(error))
            self.status.set("Input Error")
        except Exception as error:
            messagebox.showerror(
                "Error",
                type(error).__name__ + ": " + str(error)
            )
            self.status.set("Error")

    # -------------------- 10 re functions --------------------

    def f1_findall(self):
        def work():
            text = self.get_input()
            pattern = self.get_pattern()
            matches = re.findall(pattern, text, self.get_flags())

            self.result(
                "re.findall()\n\n"
                f"Number of matches: {len(matches)}\n\n"
                f"{matches}",
                "f1 findall completed"
            )
        self.safe(work)

    def f2_search(self):
        def work():
            text = self.get_input()
            pattern = self.get_pattern()
            m = re.search(pattern, text, self.get_flags())

            if m:
                answer = (
                    "re.search()\n\n"
                    f"Match: {m.group()}\n"
                    f"Start: {m.start()}\n"
                    f"End: {m.end()}\n"
                    f"Span: {m.span()}"
                )
            else:
                answer = "re.search()\n\nNo match found."

            self.result(answer, "f2 search completed")
        self.safe(work)

    def f3_match(self):
        def work():
            text = self.get_input()
            pattern = self.get_pattern()
            m = re.match(pattern, text, self.get_flags())

            if m:
                answer = (
                    "re.match()\n\n"
                    f"Match at beginning: {m.group()}\n"
                    f"Span: {m.span()}"
                )
            else:
                answer = "re.match()\n\nNo match at the beginning."

            self.result(answer, "f3 match completed")
        self.safe(work)

    def f4_fullmatch(self):
        def work():
            text = self.get_input()
            pattern = self.get_pattern()
            m = re.fullmatch(pattern, text, self.get_flags())

            answer = (
                "re.fullmatch()\n\n"
                + ("Entire text matches the pattern." if m
                   else "Entire text does NOT match the pattern.")
            )

            self.result(answer, "f4 fullmatch completed")
        self.safe(work)

    def f5_split(self):
        def work():
            text = self.get_input()
            pattern = self.get_pattern()
            parts = re.split(pattern, text, flags=self.get_flags())

            lines = [f"[{i}] {part}" for i, part in enumerate(parts)]
            self.result(
                "re.split()\n\n" + "\n".join(lines),
                "f5 split completed"
            )
        self.safe(work)

    def f6_sub(self):
        def work():
            text = self.get_input()
            pattern = self.get_pattern()
            replacement = self.replace_var.get()

            answer = re.sub(
                pattern, replacement, text, flags=self.get_flags()
            )

            self.result(
                "re.sub()\n\n" + answer,
                "f6 sub completed"
            )
        self.safe(work)

    def f7_subn(self):
        def work():
            text = self.get_input()
            pattern = self.get_pattern()
            replacement = self.replace_var.get()

            answer, count = re.subn(
                pattern, replacement, text, flags=self.get_flags()
            )

            self.result(
                "re.subn()\n\n"
                f"Replacement count: {count}\n\n{answer}",
                "f7 subn completed"
            )
        self.safe(work)

    def f8_finditer(self):
        def work():
            text = self.get_input()
            pattern = self.get_pattern()

            matches = list(re.finditer(
                pattern, text, self.get_flags()
            ))

            if not matches:
                answer = "re.finditer()\n\nNo match found."
            else:
                lines = []
                for i, m in enumerate(matches, 1):
                    lines.append(
                        f"{i}. {m.group()}   position={m.span()}"
                    )
                answer = (
                    "re.finditer()\n\n"
                    f"Number of matches: {len(matches)}\n\n"
                    + "\n".join(lines)
                )

            self.result(answer, "f8 finditer completed")
        self.safe(work)

    def f9_escape(self):
        def work():
            pattern = self.get_pattern()
            escaped = re.escape(pattern)

            self.result(
                "re.escape()\n\n"
                f"Original:\n{pattern}\n\n"
                f"Escaped:\n{escaped}",
                "f9 escape completed"
            )
        self.safe(work)

    def f10_compile(self):
        def work():
            text = self.get_input()
            pattern = self.get_pattern()

            regex = re.compile(pattern, self.get_flags())
            matches = regex.findall(text)

            self.result(
                "re.compile()\n\n"
                f"Compiled pattern: {regex.pattern}\n"
                f"Number of matches: {len(matches)}\n\n"
                f"{matches}",
                "f10 compile completed"
            )
        self.safe(work)

    # -------------------- File functions --------------------

    def load_text(self):
        try:
            path = filedialog.askopenfilename(
                title="Load Text File",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("Python files", "*.py"),
                    ("All files", "*.*")
                ]
            )

            if not path:
                return

            with open(path, "r", encoding="utf-8") as file:
                text = file.read()

            self.input_box.delete("1.0", "end")
            self.input_box.insert("1.0", text)
            self.status.set("Loaded: " + path)

        except UnicodeDecodeError:
            messagebox.showerror(
                "File Error",
                "The file is not UTF-8 encoded."
            )
        except Exception as error:
            messagebox.showerror(
                "File Error",
                type(error).__name__ + ": " + str(error)
            )

    def clear_all(self):
        self.input_box.delete("1.0", "end")
        self.output_box.delete("1.0", "end")
        self.status.set("Ready")


if __name__ == "__main__":
    root = tk.Tk()
    app = RegexTextGUI(root)
    root.mainloop()