# Hangman Word Game

A command-line implementation of the classic Hangman word guessing game in Python.

## Features

- **Word file support**: Load words from `words.txt` or use default word list
- **Multi-round gameplay**: Play multiple rounds and track wins/losses
- **Input validation**: Prevents invalid guesses and duplicate letters
- **Game summary**: Displays win/loss statistics at the end
- **Comprehensive tests**: 27 unit tests covering all game functions

## Project Structure

```
.
├── main.py              # Main game implementation
├── test_main.py         # Unit tests (27 tests)
├── words.txt            # Word list for gameplay
├── DOCUMENTATION.md     # Detailed function documentation
├── README.md            # This file
└── requirements.txt     # Python dependencies (optional)
```

## Installation

1. Clone or download the repository
2. No external dependencies required—uses only Python standard library

## How to Play

```bash
python main.py
```

Follow the prompts:
- Guess one letter at a time
- You have 6 lives (wrong guesses cost 1 life)
- Reveal all letters to win
- Game tracks rounds and displays final summary

## Running Tests

### Prerequisites
Install pytest (optional but recommended):
```bash
pip install pytest
```

### Run all tests
```bash
pytest test_main.py -v
```

### Run specific test class
```bash
pytest test_main.py::TestMakeMask -v
```

### Run without pytest (using unittest)
```bash
python -m unittest test_main.py
```

## Test Coverage

The test suite includes:
- **File Loading Tests** (8 tests): File handling, filtering, validation
- **Word Selection Tests** (2 tests): Random word picking
- **Mask Generation Tests** (6 tests): Mask creation for various word lengths
- **Guess Application Tests** (8 tests): Correct/incorrect guesses, edge cases
- **Integration Tests** (3 tests): Full game flow scenarios

All 27 tests pass successfully.

## Game Rules

- Each round uses a random secret word
- Player guesses one letter per turn
- Correct guesses reveal all matching letters
- Wrong guesses deduct 1 life
- Win: reveal all letters before losing all lives
- Lose: run out of lives before revealing the word
- Play multiple rounds and compare stats

## Example Game Session

```
Word: _ _ _ _ _ _
Lives: 6
Guessed: []
Guess a letter: e
Good guess!

Word: _ _ _ _ _ e
Lives: 6
Guessed: ['e']
Guess a letter: a
Wrong! 5 lives left.
...
You won! The word was python
```

## Documentation

See [DOCUMENTATION.md](DOCUMENTATION.md) for detailed function descriptions.

## License

Open source.
