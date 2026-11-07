from pathlib import Path
import subprocess
import sys
import unittest

from src.parser import Parser
from src.scanner import Scanner
from src.stmt import ExpressionStatement, PrintStatement


ROOT = Path(__file__).resolve().parents[2]
INPUTS = Path(__file__).parent / "inputs"


def run_case(name, *flags):
    return subprocess.run(
        [sys.executable, "-m", "src.main", *flags, str(INPUTS / name)],
        cwd=ROOT, text=True, encoding="utf-8", capture_output=True, timeout=10,
    )


class Lab4Tests(unittest.TestCase):
    def test_assignment_valid_case(self):
        result = run_case("required_success.josh", "--run")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "one\ntrue\n3\nnil\n")
        self.assertEqual(result.stderr, "")

    def test_assignment_error_case(self):
        result = run_case("required_errors.josh", "--run")
        self.assertEqual(result.returncode, 65)
        self.assertEqual(result.stdout, "")
        self.assertEqual(
            result.stderr,
            "[line 2, column 1] Syntax error: Expected ';' after expression.\n"
            "[line 4, column 1] Syntax error: Expected an expression after '+'.\n",
        )

    def test_panic_recovery_executes_following_print(self):
        result = run_case("recovery.josh", "--run")
        self.assertEqual(result.returncode, 65)
        self.assertEqual(result.stdout, "before\nafter\n")
        self.assertIn("Syntax error:", result.stderr)

    def test_panic_recovery_after_missing_semicolon(self):
        result = run_case("missing_semicolon.josh", "--run")
        self.assertEqual(result.returncode, 65)
        self.assertEqual(result.stdout, "preserved\n")
        self.assertIn("Expected ';' after print statement.", result.stderr)

    def test_expression_statements_do_not_print(self):
        result = run_case("expressions.josh", "--run")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "16\ntrue\nhello world\n")
        self.assertEqual(result.stderr, "")

    def test_statement_ast_types(self):
        parser = Parser(Scanner('4 + 2; print "hello";').scan_tokens())
        statements = parser.parse_statements()
        self.assertEqual(parser.errors, [])
        self.assertEqual(len(statements), 2)
        self.assertIsInstance(statements[0], ExpressionStatement)
        self.assertIsInstance(statements[1], PrintStatement)

    def test_recovery_after_bad_group(self):
        result = run_case("recovery_group.josh", "--run")
        self.assertEqual(result.returncode, 65)
        self.assertEqual(result.stdout, "recovered\n")
        self.assertIn("Expected an expression after '+'", result.stderr)

    def test_multiple_errors_and_valid_final_statement(self):
        result = run_case("multiple_errors.josh", "--run")
        self.assertEqual(result.returncode, 65)
        self.assertEqual(result.stdout, "good\n")
        self.assertEqual(result.stderr.count("Syntax error"), 2)

    def test_empty_script(self):
        result = run_case("empty.josh", "--run")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")

    def test_previous_eval_mode_still_works(self):
        result = subprocess.run(
            [sys.executable, "-m", "src.main", "--eval"],
            cwd=ROOT, input="1 + 2 * 3\n", text=True,
            encoding="utf-8", capture_output=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "7\n")
        self.assertEqual(result.stderr, "")

    def test_previous_ast_mode_still_works(self):
        parser = Parser(Scanner("1 + 2 * 3").scan_tokens())
        expression = parser.parse()
        self.assertEqual(parser.errors, [])
        self.assertEqual(expression.operator.lexeme, "+")


if __name__ == "__main__":
    unittest.main()
