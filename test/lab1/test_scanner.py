from pathlib import Path
import subprocess
import sys
import unittest

from src.scanner import Scanner
from src.token_type import TokenType
from test.lab1.cases import CASES, expected_stderr, expected_stdout


ROOT = Path(__file__).resolve().parents[2]


class ScannerTests(unittest.TestCase):
    def test_all_scanner_cases(self):
        for case in CASES:
            with self.subTest(case=case.name):
                source = case.path.read_bytes().decode("utf-8")
                self.assertEqual(source, case.source)
                scanner = Scanner(source)
                tokens = scanner.scan_tokens()
                actual = tuple((t.type.name, t.lexeme, t.literal, t.line, t.column) for t in tokens)
                self.assertEqual(actual, case.tokens)
                self.assertEqual(tuple((e.line, e.column, e.message) for e in scanner.errors), case.errors)
                self.assertEqual("".join(f"{token}\n" for token in tokens), expected_stdout(case))
                self.assertEqual("".join(f"{error}\n" for error in scanner.errors), expected_stderr(case))

    def test_every_token_type_is_covered(self):
        covered = {record[0] for case in CASES for record in case.tokens}
        self.assertEqual(covered, {token_type.name for token_type in TokenType})

    def test_all_cases_in_source_file_mode(self):
        for case in CASES:
            with self.subTest(case=case.name):
                result = subprocess.run(
                    [sys.executable, "-m", "src.main", "--scan", str(case.path)],
                    cwd=ROOT, text=True, capture_output=True, encoding="utf-8", timeout=10,
                )
                self.assertEqual(result.returncode, 65 if case.errors else 0)
                self.assertEqual(result.stdout, expected_stdout(case))
                self.assertEqual(result.stderr, expected_stderr(case))

    def test_interactive_recovery(self):
        result = subprocess.run(
            [sys.executable, "-m", "src.main", "--scan"], cwd=ROOT,
            input='@\n42\n"oops\n"fixed"\n', text=True,
            capture_output=True, encoding="utf-8", timeout=10,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, (
            "EOF lexeme='' literal=None line=1 column=2\n"
            "NUMBER lexeme='42' literal=42.0 line=1 column=1\n"
            "EOF lexeme='' literal=None line=1 column=3\n"
            "EOF lexeme='' literal=None line=1 column=6\n"
            'STRING lexeme=\'"fixed"\' literal=\'fixed\' line=1 column=1\n'
            "EOF lexeme='' literal=None line=1 column=8\n"
        ))
        self.assertEqual(result.stderr, (
            "[line 1, column 1] Lexical error: Unexpected character '@'.\n"
            "[line 1, column 1] Lexical error: Unterminated string.\n"
        ))

    def test_interactive_whitespace_and_eof(self):
        result = subprocess.run(
            [sys.executable, "-m", "src.main", "--scan"], cwd=ROOT,
            input="\n  \n7\n", text=True, capture_output=True, encoding="utf-8", timeout=10,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, (
            "NUMBER lexeme='7' literal=7.0 line=1 column=1\n"
            "EOF lexeme='' literal=None line=1 column=2\n"
        ))
        self.assertEqual(result.stderr, "")

    def test_interactive_unsupported_whitespace(self):
        result = subprocess.run(
            [sys.executable, "-m", "src.main", "--scan"], cwd=ROOT,
            input="\f\n7\n", text=True, capture_output=True, encoding="utf-8", timeout=10,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, (
            "EOF lexeme='' literal=None line=1 column=2\n"
            "NUMBER lexeme='7' literal=7.0 line=1 column=1\n"
            "EOF lexeme='' literal=None line=1 column=2\n"
        ))
        self.assertEqual(result.stderr, (
            "[line 1, column 1] Lexical error: Unexpected character '\\x0c'.\n"
        ))


if __name__ == "__main__":
    unittest.main()
