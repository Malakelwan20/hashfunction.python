import hashlib
import math
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


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


# ── ANALYSIS ENGINE ───────────────────────────────
class HashAnalyzer:

    def __init__(self, text):
        self.text = text
        self.hashes = {}
        self.results = {}

    def run(self):
        self.hashes = {
            "MD5": generate_hash(self.text, "MD5"),
            "SHA-1": generate_hash(self.text, "SHA-1"),
            "SHA-256": generate_hash(self.text, "SHA-256"),
            "SHA-512": generate_hash(self.text, "SHA-512"),
        }

        self.results = {
            "comparison": [
                ("MD5", "128-bit", "BROKEN"),
                ("SHA-1", "160-bit", "WEAK"),
                ("SHA-256", "256-bit", "SECURE"),
                ("SHA-512", "512-bit", "STRONG"),
            ],
            "avalanche": {
                "original": self.text,
                "modified": self.text[:-1] + "X" if self.text else "A"
            },
            "security": [
                "MD5 → Collision attacks",
                "SHA-1 → Deprecated",
                "SHA-256 → Industry standard",
                "SHA-512 → High security",
            ],
            "entropy": {}
        }

        for name, h in self.hashes.items():
            e, freq = entropy(h)
            self.results["entropy"][name] = {
                "score": min(10, (e / 4.0) * 10),
                "freq": freq
            }

    # ── CONSOLE OUTPUT ───────────────────────────
    def display(self):
        print("\n🔐 HASH SECURITY ANALYSIS REPORT\n")

        print("GENERATED HASHES")
        for k, v in self.hashes.items():
            print(f"{k}: {v}")

        print("\nCOMPARISON TABLE")
        for n, b, s in self.results["comparison"]:
            print(f"{n:8} | {b:7} | {s}")

        print("\nAVALANCHE EFFECT")
        print("Original:", self.results["avalanche"]["original"])
        print("Modified:", self.results["avalanche"]["modified"])
        print("Small change → completely different hash")

        print("\nSECURITY ANALYSIS")
        for s in self.results["security"]:
            print(s)

        print("\nENTROPY & FINGERPRINT SCORE")

        for name, data in self.results["entropy"].items():
            score = data["score"]
            freq = data["freq"]

            bar = "█" * int(score) + "░" * (10 - int(score))

            print(f"\n{name} [{bar}] {score:.1f}/10")

            print("Fingerprint breakdown:")
            for char, count in sorted(freq.items()):
                print(f"  {char} → {count} time(s)")

    # ── PDF EXPORT ───────────────────────────────
    def export_pdf(self, path):
        c = canvas.Canvas(path, pagesize=A4)
        y = 800

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "HASH SECURITY REPORT")
        y -= 40

        c.setFont("Helvetica", 11)
        c.drawString(50, y, f"Input: {self.text}")
        y -= 30

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Generated Hashes")
        y -= 20

        for k, v in self.hashes.items():
            c.drawString(50, y, f"{k}: {v}")
            y -= 20

        y -= 10
        c.drawString(50, y, "Security Summary")
        y -= 20

        for s in self.results["security"]:
            c.drawString(50, y, s)
            y -= 18

        c.save()
        print("\nPDF exported successfully!")


# ── RUN PROGRAM ───────────────────────────────────
if __name__ == "__main__":
    text = input("Enter text to analyze: ")

    analyzer = HashAnalyzer(text)
    analyzer.run()
    analyzer.display()

    choice = input("\nExport PDF? (y/n): ")

    if choice.lower() == "y":
        path = input("Enter file name (e.g. report.pdf): ")
        analyzer.export_pdf(path)