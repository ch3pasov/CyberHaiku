import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / 'main.py'


class ConverterTests(unittest.TestCase):
    def convert(self, text):
        # Run the real CLI using only temporary, synthetic input/output files.
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            (folder / 'input').write_text(text, encoding='utf-8')
            result = subprocess.run(
                [sys.executable, '-X', 'utf8', str(SCRIPT)],
                cwd=folder, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            return (folder / 'output').read_text(encoding='utf-8')

    def test_empty_input_has_empty_output(self):
        self.assertEqual(self.convert(''), '')

    def test_lowercase_expansion_is_not_truncated(self):
        # U+0130 becomes two code points: i + COMBINING DOT ABOVE.
        self.assertEqual(self.convert('\u0130'), 'i\n\u0307')

    def test_unequal_rows_keep_the_existing_padding_and_separator(self):
        self.assertEqual(self.convert('AB\nC'), 'a c\nb  ')

    def test_one_final_newline_keeps_the_existing_output(self):
        self.assertEqual(self.convert('AB\nC\n'), 'a c\nb  ')

    def test_blank_rows_and_zero_width_input_keep_existing_behavior(self):
        self.assertEqual(self.convert('A\n\nC'), 'a   c')
        self.assertEqual(self.convert('\n'), '')


if __name__ == '__main__':
    unittest.main()
