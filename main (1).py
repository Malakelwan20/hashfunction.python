import hashlib
import tkinter as tk
from tkinter import font
import math

# ── Colors & Styling ────────────────────────────────
BG = "#1e1e2e"
CARD = "#13131f"
ACCENT = "#7c6af7"
GREEN = "#4ade80"
YELLOW = "#fbbf24"
RED = "#f87171"
CYAN = "#4ecdc4"
WHITE = "#ffffff"
BORDER = "#2a2a3a"

# ── Hash Function Logic ────────────────────────────
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

# ── Main App ───────────────────────────────────────
class HashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hash Security Analyzer Pro")
        self.root.geometry("950x900")
        self.root.configure(bg=BG)

        self.canvas = tk.Canvas(self.root, bg=BG, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.build_ui()

    # ── UI ────────────────────────────────
    def build_ui(self):
        header = tk.Label(
            self.scrollable_frame,
            text="🔐 Hash Generator & Security Analyzer",
            bg=ACCENT,
            fg=WHITE,
            font=("Consolas", 20, "bold"),
            pady=20
        )
        header.pack(fill="x")

        input_container = tk.Frame(self.scrollable_frame, bg=BG, padx=30, pady=20)
        input_container.pack(fill="x")

        tk.Label(
            input_container,
            text="Input Data:",
            bg=BG,
            fg=WHITE,
            font=("Consolas", 12, "bold")
        ).pack(anchor="w")

        self.input_box = tk.Text(
            input_container,
            height=3,
            font=("Consolas", 12),
            bg=CARD,
            fg=WHITE,
            insertbackground="white",
            bd=0,
            padx=10,
            pady=10
        )
        self.input_box.pack(fill="x", pady=(5, 15))
        self.input_box.insert("1.0", "Security Engineering 2026")

        tk.Button(
            input_container,
            text="⚡ ANALYZE CRYPTOGRAPHIC STRENGTH",
            command=self.analyze,
            bg=ACCENT,
            fg=WHITE,
            font=("Consolas", 12, "bold"),
            cursor="hand2",
            bd=0,
            pady=10
        ).pack(fill="x")

        self.results_area = tk.Frame(self.scrollable_frame, bg=BG, padx=30)
        self.results_area.pack(fill="both", expand=True)

    # ── Cards ────────────────────────────────
    def create_card(self, title):
        card = tk.LabelFrame(
            self.results_area,
            text=f" {title} ",
            bg=CARD,
            fg=ACCENT,
            font=("Consolas", 12, "bold"),
            bd=1,
            relief="flat",
            padx=15,
            pady=15
        )
        card.pack(fill="x", pady=10)
        return card

    def write_line(self, parent, text, color=WHITE, bullet=False):
        prefix = " • " if bullet else ""
        tk.Label(
            parent,
            text=f"{prefix}{text}",
            bg=CARD,
            fg=color,
            font=("Consolas", 10),
            anchor="w",
            justify="left"
        ).pack(fill="x")

    # ── Entropy Function ────────────────────────────────
    def calc_entropy(self, hex_str):
        freq = {c: hex_str.count(c) for c in "0123456789abcdef"}
        total = len(hex_str)
        e = -sum((f/total) * math.log2(f/total) for f in freq.values() if f > 0)
        return e, freq

    # ── Main Analysis ────────────────────────────────
    def analyze(self):
        for widget in self.results_area.winfo_children():
            widget.destroy()

        text = self.input_box.get("1.0", "end-1c")
        if not text:
            return

        md5_h = generate_hash(text, "MD5")
        sha1_h = generate_hash(text, "SHA-1")
        sha256_h = generate_hash(text, "SHA-256")
        sha512_h = generate_hash(text, "SHA-512")

        # ── 1. HASHES ──
        h_card = self.create_card("GENERATED HASHES")
        self.write_line(h_card, f"MD5: {md5_h}", RED)
        self.write_line(h_card, f"SHA-1: {sha1_h}", YELLOW)
        self.write_line(h_card, f"SHA-256: {sha256_h}", GREEN)
        self.write_line(h_card, f"SHA-512: {sha512_h}", CYAN)

        # ── 2. COMPARISON ──
        c_card = self.create_card("COMPARISON TABLE")
        self.write_line(c_card, "ALGORITHM | BIT LENGTH | STATUS")
        self.write_line(c_card, "-" * 50)
        self.write_line(c_card, "MD5     | 128-bit | BROKEN", RED)
        self.write_line(c_card, "SHA-1   | 160-bit | WEAK", YELLOW)
        self.write_line(c_card, "SHA-256 | 256-bit | SECURE", GREEN)
        self.write_line(c_card, "SHA-512 | 512-bit | MILITARY", CYAN)

        # ── 3. AVALANCHE ──
        a_card = self.create_card("AVALANCHE EFFECT")
        changed_text = text[:-1] + (chr(ord(text[-1]) + 1) if text else "A")
        changed_md5 = generate_hash(changed_text, "MD5")

        self.write_line(a_card, f"Original: {text}")
        self.write_line(a_card, f"Modified: {changed_text}")
        self.write_line(a_card, f"MD5 Original: {md5_h}")
        self.write_line(a_card, f"MD5 Modified: {changed_md5}")
        self.write_line(a_card, "Tiny change → completely different hash", ACCENT)

        # ── 4. SECURITY ──
        s_card = self.create_card("SECURITY ANALYSIS")
        self.write_line(s_card, "MD5 → Collision-prone", RED, True)
        self.write_line(s_card, "SHA-1 → Deprecated", YELLOW, True)
        self.write_line(s_card, "SHA-256/512 → Industry standard", GREEN, True)

        # ── 5. FINAL VERDICT ──
        v_card = self.create_card("FINAL VERDICT")
        self.write_line(v_card, "Avoid MD5 & SHA-1", RED)
        self.write_line(v_card, "Use SHA-256 / SHA-512", GREEN)
        self.write_line(v_card, "Passwords → Argon2 / BCrypt", ACCENT)

        # ── 6. ENTROPY + FINGERPRINT (ALL HASHES) ──
        e_card = self.create_card("HASH ENTROPY & FINGERPRINT ANALYSIS")

        hashes = {
            "MD5": md5_h,
            "SHA-1": sha1_h,
            "SHA-256": sha256_h,
            "SHA-512": sha512_h
        }

        for name, h in hashes.items():
            e_score, freq_map = self.calc_entropy(h)

            self.write_line(e_card, f"{name} → Entropy: {e_score:.4f}", CYAN)

            bar_frame = tk.Frame(e_card, bg=CARD)
            bar_frame.pack(fill="x", pady=5)

            max_freq = max(freq_map.values())

            for k, v in freq_map.items():
                bar = "█" * int((v / max_freq) * 25)
                self.write_line(bar_frame, f"{k}: {bar} ({v})", ACCENT)

            if e_score > 3.8:
                msg, col = "HIGH ENTROPY → Strong randomness", GREEN
            elif e_score > 3.4:
                msg, col = "MEDIUM ENTROPY → Acceptable", YELLOW
            else:
                msg, col = "LOW ENTROPY → Weak pattern risk", RED

            self.write_line(e_card, msg, col)
            self.write_line(e_card, "─" * 60, WHITE)

# ── RUN APP ───────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = HashApp(root)
    root.mainloop()