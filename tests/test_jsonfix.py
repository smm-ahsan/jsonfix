"""Tests for jsonfix — stdlib unittest only."""

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import jsonfix  # noqa: E402


def run_cli(*argv):
    """Run the CLI in-process and capture stdout plus the exit code."""
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        with mock.patch.object(sys, "argv", ["jsonfix.py", *argv]):
            code = jsonfix.main()
    return code, stdout.getvalue()


class TestJsonfix(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_text_exits_zero(self):
        code, out = run_cli("--text", '{"a": 1}')
        self.assertEqual(code, 0)
        self.assertIn("Valid JSON.", out)

    def test_invalid_text_exits_two_with_caret(self):
        code, out = run_cli("--text", '{"a": 1')
        self.assertEqual(code, 2)
        self.assertIn("Invalid JSON:", out)
        self.assertIn("^", out)

    def test_missing_file_exits_two(self):
        code, out = run_cli("--file", str(self.dir / "nope.json"))
        self.assertEqual(code, 2)
        self.assertIn("could not read file", out)

    def test_non_utf8_file_exits_two_without_traceback(self):
        path = self.dir / "latin1.json"
        path.write_bytes(b'{"a": "caf\xe9"}\n')
        code, out = run_cli("--file", str(path))
        self.assertEqual(code, 2)
        self.assertIn("could not read file", out)

if __name__ == "__main__":
    unittest.main()
