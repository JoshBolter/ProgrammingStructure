from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from src.evaluator import EvaluationError, Evaluator
from src.parser import Parser
from src.scanner import Scanner


ROOT = Path(__file__).resolve().parents[1]


def parsed(source):
    scanner = Scanner(source)
    expression = Parser(scanner.scan_tokens()).parse()
    if scanner.errors or expression is None:
        raise AssertionError(f"Test source did not parse: {source!r}")
    return expression


def run_cli(*options, source):
    return subprocess.run(
        [sys.executable, "-m", "src.main", *options],
        input=source, text=True, encoding="utf-8", capture_output=True,
        cwd=ROOT, timeout=10,
    )


class EvaluatorTests(unittest.TestCase):
    def test_midterm_example(self):
        evaluator = Evaluator()
        result = evaluator.evaluate(parsed("1 + 2 / 3 * 4 == 23"))
        self.assertIs(result, False)
        self.assertEqual([step.operator for step in evaluator.steps], ["/", "*", "+", "=="])
        self.assertAlmostEqual(evaluator.steps[0].result, 2 / 3)
        self.assertAlmostEqual(evaluator.steps[1].result, 8 / 3)
        self.assertAlmostEqual(evaluator.steps[2].result, 11 / 3)
        self.assertIs(evaluator.steps[3].result, False)

    def test_arithmetic_and_precedence(self):
        examples = {
            "2 + 3 * 4": 14,
            "(2 + 3) * 4": 20,
            "20 / 5 / 2": 2,
            "17 % 5": 2,
            "10 - 3 - 2": 5,
            "1.5 + 2.25": 3.75,
            "-3 * 2": -6,
            "--3": 3,
            "true + 2 * 3": 7,
        }
        for source, expected in examples.items():
            with self.subTest(source=source):
                self.assertEqual(Evaluator().evaluate(parsed(source)), expected)

    def test_boolean_number_coercion(self):
        examples = {
            "true + 2": 3,
            "false * 12": 0,
            "true / 2": 0.5,
            "-true": -1,
            "true == 1": True,
            "false == 0": True,
            "true == 0": False,
            "false != 1": True,
            "true > false": True,
            "2 > true": True,
            "false <= 0": True,
        }
        for source, expected in examples.items():
            with self.subTest(source=source):
                self.assertEqual(Evaluator().evaluate(parsed(source)), expected)

    def test_equality_and_strings(self):
        examples = {
            '"ab" + "cd"': "abcd",
            '"same" == "same"': True,
            '"same" != "other"': True,
            '"1" == 1': False,
            '"true" == true': False,
            "nil == nil": True,
            "nil != false": True,
            "3 >= 3": True,
            "2 < 1": False,
        }
        for source, expected in examples.items():
            with self.subTest(source=source):
                self.assertEqual(Evaluator().evaluate(parsed(source)), expected)

    def test_logical_not_and_truthiness(self):
        examples = {
            "!false": True,
            "!true": False,
            "!0": True,
            "!1": False,
            "!2": False,
            "!nil": True,
            '!""': False,
            "!!false": False,
        }
        for source, expected in examples.items():
            with self.subTest(source=source):
                self.assertIs(Evaluator().evaluate(parsed(source)), expected)

    def test_trace_resets_between_expressions(self):
        evaluator = Evaluator()
        evaluator.evaluate(parsed("1 + 2 * 3"))
        self.assertEqual(len(evaluator.steps), 2)
        evaluator.evaluate(parsed("true"))
        self.assertEqual(evaluator.steps, [])

    def test_runtime_errors(self):
        bad = {
            "1 / 0": "Division by zero.",
            "2 % false": "Division by zero in remainder.",
            '"x" - 1': "Operand must be a number or boolean.",
            '"x" + 1': "Operand must be a number or boolean.",
            "nil + 1": "Operand must be a number or boolean.",
            '"a" < "b"': "Operand must be a number or boolean.",
        }
        for source, message in bad.items():
            with self.subTest(source=source):
                with self.assertRaises(EvaluationError) as failure:
                    Evaluator().evaluate(parsed(source))
                self.assertIn(message, str(failure.exception))

    def test_overflow_error(self):
        huge_number = "9" * 308
        with self.assertRaisesRegex(EvaluationError, "outside the supported range"):
            Evaluator().evaluate(parsed(f"{huge_number} * 10"))

    def test_eval_repl(self):
        result = run_cli("--eval", source="true == 1\nfalse + 4\n1 + 2 / 3 * 4 == 23\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "true\n4\nfalse\n")
        self.assertEqual(result.stderr, "")

    def test_trace_repl(self):
        result = run_cli("--trace", source="1 + 2 / 3 * 4 == 23\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        lines = result.stdout.splitlines()
        self.assertEqual(len(lines), 5)
        self.assertTrue(lines[0].startswith("1. 2 / 3 -> "))
        self.assertIn(" * 4 -> ", lines[1])
        self.assertIn(" + ", lines[2])
        self.assertIn(" == 23 -> false", lines[3])
        self.assertEqual(lines[4], "Result: false")

    def test_repl_recovers_after_runtime_error(self):
        result = run_cli("--eval", source="1 / 0\n2 + 3\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "5\n")
        self.assertIn("Runtime error: Division by zero.", result.stderr)

    def test_eval_file_and_error_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.josh"
            path.write_text("true + 2", encoding="utf-8")
            valid = run_cli("--eval", str(path), source="")
            self.assertEqual(valid.returncode, 0)
            self.assertEqual(valid.stdout, "3\n")
            path.write_text("1 / 0", encoding="utf-8")
            invalid = run_cli("--eval", str(path), source="")
            self.assertEqual(invalid.returncode, 70)
            self.assertIn("[line 1, column 3] Runtime error", invalid.stderr)

    def test_existing_default_ast_output_is_unchanged(self):
        result = run_cli(source="1 + 2 / 3 * 4 == 23\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "(== (+ 1 (* (/ 2 3) 4)) 23)\n")

    def test_existing_scan_mode_is_unchanged(self):
        result = run_cli("--scan", source="1 + 2\n")
        self.assertEqual(result.returncode, 0)
        self.assertIn("NUMBER lexeme='1'", result.stdout)
        self.assertIn("PLUS lexeme='+'", result.stdout)

    def test_modes_are_exclusive(self):
        result = run_cli("--scan", "--eval", source="1 + 2\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("not allowed with argument", result.stderr)


if __name__ == "__main__":
    unittest.main()
