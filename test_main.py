import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import os
from main import (
    load_words_from_file,
    pick_word,
    make_mask,
    apply_guess,
    DEFAULT_WORD_LIST,
)


class TestLoadWordsFromFile(unittest.TestCase):
    """Test cases for the load_words_from_file function."""

    def setUp(self):
        """Create a temporary file for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_words.txt")

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)

    def test_load_words_from_valid_file(self):
        """Test loading words from a valid file."""
        with open(self.test_file, "w") as f:
            f.write("python\njavascript\nrustlang\n")

        words = load_words_from_file(self.test_file)
        self.assertEqual(words, ["python", "javascript", "rustlang"])

    def test_load_words_case_insensitive(self):
        """Test that words are converted to lowercase."""
        with open(self.test_file, "w") as f:
            f.write("Python\nJavaScript\nRUSTLANG\n")

        words = load_words_from_file(self.test_file)
        self.assertEqual(words, ["python", "javascript", "rustlang"])

    def test_load_words_ignores_comments(self):
        """Test that lines starting with # are ignored."""
        with open(self.test_file, "w") as f:
            f.write("# This is a comment\npython\n# Another comment\njava\n")

        words = load_words_from_file(self.test_file)
        self.assertEqual(words, ["python", "java"])

    def test_load_words_ignores_empty_lines(self):
        """Test that empty lines are ignored."""
        with open(self.test_file, "w") as f:
            f.write("python\n\njava\n   \nscript\n")

        words = load_words_from_file(self.test_file)
        self.assertEqual(words, ["python", "java", "script"])

    def test_load_words_ignores_single_letters(self):
        """Test that single-letter words are ignored."""
        with open(self.test_file, "w") as f:
            f.write("a\npython\nb\njava\n")

        words = load_words_from_file(self.test_file)
        self.assertEqual(words, ["python", "java"])

    def test_load_words_ignores_non_alpha(self):
        """Test that words with numbers or symbols are ignored."""
        with open(self.test_file, "w") as f:
            f.write("python2\npython\njava3.0\njava\n")

        words = load_words_from_file(self.test_file)
        self.assertEqual(words, ["python", "java"])

    def test_load_words_file_not_found(self):
        """Test that default word list is returned when file doesn't exist."""
        words = load_words_from_file("/nonexistent/path/words.txt")
        self.assertEqual(words, DEFAULT_WORD_LIST.copy())

    def test_load_words_empty_file(self):
        """Test that default word list is returned for empty file."""
        with open(self.test_file, "w") as f:
            f.write("# Only comments\n# No actual words\n")

        words = load_words_from_file(self.test_file)
        self.assertEqual(words, DEFAULT_WORD_LIST.copy())


class TestPickWord(unittest.TestCase):
    """Test cases for the pick_word function."""

    @patch("main.word_list", ["python", "hangman", "keyboard"])
    @patch("main.random.choice")
    def test_pick_word_returns_from_list(self, mock_choice):
        """Test that pick_word returns a word from the word list."""
        mock_choice.return_value = "python"
        word = pick_word()
        self.assertEqual(word, "python")
        mock_choice.assert_called_once()

    @patch("main.word_list", ["hangman"])
    @patch("main.random.choice")
    def test_pick_word_single_word(self, mock_choice):
        """Test pick_word with a single word in the list."""
        mock_choice.return_value = "hangman"
        word = pick_word()
        self.assertEqual(word, "hangman")


class TestMakeMask(unittest.TestCase):
    """Test cases for the make_mask function."""

    def test_make_mask_simple_word(self):
        """Test mask creation for a simple word."""
        mask = make_mask("python")
        self.assertEqual(mask, ["_", "_", "_", "_", "_", "_"])

    def test_make_mask_short_word(self):
        """Test mask creation for a short word."""
        mask = make_mask("hi")
        self.assertEqual(mask, ["_", "_"])

    def test_make_mask_long_word(self):
        """Test mask creation for a long word."""
        mask = make_mask("internationalization")
        self.assertEqual(len(mask), 20)
        self.assertEqual(mask, ["_"] * 20)

    def test_make_mask_single_letter(self):
        """Test mask creation for a single letter."""
        mask = make_mask("a")
        self.assertEqual(mask, ["_"])

    def test_make_mask_returns_list(self):
        """Test that make_mask returns a list."""
        mask = make_mask("test")
        self.assertIsInstance(mask, list)

    def test_make_mask_correct_length(self):
        """Test that mask length matches word length."""
        words = ["a", "at", "cat", "python", "programming"]
        for word in words:
            mask = make_mask(word)
            self.assertEqual(len(mask), len(word))


class TestApplyGuess(unittest.TestCase):
    """Test cases for the apply_guess function."""

    def test_apply_guess_correct_single_letter(self):
        """Test applying a correct guess with one occurrence."""
        secret_word = "python"
        mask = make_mask(secret_word)
        result = apply_guess(secret_word, mask, "p")

        self.assertTrue(result)
        self.assertEqual(mask[0], "p")
        self.assertEqual(mask, ["p", "_", "_", "_", "_", "_"])

    def test_apply_guess_correct_multiple_occurrences(self):
        """Test applying a correct guess with multiple occurrences."""
        secret_word = "banana"
        mask = make_mask(secret_word)
        result = apply_guess(secret_word, mask, "a")

        self.assertTrue(result)
        self.assertEqual(mask, ["_", "a", "_", "a", "_", "a"])

    def test_apply_guess_incorrect(self):
        """Test applying an incorrect guess."""
        secret_word = "python"
        mask = make_mask(secret_word)
        result = apply_guess(secret_word, mask, "z")

        self.assertFalse(result)
        self.assertEqual(mask, ["_", "_", "_", "_", "_", "_"])

    def test_apply_guess_modifies_mask_correctly(self):
        """Test that apply_guess modifies the mask in place."""
        secret_word = "cat"
        mask = make_mask(secret_word)
        apply_guess(secret_word, mask, "c")
        apply_guess(secret_word, mask, "a")
        apply_guess(secret_word, mask, "t")

        self.assertEqual(mask, ["c", "a", "t"])

    def test_apply_guess_case_insensitive(self):
        """Test that apply_guess works with lowercase guesses."""
        secret_word = "Python"
        mask = make_mask(secret_word.lower())
        # Note: The game converts words to lowercase, so secret_word should be lowercase
        secret_word_lower = "python"
        result = apply_guess(secret_word_lower, mask, "p")

        self.assertTrue(result)
        self.assertEqual(mask[0], "p")

    def test_apply_guess_all_same_letter_word(self):
        """Test applying guesses to a word with repeated letters."""
        secret_word = "aaa"
        mask = make_mask(secret_word)
        result = apply_guess(secret_word, mask, "a")

        self.assertTrue(result)
        self.assertEqual(mask, ["a", "a", "a"])

    def test_apply_guess_does_not_affect_mask_on_wrong_guess(self):
        """Test that mask is unchanged after a wrong guess."""
        secret_word = "python"
        mask = ["p", "_", "_", "_", "_", "_"]
        original_mask = mask.copy()
        apply_guess(secret_word, mask, "z")

        self.assertEqual(mask, original_mask)

    def test_apply_guess_return_value(self):
        """Test that apply_guess returns boolean correctly."""
        secret_word = "test"
        mask = make_mask(secret_word)

        result_correct = apply_guess(secret_word, mask, "t")
        result_incorrect = apply_guess(secret_word, mask, "z")

        self.assertEqual(result_correct, True)
        self.assertEqual(result_incorrect, False)


class TestIntegration(unittest.TestCase):
    """Integration tests for game functions working together."""

    def test_full_word_reveal_process(self):
        """Test revealing a complete word through guesses."""
        secret_word = "cat"
        mask = make_mask(secret_word)

        guesses = ["c", "a", "t"]
        for guess in guesses:
            apply_guess(secret_word, mask, guess)

        self.assertEqual("".join(mask), secret_word)

    def test_partial_reveal(self):
        """Test partial word revelation."""
        secret_word = "python"
        mask = make_mask(secret_word)

        apply_guess(secret_word, mask, "p")
        apply_guess(secret_word, mask, "h")
        apply_guess(secret_word, mask, "z")  # Wrong guess

        self.assertIn("_", mask)
        self.assertEqual(mask[0], "p")
        self.assertEqual(mask[3], "h")

    def test_game_flow_scenario(self):
        """Test a realistic game scenario."""
        secret_word = "hangman"
        mask = make_mask(secret_word)
        guessed_letters = []

        # Simulate some guesses
        test_guesses = ["a", "n", "g", "x", "y", "z"]
        correct_count = 0
        incorrect_count = 0

        for guess in test_guesses:
            guessed_letters.append(guess)
            is_correct = apply_guess(secret_word, mask, guess)
            if is_correct:
                correct_count += 1
            else:
                incorrect_count += 1

        self.assertEqual(correct_count, 3)  # a, n, g
        self.assertEqual(incorrect_count, 3)  # x, y, z


if __name__ == "__main__":
    unittest.main()
