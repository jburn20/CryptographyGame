"""
Author: jburn20
Program that teaches student cryptography
"""

import random, os

def intro(level):
    barrier = "************"
    print(barrier)
    print(f"   Level {level}")
    print(barrier)

def random_picker():
    with open(os.path.join(os.path.dirname(__file__), "wordlist.txt"), "r") as f:
         words = [line.strip() for line in f if line.strip()]
    return random.choice(words)

def caesar():
    intro(level="1")
    shift = random.randint(1,25)
    word = random_picker() 
    new = []
    for i in word:
        if ord(i) + shift >= 123: #*
            diff = (ord(i) + shift) - 123 #* handles non alphabetical ord
            newchar = 97 + diff #* 97 = a in ord() form, serves as reset if we go past z
        else: 
            newchar = ord(i) + shift #* normal shifting
        new.append(chr(newchar)) #* convert num to char, append char to new
    print("CIPHER:","".join(new)) #* turn list into string
    ans = input("What is the word?\n").strip()
    while ans != word:
        ans = input("Incorrect. Try again: ")
    print("You win! That was a caesar cipher with a shift of {shift}. Nice work!")
    
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
try: 
    caesar()
    rotThirteen() # TODO: Iterate with this format

except KeyboardInterrupt:
        print("\nQuitting game, goodbye.")