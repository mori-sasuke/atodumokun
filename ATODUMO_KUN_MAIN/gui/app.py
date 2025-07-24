import tkinter as tk
from tkinter import ttk, messagebox
from logic.ahp import AHPAnalyzer
from utils.data_handler import save_record, load_records
from datetime import datetime

class AtodumoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("後ヅモ君")
        self.root.geometry("480x600")

        self._build_ui()
        self.analyzer = AHPAnalyzer({
            'grape': 0.4,
            'reg': 0.3,
            'spins': 0.2,
            'tokubi': 0.1
        })

    def _build_ui(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.pack(fill="x")

        self.inputs = {}
        for label, key in [
            ("BIG回数", "big"),
            ("REG回数", "reg"),
            ("総回転数", "spins"),
            ("差枚数", "diff")
        ]:
            row = ttk.Frame(frm)
            row.pack(fill="x", pady=2)
            ttk.Label(row, text=label, width=12).pack(side="left")
            ent = ttk.Entry(row)
            ent.pack(side="right", fill="x", expand=True)
            self.inputs[key] = ent

        self.tokubi = tk.BooleanVar()
        ttk.Checkbutton(frm, text="特定日である", variable=self.tokubi).pack(anchor="w", pady=5)

        ttk.Button(frm, text="評価する", command=self.evaluate).pack(pady=10)

        self.result_label = ttk.Label(self.root, text="結果がここに表示されます", font=("Meiryo", 12), padding=10)
        self.result_label.pack()

        ttk.Label(self.root, text="履歴", font=("Meiryo", 10, "bold")).pack()
        self.history = tk.Text(self.root, height=15, wrap="word", state="disabled")
        self.history.pack(fill="both", padx=10, pady=5, expand=True)

        self._load_history()

    def evaluate(self):
        try:
            big = int(self.inputs["big"].get())
            reg = int(self.inputs["reg"].get())
            spins = int(self.inputs["spins"].get())
            diff = int(self.inputs["diff"].get())
            tokubi = self.tokubi.get()

            in_medals = big * 312 + reg * 112 - diff
            grape = in_medals / spins if spins else 0
            reg_prob = spins / reg if reg else 9999

            data = {
                "grape": grape,
                "reg": reg_prob,
                "spins": spins,
                "tokubi": tokubi
            }

            result = self.analyzer.evaluate(data)
            self.result_label.config(text=result["result_text"])

            record = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                **{str(k): {"confidence": v} for k, v in result["setting_scores"].items()}
            }
            save_record(record)
            self._load_history()

        except Exception as e:
            messagebox.showerror("エラー", str(e))

    def _load_history(self):
        self.history.config(state="normal")
        self.history.delete("1.0", "end")
        for record in load_records():
            self.history.insert("end", f"[{record.get('timestamp', '?')}]\n")
            for k in range(1, 7):
                score = record.get(str(k), {}).get("confidence")
                if score is not None:
                    self.history.insert("end", f"  設定{k}: {score}%\n")
            self.history.insert("end", "\n")
        self.history.config(state="disabled")
