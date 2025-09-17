import time
import sys

def rail_fence_demo(word="HELLOWORLD", rails=3, delay=0.4):
    print("The rail fence cipher is a transposition cipher that writes characters in a zigzag pattern across a given number of rows(rails).")

    header = f"Word: {word} | Rails: {rails}"
    print(header, "\n")
    

    # Initialize rail structure
    fence = [["-" for _ in range(len(word))] for _ in range(rails)]

    # Print initial rails
    for row in fence:
        print(" ".join(row))

    rail = 0
    direction = 1

    for col, ch in enumerate(word):
        # Place the letter in the correct rail
        fence[rail][col] = ch

        # Move cursor up to the start of rail lines
        sys.stdout.write(f"\033[{rails}F")  # move cursor up N lines
        # Print each rail line
        for row in fence:
            print(" ".join(row))
        # Move cursor down again so next print is after rails
        sys.stdout.flush()
        time.sleep(delay)

        # Move to next rail
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    # Build final ciphertext
    cipher = "".join(ch for row in fence for ch in row if ch != "-")
    print("\nFinal Ciphertext:", cipher)


if __name__ == "__main__":
    rail_fence_demo("HELLOWORLD", rails=3, delay=0.4)
