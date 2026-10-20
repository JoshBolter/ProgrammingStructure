import argparse
import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from src.ast_printer import AstPrinter
from src.expr import Binary, Expr, Grouping, Literal, Unary
from src.token_type import TokenType
from src.tokens import Token


@dataclass(frozen=True)
class Example:
    name: str
    purpose: str
    build: Callable[[], Expr]
    expected: str


def textbook_nested():
    return Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123.0)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )


def string_addition():
    return Binary(
        Literal("hello"),
        Token(TokenType.PLUS, "+", None, 1),
        Literal(" world"),
    )


def subtraction():
    return Binary(
        Literal(10.0), Token(TokenType.MINUS, "-", None, 1), Literal(3.0)
    )


def division():
    return Binary(
        Literal(20.0), Token(TokenType.SLASH, "/", None, 1), Literal(4.0)
    )


def remainder():
    return Binary(
        Literal(17.0), Token(TokenType.PERCENT, "%", None, 1), Literal(5.0)
    )


def unary_not():
    return Unary(Token(TokenType.BANG, "!", None, 1), Literal(True))


def nil_equality():
    return Binary(
        Literal(None), Token(TokenType.EQUAL_EQUAL, "==", None, 1), Literal(None)
    )


def boolean_inequality():
    return Binary(
        Literal(True), Token(TokenType.BANG_EQUAL, "!=", None, 1), Literal(False)
    )


def less_than():
    return Binary(
        Literal(1.0), Token(TokenType.LESS, "<", None, 1), Literal(2.0)
    )


def less_equal():
    return Binary(
        Literal(1.0), Token(TokenType.LESS_EQUAL, "<=", None, 1), Literal(1.0)
    )


def greater_than():
    return Binary(
        Literal(3.0), Token(TokenType.GREATER, ">", None, 1), Literal(2.0)
    )


def greater_equal():
    return Binary(
        Literal(3.0), Token(TokenType.GREATER_EQUAL, ">=", None, 1), Literal(3.0)
    )


def left_associative_subtraction():
    return Binary(
        Binary(
            Literal(10.0), Token(TokenType.MINUS, "-", None, 1), Literal(3.0)
        ),
        Token(TokenType.MINUS, "-", None, 1),
        Literal(2.0),
    )


def nested_grouping():
    return Grouping(
        Grouping(
            Binary(
                Literal(2.0), Token(TokenType.PLUS, "+", None, 1), Literal(3.0)
            )
        )
    )


def double_not():
    return Unary(
        Token(TokenType.BANG, "!", None, 1),
        Unary(Token(TokenType.BANG, "!", None, 1), Literal(False)),
    )


def empty_string():
    return Literal("")


def string_true():
    return Literal("true")


def multiline_string():
    return Literal("line one\nline two")


def zero():
    return Literal(0.0)


def mixed_precedence():
    return Binary(
        Binary(
            Literal(1.0),
            Token(TokenType.PLUS, "+", None, 1),
            Binary(
                Literal(2.0), Token(TokenType.STAR, "*", None, 1), Literal(3.0)
            ),
        ),
        Token(TokenType.EQUAL_EQUAL, "==", None, 1),
        Literal(7.0),
    )


EXAMPLES = (
    Example(
        "textbook_nested",
        "Combine all four node classes and both whole and fractional numbers.",
        textbook_nested,
        "(* (- 123) (group 45.67))",
    ),
    Example(
        "string_addition",
        "Print a binary plus expression with quoted string literals.",
        string_addition,
        '(+ "hello" " world")',
    ),
    Example("subtraction", "Print binary subtraction.", subtraction, "(- 10 3)"),
    Example("division", "Print division.", division, "(/ 20 4)"),
    Example("remainder", "Print JoshLang's added % operator.", remainder, "(% 17 5)"),
    Example("unary_not", "Print unary ! and a true literal.", unary_not, "(! true)"),
    Example(
        "nil_equality", "Print == and nil values.", nil_equality, "(== nil nil)"
    ),
    Example(
        "boolean_inequality",
        "Print != and preserve both boolean spellings.",
        boolean_inequality,
        "(!= true false)",
    ),
    Example("less_than", "Print <.", less_than, "(< 1 2)"),
    Example("less_equal", "Print <=.", less_equal, "(<= 1 1)"),
    Example("greater_than", "Print >.", greater_than, "(> 3 2)"),
    Example("greater_equal", "Print >=.", greater_equal, "(>= 3 3)"),
    Example(
        "left_associative_subtraction",
        "Preserve a left-nested tree for 10 - 3 - 2.",
        left_associative_subtraction,
        "(- (- 10 3) 2)",
    ),
    Example(
        "nested_grouping",
        "Keep both explicit grouping nodes.",
        nested_grouping,
        "(group (group (+ 2 3)))",
    ),
    Example(
        "double_not",
        "Preserve nested unary expressions.",
        double_not,
        "(! (! false))",
    ),
    Example("empty_string", "Keep an empty string visible.", empty_string, '""'),
    Example(
        "string_true",
        "Distinguish the string true from the boolean true.",
        string_true,
        '"true"',
    ),
    Example(
        "multiline_string",
        "Display a newline without splitting the printed tree across lines.",
        multiline_string,
        '"line one\\nline two"',
    ),
    Example("zero", "Print a whole-valued float without .0.", zero, "0"),
    Example(
        "mixed_precedence",
        "Preserve multiplication inside addition inside equality.",
        mixed_precedence,
        "(== (+ 1 (* 2 3)) 7)",
    ),
)


def run_examples(write_report=False):
    printer = AstPrinter()
    results = []
    for example in EXAMPLES:
        actual = printer.print(example.build())
        passed = actual == example.expected
        results.append((example, actual, passed))
        print(f"{example.name}: {'PASS' if passed else 'FAIL'}")
        print(actual)

    if write_report:
        fence = chr(96) * 3
        lines = [
            "# Lab 2 test results",
            "",
            "These results were produced by running python -m test.lab2.examples --report.",
            "Each expected result is written separately from the printer. "
            "The actual results below come from running the hard-coded constructors.",
            "",
            f"Result: **{sum(passed for _, _, passed in results)}/{len(results)} examples passed.**",
            "",
        ]
        for example, actual, passed in results:
            lines.extend(
                [
                    f"## {example.name}",
                    "",
                    f"Purpose: {example.purpose}",
                    "",
                    "Hard-coded AST:",
                    "",
                    fence + "python",
                    inspect.getsource(example.build).rstrip(),
                    fence,
                    "",
                    "Expected:",
                    "",
                    fence + "text",
                    example.expected,
                    fence,
                    "",
                    "Actual:",
                    "",
                    fence + "text",
                    actual,
                    fence,
                    "",
                    f"Matches expectations: **{'Yes' if passed else 'No'}**.",
                    "",
                ]
            )
        report = Path(__file__).resolve().parents[2] / "report" / "lab2-test-results.md"
        report.write_text("\n".join(lines), encoding="utf-8")
        print(f"Report written: {report.name}")

    return 0 if all(passed for _, _, passed in results) else 1


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "--report", action="store_true", help="Regenerate the saved test results."
    )
    arguments = argument_parser.parse_args()
    raise SystemExit(run_examples(arguments.report))
