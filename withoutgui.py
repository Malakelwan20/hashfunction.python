import hashlib
import math

# ── HASH FUNCTIONS ────────────────────────────────
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


# ── ENTROPY CALCULATION ────────────────────────────
def calc_entropy(hex_str):
    freq = {c: hex_str.count(c) for c in "0123456789abcdef"}
    total = len(hex_str)

    entropy = -sum(
        (f / total) * math.log2(f / total)
        for f in freq.values()
        if f > 0
    )

    return entropy, freq


# ── DISPLAY FINGERPRINT ────────────────────────────
def print_fingerprint(name, freq_map):
    max_freq = max(freq_map.values())

    print("\nFingerprint Distribution:")
    for k, v in freq_map.items():
        bar = "█" * int((v / max_freq) * 30)
        print(f"{k} : {bar} ({v})")


# ── ANALYSIS ENGINE ────────────────────────────────
def analyze(text):

    print("\n" + "=" * 70)
    print("🔐 HASH SECURITY ANALYZER (NO GUI VERSION)")
    print("=" * 70)

    # ── Generate hashes ──
    md5_h = generate_hash(text, "MD5")
    sha1_h = generate_hash(text, "SHA-1")
    sha256_h = generate_hash(text, "SHA-256")
    sha512_h = generate_hash(text, "SHA-512")

    hashes = {
        "MD5": md5_h,
        "SHA-1": sha1_h,
        "SHA-256": sha256_h,
        "SHA-512": sha512_h
    }

    # ── 1. HASHES ──
    print("\n📌 GENERATED HASHES")
    for k, v in hashes.items():
        print(f"{k}: {v}")

    # ── 2. COMPARISON TABLE ──
    print("\n📊 COMPARISON TABLE")
    print("ALGO     | BITS   | STATUS")
    print("-" * 40)
    print("MD5      | 128    | BROKEN")
    print("SHA-1    | 160    | WEAK")
    print("SHA-256  | 256    | SECURE")
    print("SHA-512  | 512    | MILITARY")

    # ── 3. AVALANCHE EFFECT ──
    print("\n⚡ AVALANCHE EFFECT")

    changed_text = text[:-1] + (chr(ord(text[-1]) + 1) if text else "A")

    original = generate_hash(text, "MD5")
    modified = generate_hash(changed_text, "MD5")

    print(f"Original text : {text}")
    print(f"Modified text : {changed_text}")
    print(f"MD5 original  : {original}")
    print(f"MD5 modified  : {modified}")
    print("→ Tiny change completely changes hash output")

    # ── 4. SECURITY ANALYSIS ──
    print("\n🛡 SECURITY ANALYSIS")
    print("MD5    → Collision-prone, broken")
    print("SHA-1  → Deprecated, vulnerable")
    print("SHA-2  → Secure standard (industry use)")

    print("\n🔐 FINAL VERDICT")
    print("❌ Avoid MD5 & SHA-1")
    print("✅ Use SHA-256 / SHA-512")
    print("🔑 Passwords → use Argon2 / BCrypt")

    # ── 5. ENTROPY + FINGERPRINT FOR ALL HASHES ──
    print("\n📈 HASH ENTROPY & FINGERPRINT ANALYSIS")

    for name, h in hashes.items():

        entropy, freq = calc_entropy(h)

        print("\n" + "-" * 50)
        print(f"{name} → Entropy Score: {entropy:.4f}")

        print_fingerprint(name, freq)

        if entropy > 3.8:
            print("🟢 HIGH ENTROPY → Strong randomness")
        elif entropy > 3.4:
            print("🟡 MEDIUM ENTROPY → Acceptable randomness")
        else:
            print("🔴 LOW ENTROPY → Weak pattern risk")


# ── RUN PROGRAM ───────────────────────────────────
if __name__ == "__main__":
    user_input = input("Enter text to analyze: ")
    analyze(user_input)