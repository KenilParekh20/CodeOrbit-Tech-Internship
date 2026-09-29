"""
Number Guessing Game (Command-Line Interface)
--------------------------------------------
A beginner-friendly Python game where the computer picks a random number
between 1 and 100, and the player tries to guess it with helpful hints.
"""

import random


# ==========================================
# 1. Helper Functions
# ==========================================

def generate_random_number(low: int = 1, high: int = 100) -> int:
    """
    Generates and returns a random integer between low and high (inclusive)
    using Python's built-in random module.
    """
    return random.randint(low, high)


def get_user_guess(low: int = 1, high: int = 100) -> int:
    """
    Prompts the player for a guess and handles invalid input (e.g. text/symbols)
    using a try/except block. Ensures the guess is within the valid range.
    """
    while True:
        user_input = input(f"Enter your guess ({low}-{high}): ").strip()
        try:
            guess = int(user_input)
            # Check if the guess falls within the allowed range
            if low <= guess <= high:
                return guess
            else:
                print(f"  [!] Out of bounds: Please enter a number between {low} and {high}.")
        except ValueError:
            # Handles non-integer input gracefully without crashing
            print("  [!] Invalid input: Please enter a valid whole number (no letters or symbols).")


def play_round(low: int = 1, high: int = 100) -> int:
    """
    Executes a single round of the game:
    - Generates the secret number
    - Loops until the player guesses correctly
    - Provides 'Too high' or 'Too low' hints
    - Returns the total number of attempts taken
    """
    secret_number = generate_random_number(low, high)
    attempts = 0

    print(f"\nI'm thinking of a number between {low} and {high}. Can you guess it?")

    while True:
        guess = get_user_guess(low, high)
        attempts += 1

        # Compare guess with the secret number
        if guess < secret_number:
            print("  📉 Too low! Try a higher number.\n")
        elif guess > secret_number:
            print("  📈 Too high! Try a lower number.\n")
        else:
            # Player guessed correctly
            print("\n" + "*" * 45)
            print(f"  🎉 Congratulations! You guessed it!")
            print(f"  🎯 The secret number was: {secret_number}")
            print(f"  📊 Total attempts taken: {attempts}")
            print("*" * 45)
            return attempts


# ==========================================
# 2. Main Game Loop
# ==========================================

def main():
    """
    Main controller for the game:
    - Displays the welcome banner
    - Manages multiple rounds
    - Tracks the player's best score (fewest attempts)
    - Asks if the user wants to play again
    """
    print("=" * 50)
    print("        WELCOME TO THE NUMBER GUESSING GAME       ")
    print("=" * 50)

    best_score = None  # Stores the lowest number of attempts

    while True:
        # Play a round and get attempts
        attempts = play_round(1, 100)

        # Update best score
        if best_score is None or attempts < best_score:
            best_score = attempts
            print(f"  🏆 New Best Score: {best_score} attempt(s)!")
        else:
            print(f"  🏆 Current Best Score: {best_score} attempt(s).")

        # Ask the user if they want to play another round
        play_again = input("\nDo you want to play again? (y/n): ").strip().lower()
        if play_again not in ("y", "yes"):
            print("\nThank you for playing! See you next time.\n")
            break


# Standard entry point
if __name__ == "__main__":
    main()
