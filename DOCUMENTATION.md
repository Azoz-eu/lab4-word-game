# Main.py Documentation

## Overview
Hangman game implementation with word list file support and multi-round gameplay tracking.

## Core Functions

### `load_words_from_file(file_path)`
Loads words from a text file with filtering:
- Strips whitespace and converts to lowercase
- Skips comments (lines starting with `#`)
- Skips single-letter words and non-alphabetic words
- Falls back to `DEFAULT_WORD_LIST` if file not found or empty

### `pick_word()`
Returns a random word from the loaded `word_list`.

### `make_mask(word)`
Creates a list of underscores matching word length, representing hidden letters.

### `get_guess(guessed_letters)`
Prompts player for a single alphabetic letter, with validation:
- Rejects non-single characters
- Rejects non-alphabetic input
- Prevents duplicate guesses

Returns lowercase letter.

### `apply_guess(secret_word, mask, guess)`
Updates the mask by revealing all matching letters in the secret word.

**Returns:** `True` if guess was correct, `False` otherwise

### `play_game(round_number)`
Main game loop for a single round:
- Generates secret word and mask
- Tracks guessed letters and lives (starts at 6)
- Loop: displays word/lives/guesses, gets guess, applies it, deducts life on wrong guess
- Ends when word is revealed (win) or lives reach 0 (loss)

**Returns:** Dictionary with round number, secret word, outcome, and lives remaining

### `main()`
Game driver:
- Loops through rounds, tracking results
- Displays final summary with win/loss counts

## Game Entry Point
Run with `python main.py` to start playing. The `if __name__ == "__main__":` guard allows importing functions for testing without triggering gameplay.

## Key Variables
- `word_list`: Words loaded from `words.txt` or defaults
- `mask`: List representing revealed/hidden letters (e.g., `['h', '_', 'n', 'g', 'm', '_', 'n']`)
- `guessed_letters`: List of player's guesses
- `lives`: Remaining incorrect guess allowances (decrements on wrong guesses)
