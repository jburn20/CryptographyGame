"""
Author: jburn20
Program that teaches student cryptography
"""
from demos import demo_registry
import random, os, sys

def intro(level):
    barrier = "************"
    print(barrier)
    print(f"   Level {level}")
    print(barrier)

def random_picker():
    with open(os.path.join(os.path.dirname(__file__), "wordlist.txt"), "r") as f:
        words = [line.strip() for line in f if line.strip()]
    return random.choice(words)
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
        if ord(i) + shift >= 123: 
            diff = (ord(i) + shift) - 123 #* handles non alphabetical ord
            newchar = 97 + diff #* 97 = a in ord() form, serves as reset if we go past z
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
        if ord(i) + shift >= 123:
            diff = (ord(i) + shift) - 123
            newchar = 97 + diff
        else:
            newchar = ord(i) + shift
        new.append((chr(newchar)))
    print("CIPHER: ","".join(new))
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
    userMode = int(input("Welcome to a Cryptography learning game. Enter [1] to test your decryption skills or enter [2] to view encoding demonstrations.\n"))
    if userMode == 1: 
        caesar()
        rotThirteen()
        railFence()
    elif userMode == 2:
        while True:
            run_demos()
            
        # TODO: Iterate with this format
    
except KeyboardInterrupt:
    print("\nQuitting game, goodbye.")