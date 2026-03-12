# My original thinking
1- what are the states of a game like hangman?
''' starts the game by picking a word and hiding it with (_ _ _ _)
the player guesses and updates it each time
player either guesses it right or runs out of guesses

2- What variables are required?
''' secret word = string
letters player has guessed = list
how many guesses left = integer
the word guessing current progress = list/string

3- what are the rules and invariants?
''' if a guessed letter is in the word, reveal all instances of it. if not then decreases the lives's count
the number of blanks letters shown to the player must always match the length of the secret word

4- What kind of bugs and edge cases should we be careful about?
case sensitivity
invalid characters
repeated guesses
what happens if the player writes the entire sentence instead of a letter?

# Copilot suggestions
App states: setup
Choose secret word.
Initialize guesses_left, guessed_letters, and masked word (like _ _ _ _).

AWAIT_INPUT
Prompt player for next guess.
Game is waiting; no state changes yet.

VALIDATE_INPUT
Check input rules:
exactly one character
alphabetical only
normalize case (e.g., lowercase)
reject if previously guessed

APPLY_GUESS
If letter is in secret word: reveal all matching positions.
If letter is not in secret word: decrement guesses_left.
Add guess to guessed_letters.

CHECK_WIN_LOSS
If all letters revealed: go to WON.
Else if guesses_left == 0: go to LOST.
Else go back to AWAIT_INPUT.

CHECK_WIN_LOSS
If all letters revealed: go to WON.
Else if guesses_left == 0: go to LOST.
Else go back to AWAIT_INPUT.

LOST (terminal)
Show failure message and reveal word.
Offer replay

REPLAY_DECISION (optional)
If yes: back to SETUP.
If no: EXIT.


App variables:
secret_word: str

The answer the player is trying to guess.

guessed_letters: set[str]

All letters the player has already tried.

set is better than list because duplicate checks are fast.

correct_letters: set[str]

Subset of guessed letters that are in secret_word.

Optional, but useful for clarity.

wrong_letters: set[str]

Subset of guessed letters not in secret_word.

Useful for showing mistakes to the player.

guesses_left: int

Remaining lives/attempts
max_guesses: int

Initial lives, so you can reset/restart easily.

current_mask: list[str] or derived string

Current revealed progress like ['_', 'a', '_', 'g'].

Can also be computed each turn from secret_word + correct_letters instead of stored.

game_state: str (or enum)

Example values: SETUP, AWAIT_INPUT, APPLY_GUESS, WON, LOST.

Helps keep game flow explicit.

last_input: str

Most recent raw player input (helpful for validation and feedback).

message: str (optional UI feedback)

Example: "Already guessed that letter" or "Good guess!".


App rules and invariants:

input policy, reveal/penalty behavior, terminal states, and consistency conditions for masks and guesses


App bugs: 

invalid input, repeated guesses, normalization issues, off-by-one life handling, and restart/state-reset errors