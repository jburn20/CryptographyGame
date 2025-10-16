"""
Author: jburn20
Program that teaches student cryptography
"""
from demos import demo_registry
import random, os, sys, string, time
from ciphers import generate_round, choose_difficulty_for_level, CIPHERS, generate_specific_round

# --- Dev toggle: reveal cipher type during gameplay (set to True for dev/testing) ---
DEV_SHOW_CIPHER = False

# ANSI colors for difficulty
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def _diff_color(difficulty):
    if difficulty == "easy":
        return GREEN
    if difficulty == "medium":
        return YELLOW
    return RED

def intro(level):
    barrier = "************"
    print(barrier)
    print(f"   Level {level}")
    print(barrier)

def _clean_word(text):
    # Allow letters plus spaces only
    return "".join(ch for ch in text if ch.isalpha() or ch == " ")

def random_picker():
    with open(os.path.join(os.path.dirname(__file__), "wordlist.txt"), "r") as f:
        raw = [line.rstrip("\n") for line in f if line.strip()]
    words = [w for w in (_clean_word(x) for x in raw) if w]
    return random.choice(words)

DEV_SHOW_CIPHER = False

def run_level_progression(seed=None, easy_count=1, medium_count=1, total_rounds=3):
    if seed is not None:
        random.seed(seed)
    level = 1
    recent = []
    total_score = 0
    rounds_played = 0
    for _ in range(total_rounds):
        difficulty = choose_difficulty_for_level(level, easy_levels=easy_count, medium_levels=medium_count)
        word = random_picker()
        rnd = generate_round(word, difficulty, recent)
        current_cipher_name = rnd['name']
        # Base points by difficulty
        base_points = 3 if difficulty == "easy" else 5 if difficulty == "medium" else 7
        points = base_points
        revealed = False

        intro(level=str(level))
        while True:
            diff_col = _diff_color(difficulty)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Difficulty: {diff_col}{difficulty.capitalize()}{RESET}")
            if DEV_SHOW_CIPHER or revealed:
                print(f"Cipher: {diff_col}{current_cipher_name}{RESET}")
                if revealed and 'params' in rnd and rnd['params']:
                    # Friendly parameter display
                    pretty = []
                    for k, v in rnd['params'].items():
                        label = k.capitalize()
                        pretty.append(f"{label}: {v}")
                    print(" | ".join(pretty))
            print("CIPHER:", rnd['ciphertext'])
            print(f"Current score: {total_score} | This round: {points}")

            # Help thresholds by difficulty
            help_threshold = 2 if difficulty == "easy" else 3 if difficulty == "medium" else 4
            allow_help = points <= help_threshold
            if allow_help:
                print("[R] Regenerate (same cipher, new word)")
                if not revealed:
                    print("[H] Reveal cipher type and parameters (final hint)")

            ans = input("What is the word?\n").strip()
            normalized_ans = ans.replace(" ", "").upper()
            normalized_plain = rnd["plaintext"].replace(" ", "").upper()

            # Commands
            if allow_help and normalized_ans.lower() in ("r", "regenerate"):
                # regenerate new plaintext and ciphertext with same cipher
                word = random_picker()
                rnd = generate_specific_round(word, current_cipher_name)
                continue
            if allow_help and not revealed and normalized_ans.lower() in ("h", "hint"):
                revealed = True
                continue
            # Dev skip to next level without scoring
            if ans.lower() == "pass":
                rounds_played += 1
                break

            if normalized_ans == normalized_plain:
                # Animate points transfer (<= 0.7s total)
                award = max(points, 0)
                steps = max(award, 1)
                per_step = min(0.06, 0.7 / steps)
                cur_total = total_score
                cur_round = award
                for _ in range(award):
                    cur_total += 1
                    cur_round -= 1
                    sys.stdout.write(f"\rYou win! Awarding: {award} -> Total: {cur_total} | Round left: {cur_round}   ")
                    sys.stdout.flush()
                    time.sleep(0.3)
                print()  # newline after animation
                total_score += award
                rounds_played += 1
                break
            else:
                points -= 1
                if points <= 0:
                    print("Game Over.")
                    print(f"Total points: {total_score}")
                    print(f"Rounds completed: {rounds_played}")
                    retry = input("Try again? [Y/n]: ").strip().lower()
                    if retry in ("", "y", "yes"):
                        # Reset session
                        level = 1
                        total_score = 0
                        rounds_played = 0
                        recent = []
                        print()
                        break
                    else:
                        # Exit entire progression early
                        return

        recent.append(current_cipher_name)
        level += 1

def run_cipher_tester():
    print("\nCipher Tester: Choose any cipher and test with your input.\n")
    names = list(CIPHERS.keys())
    for i, name in enumerate(names, 1):
        print(f"[{i}] {name} ({CIPHERS[name]['difficulty']})")
    print("[0] Back")
    choice = input("Select a cipher: ").strip()
    if choice == "0":
        return
    try:
        idx = int(choice) - 1
        name = names[idx]
    except Exception:
        print("Invalid choice.")
        return
    meta = CIPHERS[name]
    plaintext = input("Enter plaintext (letters and spaces): ").rstrip("\n")
    auto = input("Auto-generate parameters? [Y/n]: ").strip().lower()
    if auto in ("", "y", "yes"):
        params = meta["params"]()
    else:
        params = {}
        if name == "Caesar":
            params["shift"] = int(input("shift (1-25): ") or 3)
        elif name == "Vigenere":
            params["key"] = input("key (A-Z): ").strip().upper() or "KEY"
        elif name == "Columnar":
            params["key"] = input("key (A-Z, length 3-5): ").strip().upper() or "KEY"
        elif name == "Affine":
            params["a"] = int(input("a (coprime to 26): ") or 5)
            params["b"] = int(input("b (0-25): ") or 8)
        elif name == "Keyword Substitution":
            params["keyword"] = input("keyword (A-Z): ").strip().upper() or "KEYWORD"
        elif name == "Rail Fence":
            params["rails"] = int(input("rails (2-5): ") or 3)
        elif name == "Circular Bit Shift":
            params["shift"] = int(input("shift (1-7): ") or 3)
            params["direction"] = (input("direction [left/right]: ") or "left").strip().lower()
        else:
            # ROT13, Atbash: no params
            params = {}
    ciphertext = meta["encrypt"](plaintext, params)
    print("\nResult:")
    print("Cipher:", name)
    print("Plain :", plaintext)
    print("Params:", params)
    print("Cipher:", ciphertext)
def run_demos():
    while True:
        print("\nAvailable Demos:")
        for i, name in enumerate(demo_registry.keys(), 1):
            print(f"[{i}] {name}")
        print("[0] Quit")

        choice = input("Select a demo: ").strip()
        if choice == "0":
            print("Quitting game, goodbye.")
            sys.exit()

        try:
            choice = int(choice)
            demo_name = list(demo_registry.keys())[choice - 1]
            print(f"\n--- Running {demo_name} ---\n")

            try:
                demo_registry[demo_name]()  # Run the selected demo
            except Exception as e:
                print(f"Error while running {demo_name}: {e}")

            print("\n--- Demo finished ---\n")

        except (ValueError, IndexError):
            print("Invalid choice, please try again.")

def run_demo(file_name):
    # Execute the demo file
    path = os.path.join('demos', file_name)
    with open(path) as f:
        code = f.read()
        exec(code, globals())


def caesar():
    intro(level="1")
    shift = random.randint(1,25)
    word = random_picker() 
    new = []
    for i in word:
        if i == " ":
            newchar = i
            new.append(newchar)
        elif ord(i) + shift >= 123: 
            diff = (ord(i) + shift) - 123 #* handles non alphabetical ord
            newchar = 97 + diff #* 97 = a in ord() form, serves as reset if we go past z
            new.append(chr(newchar))
        else: 
            newchar = ord(i) + shift #* normal shifting
            new.append(chr(newchar)) #* convert num to char, append char to new
    print("CIPHER:","".join(new)) #* turn list into string
    ans = input("What is the word?\n").strip()
    while ans != word:
        ans = input("Incorrect. Try again: ")
    print(f"You win! That was a caesar cipher with a shift of {shift}. Nice work!")
    
def rotThirteen():
    intro(level="2")
    shift = 13
    word = random_picker()
    new = []
    for i in word:
        if i == " ":
            
            new.append(i)
        elif ord(i) + shift >= 123:
            diff = (ord(i) + shift) - 123
            newchar = 97 + diff
            new.append((chr(newchar)))
        else:
            newchar = ord(i) + shift
            new.append((chr(newchar)))
    print("CIPHER:","".join(new))
    ans = input("What is the word?\n").strip()
    while ans != word:
        ans = input("Incorrect. Please try again: ")
    print("You win! That was a ROT13 cipher which always has a shift of 13. Nice work!")
def railFence():
    intro(level="3")  
    word = random_picker()
    rails = 3  # Number of rails
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1

    # Build the rail fence pattern, list within list
    for char in word:
        fence[rail].append(char)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    # Read off the rails to form the ciphertext
    cipher = "".join("".join(row) for row in fence)
    print("CIPHER:", cipher)
    
    ans = input("What is the word?\n").strip()
    while ans != word:
        ans = input("Incorrect. Please try again: ")
    
    print("You win! That was a Rail Fence cipher with 3 rails. Nice work!")

def vig():
    pass

def circularBitShift():
    pass


try:
    userMode = int(input("Welcome to a Cryptography learning game. Enter [1] to test your decryption skills, [2] for demos, or [3] for cipher tester.\n"))
    if userMode == 1:
        # Level-based progression with unlimited rounds (until interrupted)
        print("Level mode: 3 rounds, progressing Easy → Medium → Hard.")
        run_level_progression(total_rounds=3)
    elif userMode == 2:
        while True:
            run_demos()
    elif userMode == 3:
        while True:
            run_cipher_tester()
            back = input("\nTest another? [Y/n]: ").strip().lower()
            if back in ("n", "no"):
                break
            
    # TODO: Iterate with this format
    
except KeyboardInterrupt:
    print("\nQuitting game, goodbye.")