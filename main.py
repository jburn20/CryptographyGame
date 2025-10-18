"""
Author: jburn20
Program that teaches student cryptography
"""
from demos import demo_registry
import random, os, sys, string, time, subprocess
from ciphers import generate_round, choose_difficulty_for_level, CIPHERS, generate_specific_round
from utils import GREEN, YELLOW, RED, RESET, clear_screen

# --- Dev toggles ---
DEV_SHOW_CIPHER = False  # Show cipher names during gameplay
DEV_MODE = True  # Enable dev menu for testing features

def _diff_color(difficulty):
    if difficulty == "easy":
        return GREEN
    if difficulty == "medium":
        return YELLOW
    return RED

def _clean_word(text):
    # Allow letters plus spaces only
    return "".join(ch for ch in text if ch.isalpha() or ch == " ")

def random_picker():
    with open(os.path.join(os.path.dirname(__file__), "wordlist.txt"), "r") as f:
        raw = [line.rstrip("\n") for line in f if line.strip()]
    words = [w for w in (_clean_word(x) for x in raw) if w]
    return random.choice(words)

def smart_word_picker(cipher_name):
    """Select appropriate word length based on cipher type."""
    with open(os.path.join(os.path.dirname(__file__), "wordlist.txt"), "r") as f:
        raw = [line.rstrip("\n") for line in f if line.strip()]
    words = [w for w in (_clean_word(x) for x in raw) if w]
    
    # Categorize words by length
    word_lengths = [len(word.split()) for word in words]
    short_words = [w for w in words if len(w.split()) <= 3]
    medium_words = [w for w in words if 3 < len(w.split()) <= 4]
    long_words = [w for w in words if len(w.split()) > 4]
    
    # Select based on cipher type
    if cipher_name in ["Columnar", "Affine", "Monoalphabetic Substitution Cipher"]:
        # Hard ciphers - prefer longer phrases for better patterns
        if long_words:
            return random.choice(long_words)
        elif medium_words:
            return random.choice(medium_words)
        else:
            return random.choice(words)
    else:
        # Easy ciphers - work with any length
        return random.choice(words)

def calculate_stars(score, rounds_played=None):
    """Calculate star rating (1-5) based purely on total score"""
    # Purely points-based system for scalability
    if score >= 20:      # Excellent
        return 5
    elif score >= 15:    # Great
        return 4
    elif score >= 10:    # Good
        return 3
    elif score >= 5:     # Decent
        return 2
    else:                # Participation (0-4 points)
        return 1

def get_badge_display(stars):
    """Return simple badge display with asterisks"""
    badges = ["[ ]", "[ ]", "[ ]", "[ ]", "[ ]"]
    for i in range(min(stars, 5)):
        badges[i] = "[*]"
    return "  ".join(badges)

def award_prize_animation(score, stars):
    """Show prize animation based on score/stars"""
    # Map stars to animation files
    prize_map = {
        1: "prizes/peter.json",
        2: "prizes/dance2.json",
        3: "prizes/linuxtype.json",
        4: "prizes/nerd.json",
        5: "prizes/squid.json"
    }
    
    animation_file = prize_map.get(stars, "prizes/peter.json")
    
    # Check if file exists
    if not os.path.exists(animation_file):
        print(f"[!] Prize animation not found: {animation_file}")
        return
    
    # Run the prize animation
    try:
        subprocess.run([sys.executable, "prize.py", animation_file])
    except Exception as e:
        print(f"[!] Could not run prize animation: {e}")

def run_level_progression(seed=None):
    if seed is not None:
        random.seed(seed)
    
    total_score = 0
    rounds_played = 0
    recent = []
    
    while True:  # Main game loop - user chooses when to quit
        # Show current stats and difficulty selection
        clear_screen()
        print("=" * 50)
        print("CRYPTOGRAPHY CHALLENGE")
        print("=" * 50)
        print(f"Current Score: {total_score}")
        print(f"Rounds Played: {rounds_played}")
        print("=" * 50)
        print("\nChoose your difficulty:")
        print(f"[1] Easy   - 3 points")
        print(f"[2] Hard   - 5 points") 
        print(f"[0] Quit Game")
        if DEV_MODE:
            print(f"[D] Dev: Add points")
        print("=" * 50)
        
        choice = input("Select difficulty: ").strip()
        
        # Dev command: add points directly
        if DEV_MODE and choice.lower() == 'd':
            try:
                points = int(input("Enter points to add: "))
                rounds = int(input("Enter rounds to add (optional, default 0): ") or 0)
                total_score += points
                rounds_played += rounds
                print(f"\n[DEV] Added {points} points and {rounds} rounds")
                input("Press Enter to continue...")
                continue
            except ValueError:
                print("[DEV] Invalid input, cancelled")
                input("Press Enter to continue...")
                continue
        
        if choice == "0":
            # Game over - show final stats and prize
            final_stars = calculate_stars(total_score)
            clear_screen()
            print("=" * 60)
            print("                    GAME COMPLETE")
            print("=" * 60)
            print(f"Final Score:      {total_score}")
            print(f"Rounds Played:    {rounds_played}")
            print("=" * 60)
            
            # Show badge display
            if rounds_played > 0:
                print()
                print("BADGES:")
                print(get_badge_display(final_stars))
                print()
                
                # Offer prize animation
                show_prize = input("Claim your prize animation? [Y/n]: ").strip().lower()
                if show_prize != 'n':
                    print("\n>> Preparing prize animation...")
                    print("   Tip: Fullscreen your terminal for best experience!")
                    award_prize_animation(total_score, final_stars)
            
            print("\nThanks for playing!")
            break
            
        # Map choice to difficulty
        difficulty_map = {"1": "easy", "2": "hard"}
        if choice not in difficulty_map:
            print("Invalid choice! Please try again.")
            input("Press Enter to continue...")
            continue
            
        difficulty = difficulty_map[choice]
        base_points = 3 if difficulty == "easy" else 5
        
        # Generate round
        word = random_picker()
        rnd = generate_round(word, difficulty, recent)
        word = smart_word_picker(rnd['name'])
        rnd = generate_specific_round(word, rnd['name'])
        current_cipher_name = rnd['name']
        points = base_points
        hint_tier = 0  # 0=none, 1=type only, 2=type+params
        
        # Play the round
        while True:
            diff_col = _diff_color(difficulty)
            clear_screen()
            print(f"Difficulty: {diff_col}{difficulty.capitalize()}{RESET} ({base_points} points)")
            print(f"Current Score: {total_score} | This Round: {points}")
            if DEV_SHOW_CIPHER or hint_tier > 0:
                print(f"Cipher: {diff_col}{current_cipher_name}{RESET}")
                if hint_tier >= 2 and 'params' in rnd and rnd['params']:
                    pretty = []
                    for k, v in rnd['params'].items():
                        label = k.capitalize()
                        pretty.append(f"{label}: {v}")
                    print(" | ".join(pretty))
            print("CIPHER:", rnd['ciphertext'])

            # Always show help options
            print("[R] Regenerate (same cipher, new word) - 1 point")
            if hint_tier == 0:
                tier1_cost = -(-points // 2)  # Ceiling division for half points
                print(f"[H] Hint - Reveal cipher type - {tier1_cost} points")
            elif hint_tier == 1:
                tier2_cost = max(0, points - 1)
                print(f"[H] Hint - Reveal parameters - {tier2_cost} points (sets to 1)")

            ans = input("What is the word?\n").strip()
            normalized_ans = ans.replace(" ", "").upper()
            normalized_plain = rnd["plaintext"].replace(" ", "").upper()

            # Commands - always available
            if normalized_ans.lower() in ("r", "regenerate"):
                points = max(0, points - 1)
                word = smart_word_picker(current_cipher_name)
                rnd = generate_specific_round(word, current_cipher_name)
                continue
            if normalized_ans.lower() in ("h", "hint"):
                if hint_tier == 0:
                    hint_tier = 1
                    tier1_cost = -(-points // 2)
                    points = max(0, points - tier1_cost)
                    continue
                elif hint_tier == 1:
                    hint_tier = 2
                    points = 1
                    continue
            if ans.lower() == "pass":
                rounds_played += 1
                break

            if normalized_ans == normalized_plain:
                award = max(points, 0)
                print(f"You win! Awarded {award} points!")
                total_score += award
                rounds_played += 1
                break
            else:
                if points == 0:
                    print("Incorrect! But you get 1 point for trying.")
                    total_score += 1
                    rounds_played += 1
                    break
                else:
                    points = 1
                    print("Incorrect! You have one more chance...")

        recent.append(current_cipher_name)
        input("\nPress Enter to continue...")

def get_cipher_params(name):
    """Get parameters for a specific cipher from user input."""
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
    elif name == "Monoalphabetic Substitution Cipher":
        print("Using fixed substitution alphabet: QWERTYUIOPASDFGHJKLZXCVBNM")
        params = {}
    elif name == "Rail Fence":
        params["rails"] = int(input("rails (2-5): ") or 3)
    elif name == "Circular Bit Shift":
        params["shift"] = int(input("shift (1-7): ") or 3)
        params["direction"] = (input("direction [left/right]: ") or "left").strip().lower()
    elif name == "Beaufort":
        params["key"] = input("key (A-Z): ").strip().upper() or "KEY"
    elif name == "Autokey":
        params["primer"] = input("primer (1-3 letters): ").strip().upper() or "KEY"
    elif name == "Scytale":
        params["diameter"] = int(input("diameter (3-5): ") or 3)
    # ROT13, Atbash: no params needed
    return params

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
    
    # Ask if user wants to use smart word picker or enter their own
    use_smart = input("Use smart word picker for this cipher? [Y/n]: ").strip().lower()
    if use_smart in ("", "y", "yes"):
        plaintext = smart_word_picker(name)
        print(f"Selected phrase: {plaintext}")
    else:
        plaintext = input("Enter plaintext (letters and spaces): ").rstrip("\n")
    
    auto = input("Auto-generate parameters? [Y/n]: ").strip().lower()
    if auto in ("", "y", "yes"):
        params = meta["params"]()
    else:
        params = get_cipher_params(name)
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

def dev_test_prize_system():
    """Dev mode: Test the prize/star rating system"""
    clear_screen()
    print("=" * 60)
    print("               DEV MODE - PRIZE SYSTEM TEST")
    print("=" * 60)
    print()
    print("Test different score scenarios:\n")
    print("[1] Test 1 star  (Score: 2)")
    print("[2] Test 2 stars (Score: 7)")
    print("[3] Test 3 stars (Score: 12)")
    print("[4] Test 4 stars (Score: 17)")
    print("[5] Test 5 stars (Score: 25)")
    print("[6] Custom score")
    print("[7] Test all badges in game context")
    print("[8] Play all animations in folder")
    print("[0] Back to main menu")
    print()
    
    choice = input("Select test: ").strip()
    
    test_scenarios = {
        "1": (2, 1),
        "2": (7, 2),
        "3": (12, 3),
        "4": (17, 4),
        "5": (25, 5),
    }
    
    if choice in test_scenarios:
        score, rounds = test_scenarios[choice]
        stars = calculate_stars(score)
        
        clear_screen()
        print("=" * 60)
        print("                    TEST GAME COMPLETE")
        print("=" * 60)
        print(f"Final Score:      {score}")
        print(f"Rounds Played:    {rounds}")
        print("=" * 60)
        print()
        print("BADGES:")
        print(get_badge_display(stars))
        print()
        
        show_prize = input("See prize animation? [Y/n]: ").strip().lower()
        if show_prize != 'n':
            print("\n>> Preparing prize animation...")
            print("   Tip: Fullscreen your terminal for best experience!")
            award_prize_animation(score, stars)
    
    elif choice == "6":
        try:
            score = int(input("Enter score: "))
            stars = calculate_stars(score)
            print(f"\nResult: {stars} stars for {score} points")
            print()
            print("BADGES:")
            print(get_badge_display(stars))
            print()
            show_prize = input("See prize animation? [Y/n]: ").strip().lower()
            if show_prize != 'n':
                award_prize_animation(score, stars)
        except ValueError:
            print("Invalid input")
    
    elif choice == "7":
        # Test badges in game context
        clear_screen()
        print("=" * 60)
        print("            TEST BADGES IN GAME CONTEXT")
        print("=" * 60)
        print()
        
        prize_map = {
            1: ("prizes/peter.json", "1 Star - Peter", 2),
            2: ("prizes/dance2.json", "2 Stars - Dance", 7),
            3: ("prizes/linuxtype.json", "3 Stars - Linux Type", 12),
            4: ("prizes/nerd.json", "4 Stars - Nerd", 17),
            5: ("prizes/squid.json", "5 Stars - Squid", 25)
        }
        
        for stars, (animation_file, description, score) in prize_map.items():
            clear_screen()
            print("=" * 60)
            print("                    GAME COMPLETE")
            print("=" * 60)
            print(f"Final Score:      {score}")
            print(f"Rounds Played:    {stars}")
            print("=" * 60)
            print()
            print("BADGES:")
            print(get_badge_display(stars))
            print()
            print(f"Prize: {description}")
            
            play = input("\nPlay this prize animation? [Y/n/q to quit]: ").strip().lower()
            if play == 'q':
                break
            elif play != 'n':
                if not os.path.exists(animation_file):
                    print(f"[!] File not found: {animation_file}")
                    input("Press Enter to continue...")
                else:
                    try:
                        subprocess.run([sys.executable, "prize.py", animation_file])
                    except Exception as e:
                        print(f"[!] Error: {e}")
                        input("Press Enter to continue...")
        
        input("\nAll badge tests complete. Press Enter to continue...")
    
    elif choice == "8":
        # Play all animations in prizes folder
        import glob
        
        while True:
            clear_screen()
            print("=" * 60)
            print("         PLAY ALL ANIMATIONS IN FOLDER")
            print("=" * 60)
            print()
            
            # Get all .json files in prizes folder
            animation_files = sorted(glob.glob("prizes/*.json"))
            
            if not animation_files:
                print("[!] No animation files found in prizes/ folder")
                input("Press Enter to continue...")
                break
            
            print(f"Found {len(animation_files)} animation(s):\n")
            for i, filepath in enumerate(animation_files, 1):
                filename = os.path.basename(filepath)
                print(f"  [{i}] {filename}")
            print(f"  [A] Play all sequentially")
            print(f"  [0] Back to dev menu")
            print()
            
            selection = input("Select animation number (or A for all): ").strip().lower()
            
            if selection == '0':
                break
            elif selection == 'a':
                # Play all animations sequentially
                for filepath in animation_files:
                    filename = os.path.basename(filepath)
                    print(f"\n{'='*60}")
                    print(f"  Animation: {filename}")
                    print('='*60)
                    
                    play = input("Play this animation? [Y/n/q to quit]: ").strip().lower()
                    if play == 'q':
                        break
                    elif play != 'n':
                        try:
                            subprocess.run([sys.executable, "prize.py", filepath])
                        except Exception as e:
                            print(f"[!] Error: {e}")
                            input("Press Enter to continue...")
                
                input("\nAll animations complete. Press Enter to continue...")
            else:
                # Try to play selected animation by number
                try:
                    idx = int(selection) - 1
                    if 0 <= idx < len(animation_files):
                        filepath = animation_files[idx]
                        filename = os.path.basename(filepath)
                        print(f"\nPlaying: {filename}")
                        try:
                            subprocess.run([sys.executable, "prize.py", filepath])
                        except Exception as e:
                            print(f"[!] Error: {e}")
                        input("\nPress Enter to continue...")
                    else:
                        print("[!] Invalid selection")
                        input("Press Enter to continue...")
                except ValueError:
                    print("[!] Invalid input")
                    input("Press Enter to continue...")
    
    elif choice == "0":
        return
    else:
        print("Invalid choice")
    
    input("\nPress Enter to continue...")
    dev_test_prize_system()


try:
    menu_text = "Welcome to a Cryptography learning game. Enter [1] to test your decryption skills, [2] for demos, or [3] for cipher tester"
    if DEV_MODE:
        menu_text += ", or [9] for dev tests"
    menu_text += ".\n"
    
    userMode = int(input(menu_text))
    if userMode == 1:
        # Interactive difficulty selection with point bounties
        print("Challenge mode: Choose your difficulty and earn points!")
        run_level_progression()
    elif userMode == 2:
        while True:
            run_demos()
    elif userMode == 3:
        while True:
            run_cipher_tester()
            back = input("\nTest another? [Y/n]: ").strip().lower()
            if back in ("n", "no"):
                break
    elif userMode == 9 and DEV_MODE:
        dev_test_prize_system()
    else:
        if userMode == 9 and not DEV_MODE:
            print("Dev mode is disabled. Set DEV_MODE = True in main.py to enable.")
        else:
            print("Invalid mode selected.")
            
    # TODO: Iterate with this format
    
except KeyboardInterrupt:
    print("\nQuitting game, goodbye.")