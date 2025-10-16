import random, string

# --- Normalization helpers ---
def _to_upper_letters_and_spaces(text: str) -> str:
    return "".join((c.upper() if c.isalpha() else c) for c in text)

# --- Encryptors ---
def caesar_encrypt(text: str, shift: int) -> str:
    out = []
    for ch in _to_upper_letters_and_spaces(text):
        if ch == " ":
            out.append(ch)
        elif ch.isalpha():
            base = ord('A')
            out.append(chr(base + ((ord(ch) - base + shift) % 26)))
        else:
            out.append(ch)
    return "".join(out)

def rot13_encrypt(text: str) -> str:
    return caesar_encrypt(text, 13)

def atbash_encrypt(text: str) -> str:
    out = []
    for ch in _to_upper_letters_and_spaces(text):
        if ch == " ":
            out.append(ch)
        elif ch.isalpha():
            idx = ord(ch) - ord('A')
            out.append(chr(ord('Z') - idx))
        else:
            out.append(ch)
    return "".join(out)

def vigenere_encrypt(text: str, key: str) -> str:
    key = "".join(k for k in key.upper() if k.isalpha())
    if not key:
        return _to_upper_letters_and_spaces(text)
    out = []
    ki = 0
    for ch in _to_upper_letters_and_spaces(text):
        if ch == " ":
            out.append(ch)
        elif ch.isalpha():
            shift = ord(key[ki % len(key)]) - ord('A')
            base = ord('A')
            out.append(chr(base + ((ord(ch) - base + shift) % 26)))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)

def affine_encrypt(text: str, a: int, b: int) -> str:
    out = []
    for ch in _to_upper_letters_and_spaces(text):
        if ch == " ":
            out.append(ch)
        elif ch.isalpha():
            x = ord(ch) - ord('A')
            out.append(chr(ord('A') + ((a * x + b) % 26)))
        else:
            out.append(ch)
    return "".join(out)

def keyword_substitution_encrypt(text: str, keyword: str) -> str:
    seen = set()
    key_clean = []
    for ch in keyword.upper():
        if ch.isalpha() and ch not in seen:
            key_clean.append(ch); seen.add(ch)
    for ch in string.ascii_uppercase:
        if ch not in seen:
            key_clean.append(ch); seen.add(ch)
    subst = key_clean
    out = []
    for ch in _to_upper_letters_and_spaces(text):
        if ch == " ":
            out.append(ch)
        elif ch.isalpha():
            idx = ord(ch) - ord('A')
            out.append(subst[idx])
        else:
            out.append(ch)
    return "".join(out)

def rail_fence_encrypt(text: str, rails: int) -> str:
    if rails <= 1:
        return _to_upper_letters_and_spaces(text)
    text_u = _to_upper_letters_and_spaces(text)
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1
    for ch in text_u:
        fence[rail].append(ch)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    return "".join("".join(row) for row in fence)

def _rank_key_to_permutation(key: str):
    paired = sorted([(ch, i) for i, ch in enumerate(key)], key=lambda x: (x[0], x[1]))
    order = [0] * len(key)
    for rank, (_, original_index) in enumerate(paired):
        order[original_index] = rank
    return order

def columnar_encrypt(text: str, key: str) -> str:
    # Standard columnar transposition: remove spaces, fill rows left-to-right,
    # then read columns in key order; skip empty cells in the last row.
    text_u = _to_upper_letters_and_spaces(text).replace(" ", "")
    cols = len(key)
    if cols <= 1:
        return text_u
    order = _rank_key_to_permutation(key.upper())
    rows = (len(text_u) + cols - 1) // cols
    # No pre-fill; we will only read indices that exist
    ciphertext = []
    for col in sorted(range(cols), key=lambda c: order[c]):
        for row in range(rows):
            idx = row * cols + col
            if idx < len(text_u):
                ciphertext.append(text_u[idx])
    return "".join(ciphertext)

def circular_bit_shift_encrypt(text: str, shift: int, direction: str) -> str:
    direction = direction.lower()
    shift = shift % 8
    out_chars = []
    for ch in text:
        if ch == " ":
            out_chars.append(ch)
            continue
        byte = ord(ch)
        if direction == 'left':
            val = ((byte << shift) & 0xFF) | (byte >> (8 - shift))
        else:  # right
            val = (byte >> shift) | ((byte << (8 - shift)) & 0xFF)
        # Map to uppercase A–Z to avoid non-alphabet characters
        out_chars.append(chr(ord('A') + (val % 26)))
    return "".join(out_chars)

# --- Cipher registry with parameter generators ---

def _gen_none():
    return {}

def _gen_caesar():
    return {"shift": random.randint(1, 25)}

def _gen_vigenere():
    key_len = random.randint(3, 6)
    return {"key": "".join(random.choice(string.ascii_uppercase) for _ in range(key_len))}

def _gen_columnar():
    cols = random.randint(3, 5)
    return {"key": "".join(random.choice(string.ascii_uppercase) for _ in range(cols))}

def _gen_affine():
    coprime_choices = [1,3,5,7,9,11,15,17,19,21,23,25]
    return {"a": random.choice(coprime_choices), "b": random.randint(0, 25)}

def _gen_keyword():
    kw_len = random.randint(4, 7)
    return {"keyword": "".join(random.choice(string.ascii_uppercase) for _ in range(kw_len))}

def _gen_rails():
    return {"rails": random.randint(3, 4)}

def _gen_circular():
    return {"shift": random.randint(1, 7), "direction": random.choice(['left', 'right'])}

CIPHERS = {
    # Easy
    "ROT13": {"difficulty": "easy", "encrypt": lambda t, p: rot13_encrypt(t), "params": _gen_none},
    "Caesar": {"difficulty": "easy", "encrypt": lambda t, p: caesar_encrypt(t, p["shift"]), "params": _gen_caesar},
    "Atbash": {"difficulty": "easy", "encrypt": lambda t, p: atbash_encrypt(t), "params": _gen_none},
    # Medium
    "Rail Fence": {"difficulty": "medium", "encrypt": lambda t, p: rail_fence_encrypt(t, p["rails"]), "params": _gen_rails},
    "Vigenere": {"difficulty": "medium", "encrypt": lambda t, p: vigenere_encrypt(t, p["key"]), "params": _gen_vigenere},
    "Columnar": {"difficulty": "hard", "encrypt": lambda t, p: columnar_encrypt(t, p["key"]), "params": _gen_columnar},
    "Circular Bit Shift": {"difficulty": "medium", "encrypt": lambda t, p: circular_bit_shift_encrypt(t, p["shift"], p["direction"]), "params": _gen_circular},
    # Hard
    "Affine": {"difficulty": "hard", "encrypt": lambda t, p: affine_encrypt(t, p["a"], p["b"]), "params": _gen_affine},
    "Keyword Substitution": {"difficulty": "hard", "encrypt": lambda t, p: keyword_substitution_encrypt(t, p["keyword"]), "params": _gen_keyword},
}

def choose_difficulty_for_level(level: int, easy_levels: int = 1, medium_levels: int = 1) -> str:
    if level <= easy_levels:
        return "easy"
    if level <= easy_levels + medium_levels:
        return "medium"
    return "hard"

def generate_round(plaintext: str, difficulty: str, recent: list | None = None) -> dict:
    pool = [name for name, meta in CIPHERS.items() if meta["difficulty"] == difficulty]
    if recent:
        # avoid immediate repeats of the last 2 in the same difficulty tier when possible
        pool_non_recent = [n for n in pool if n not in recent[-2:]]
        if pool_non_recent:
            pool = pool_non_recent
    name = random.choice(pool)
    meta = CIPHERS[name]
    params = meta["params"]()
    ciphertext = meta["encrypt"](plaintext, params)
    return {
        "ciphertext": ciphertext,
        "plaintext": plaintext,
        "name": name,
        "difficulty": meta["difficulty"],
        "params": params,
    }


def generate_specific_round(plaintext: str, name: str) -> dict:
    meta = CIPHERS[name]
    params = meta["params"]()
    ciphertext = meta["encrypt"](plaintext, params)
    return {
        "ciphertext": ciphertext,
        "plaintext": plaintext,
        "name": name,
        "difficulty": meta["difficulty"],
        "params": params,
    }


