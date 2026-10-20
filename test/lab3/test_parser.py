from pathlib import Path
import re
import subprocess
import sys
import unittest

from src.expr import Binary, Literal, Unary
from src.parser import Parser
from src.scanner import Scanner
from src.token_type import TokenType
from test.lab3.cases import CASES


ROOT = Path(__file__).resolve().parents[2]
INPUTS = Path(__file__).parent / "inputs"


def run_case(case):
    command = [sys.executable, "-m", "src.main"]
    if case.mode == "file":
        command.append(str(INPUTS / f"{case.name}.josh"))
    return subprocess.run(
        command, cwd=ROOT, input=case.source if case.mode == "repl" else None,
        text=True, encoding="utf-8", capture_output=True, timeout=10,
    )


def case_passed(case, result):
    stderr_matches = (
        re.fullmatch(case.stderr, result.stderr) is not None
        if case.stderr_pattern else result.stderr == case.stderr
    )
    return (
        result.stdout == case.stdout and stderr_matches
        and result.returncode == case.returncode
    )


class ParserTests(unittest.TestCase):
    def test_binary_ast_fields(self):
        scanner = Scanner("1 + 2 * 3")
        parser = Parser(scanner.scan_tokens())
        expression = parser.parse()
        self.assertEqual(scanner.errors, [])
        self.assertEqual(parser.errors, [])
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.PLUS)
        self.assertEqual(expression.left, Literal(1.0))
        self.assertIsInstance(expression.right, Binary)
        self.assertEqual(expression.right.operator.type, TokenType.STAR)
        self.assertEqual(expression.right.left, Literal(2.0))
        self.assertEqual(expression.right.right, Literal(3.0))

    def test_boolean_nil_and_numeric_value_types(self):
        for source, expected_type, expected_value in [
            ("true", bool, True), ("false", bool, False),
            ("nil", type(None), None), ("42", float, 42.0),
            ('"hi"', str, "hi"),
        ]:
            with self.subTest(source=source):
                parser = Parser(Scanner(source).scan_tokens())
                expression = parser.parse()
                self.assertEqual(parser.errors, [])
                self.assertIs(type(expression.value), expected_type)
                self.assertEqual(expression.value, expected_value)

    def test_negative_number_is_unary(self):
        parser = Parser(Scanner("-42").scan_tokens())
        expression = parser.parse()
        self.assertEqual(parser.errors, [])
        self.assertIsInstance(expression, Unary)
        self.assertEqual(expression.operator.type, TokenType.MINUS)
        self.assertEqual(expression.right, Literal(42.0))


def make_test(case):
    def test(self):
        fixture = INPUTS / f"{case.name}.josh"
        self.assertEqual(fixture.read_text(encoding="utf-8"), case.source)
        result = run_case(case)
        self.assertEqual(result.stdout, case.stdout)
        if case.stderr_pattern:
            self.assertIsNotNone(re.fullmatch(case.stderr, result.stderr))
        else:
            self.assertEqual(result.stderr, case.stderr)
        self.assertEqual(result.returncode, case.returncode)
    return test


for case in CASES:
    setattr(ParserTests, f"test_{case.name}", make_test(case))


if __name__ == "__main__":
    unittest.main()
