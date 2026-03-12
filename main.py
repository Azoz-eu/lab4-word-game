import random
from pathlib import Path

DEFAULT_WORD_LIST = ["python", "hangman", "keyboard", "monitor"]


def load_words_from_file(file_path):
    words = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                candidate = line.strip().lower()

                if not candidate or candidate.startswith("#"):
                    continue

                # Keep only letter-based words to avoid punctuation/numbers in gameplay.
                if candidate.isalpha() and len(candidate) > 1:
                    words.append(candidate)
    except OSError:
        return DEFAULT_WORD_LIST.copy()

    if not words:
        return DEFAULT_WORD_LIST.copy()

    return words


word_list = load_words_from_file(Path(__file__).with_name("words.txt"))


def pick_word():
    word = random.choice(word_list)
    return word


def make_mask(word):
    mask = []
    for letter in word:
        mask.append("_")
    return mask


def get_guess(guessed_letters):
    while True:
        guess = input("Guess a letter: ").lower()
        if len(guess) != 1:
            print("Please enter one letter only.")
        elif not guess.isalpha():
            print("Please enter a letter, not a number or symbol.")
        elif guess in guessed_letters:
            print("You already guessed that letter!")
        else:
            return guess


def apply_guess(secret_word, mask, guess):
    if guess in secret_word:
        for i in range(len(secret_word)):
            if secret_word[i] == guess:
                mask[i] = guess
        return True
    else:
        return False


def play_game(round_number):
    secret_word = pick_word()
    mask = make_mask(secret_word)
    guessed_letters = []
    lives = 6

    while lives > 0 and "_" in mask:
        print("\nWord:", " ".join(mask))
        print("Lives:", lives)
        print("Guessed:", guessed_letters)

        guess = get_guess(guessed_letters)
        guessed_letters.append(guess)

        correct = apply_guess(secret_word, mask, guess)

        if correct:
            print("Good guess!")
        else:
            lives -= 1
            print(f"Wrong! {lives} lives left.")

    if "_" not in mask:
        print(f"\nYou won! The word was {secret_word}")
        outcome = "Won"
    else:
        print(f"\nYou lost! The word was {secret_word}")
        outcome = "Lost"

    return {
        "round": round_number,
        "word": secret_word,
        "outcome": outcome,
        "lives_left": lives,
    }


def main():
    """Main function to run the hangman game"""
    results = []
    round_number = 1

    while True:
        result = play_game(round_number)
        results.append(result)
        round_number += 1

        again = input("\nPlay again? (y/n): ").lower()
        if again != "y":
            break

    wins = 0
    losses = 0

    for r in results:
        print(
            f"Round {r['round']}: {r['outcome']} | Word: {r['word']} | Lives left: {r['lives_left']}"
        )
        if r["outcome"] == "Won":
            wins += 1
        else:
            losses += 1

    print(f"\nTotal rounds: {len(results)}")
    print(f"Wins: {wins} | Losses: {losses}")

if __name__ == "__main__":
    main()
