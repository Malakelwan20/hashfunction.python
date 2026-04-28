import hashlib
import tkinter as tk
import math
from tkinter import filedialog, messagebox

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# ── COLORS ─────────────────────────────────────────
BG = "#1e1e2e"
CARD = "#13131f"
ACCENT = "#7c6af7"
GREEN = "#4ade80"
YELLOW = "#fbbf24"
RED = "#f87171"
CYAN = "#4ecdc4"
WHITE = "#ffffff"


# ── HASH FUNCTION ─────────────────────────────────
def generate_hash(text, algo):
    data = text.encode()

    if algo == "MD5":
        return hashlib.md5(data).hexdigest()
    elif algo == "SHA-1":
        return hashlib.sha1(data).hexdigest()
    elif algo == "SHA-256":
        return hashlib.sha256(data).hexdigest()
    elif algo == "SHA-512":
        return hashlib.sha512(data).hexdigest()


# ── ENTROPY FUNCTION ──────────────────────────────
def entropy(hash_value):
    freq = {}
    for c in hash_value:
        freq[c] = freq.get(c, 0) + 1

    total = len(hash_value)
    e = -sum((f / total) * math.log2(f / total) for f in freq.values())
    return e, freq


# ── APP ────────────────────────────────────────────
class HashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hash Security Analyzer Pro")
        self.root.geometry("1000x950")
        self.root.configure(bg=BG)

        self.last_data = {}

        # scroll system
        self.canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(root, command=self.canvas.yview)
        self.frame = tk.Frame(self.canvas, bg=BG)

        self.frame.bind("<Configure>", lambda e:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.build_ui()

    # ── UI ─────────────────────────────────────────
    def build_ui(self):
        tk.Label(
            self.frame,
            text="🔐 HASH SECURITY ANALYZER DASHBOARD",
            bg=ACCENT,
            fg=WHITE,
            font=("Consolas", 18, "bold"),
            pady=15
        ).pack(fill="x")

        box = tk.Frame(self.frame, bg=BG, padx=25, pady=15)
        box.pack(fill="x")

        tk.Label(box, text="Input Text:", bg=BG, fg=WHITE,
                 font=("Consolas", 12, "bold")).pack(anchor="w")

        self.input_box = tk.Text(
            box,
            height=4,
            bg=CARD,
            fg=WHITE,
            font=("Consolas", 12),
            insertbackground="white",
            bd=0
        )
        self.input_box.pack(fill="x", pady=10)
        self.input_box.insert("1.0", "Security Engineering 2026")

        self.input_box.bind("<KeyRelease>", lambda e: self.analyze())

        tk.Button(
            box,
            text="⚡ Analyze",
            command=self.analyze,
            bg=ACCENT,
            fg=WHITE,
            font=("Consolas", 12, "bold"),
            bd=0,
            pady=8
        ).pack(fill="x", pady=5)

        tk.Button(
            box,
            text="📄 Export PDF Report",
            command=self.export_pdf,
            bg=CYAN,
            fg="black",
            font=("Consolas", 12, "bold"),
            bd=0,
            pady=8
        ).pack(fill="x")

        self.results = tk.Frame(self.frame, bg=BG, padx=25)
        self.results.pack(fill="both", expand=True)

        self.analyze()

    # ── CARD ───────────────────────────────────────
    def card(self, title):
        c = tk.LabelFrame(
            self.results,
            text=" " + title + " ",
            bg=CARD,
            fg=ACCENT,
            font=("Consolas", 12, "bold"),
            padx=10,
            pady=10
        )
        c.pack(fill="x", pady=8)
        return c

    # ── ANALYZE ────────────────────────────────────
    def analyze(self):
        for w in self.results.winfo_children():
            w.destroy()

        text = self.input_box.get("1.0", "end-1c")
        if not text.strip():
            return

        hashes = {
            "MD5": generate_hash(text, "MD5"),
            "SHA-1": generate_hash(text, "SHA-1"),
            "SHA-256": generate_hash(text, "SHA-256"),
            "SHA-512": generate_hash(text, "SHA-512"),
        }

        self.last_data = {
            "input": text,
            "hashes": hashes
        }

        # ── GENERATED HASHES ──
        c = self.card("GENERATED HASHES")
        for k, v in hashes.items():
            tk.Label(c, text=f"{k}: {v}", bg=CARD, fg=WHITE,
                     font=("Consolas", 10)).pack(anchor="w")

        # ── COMPARISON TABLE ──
        c = self.card("COMPARISON TABLE")
        table = [
            ("MD5", "128-bit", "BROKEN", RED),
            ("SHA-1", "160-bit", "WEAK", YELLOW),
            ("SHA-256", "256-bit", "SECURE", GREEN),
            ("SHA-512", "512-bit", "STRONG", CYAN),
        ]

        for n, b, s, col in table:
            tk.Label(c, text=f"{n:8} | {b:7} | {s}",
                     bg=CARD, fg=col, font=("Consolas", 10)).pack(anchor="w")

        # ── AVALANCHE EFFECT ──
        c = self.card("AVALANCHE EFFECT DEMO")
        mod = text[:-1] + "X" if len(text) > 0 else "A"

        tk.Label(c, text=f"Original: {text}", bg=CARD, fg=WHITE).pack(anchor="w")
        tk.Label(c, text=f"Modified: {mod}", bg=CARD, fg=ACCENT).pack(anchor="w")
        tk.Label(c, text="Small change → completely different hash",
                 bg=CARD, fg=RED).pack(anchor="w")

        # ── SECURITY ANALYSIS ──
        c = self.card("SECURITY ANALYSIS")
        for t, col in [
            ("MD5 → Collision attacks", RED),
            ("SHA-1 → Deprecated", YELLOW),
            ("SHA-256 → Industry standard", GREEN),
            ("SHA-512 → High security", CYAN),
        ]:
            tk.Label(c, text=t, bg=CARD, fg=col).pack(anchor="w")

        # ── FINAL VERDICT ──
        c = self.card("FINAL VERDICT")
        tk.Label(c, text="❌ Avoid MD5 & SHA-1", bg=CARD, fg=RED).pack(anchor="w")
        tk.Label(c, text="✔ Use SHA-256 / SHA-512", bg=CARD, fg=GREEN).pack(anchor="w")

        # ── ENTROPY & FINGERPRINT SCORE ──
        c = self.card("ENTROPY & FINGERPRINT SCORE")

        for name, h in hashes.items():
            e, freq = entropy(h)

            score = min(10, (e / 4.0) * 10)
            bar = "█" * int(score) + "░" * (10 - int(score))

            tk.Label(
                c,
                text=f"{name:<7} [{bar}] {score:.1f}/10",
                bg=CARD,
                fg=WHITE,
                font=("Consolas", 11, "bold")
            ).pack(anchor="w")

            # ── DETAILED FINGERPRINT ──
            tk.Label(
                c,
                text="Fingerprint breakdown:",
                bg=CARD,
                fg=ACCENT,
                font=("Consolas", 10, "bold")
            ).pack(anchor="w")

            for char, count in sorted(freq.items()):
                tk.Label(
                    c,
                    text=f"   {char} → {count} time(s)",
                    bg=CARD,
                    fg=GREEN,
                    font=("Consolas", 9)
                ).pack(anchor="w")

            tk.Label(c, text="─" * 60, bg=CARD, fg=WHITE).pack(anchor="w")

    # ── EXPORT PDF ────────────────────────────────
    def export_pdf(self):
        if not self.last_data:
            messagebox.showwarning("Warning", "Run analysis first")
            return

        path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not path:
            return

        try:
            c = canvas.Canvas(path, pagesize=A4)
            y = 800

            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, "HASH SECURITY REPORT")
            y -= 40

            c.setFont("Helvetica", 11)
            c.drawString(50, y, f"Input: {self.last_data['input']}")
            y -= 30

            for k, v in self.last_data["hashes"].items():
                c.drawString(50, y, f"{k}: {v}")
                y -= 20

            c.save()
            messagebox.showinfo("Success", "PDF exported successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))


# ── RUN ───────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = HashApp(root)
    root.mainloop()