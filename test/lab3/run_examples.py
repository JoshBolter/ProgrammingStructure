from pathlib import Path
import sys

from src.parser import Parser
from src.scanner import Scanner
from test.lab3.cases import CASES
from test.lab3.test_parser import INPUTS, case_passed, run_case


def block(value, language="text", empty="(no output)"):
    if not value:
        return empty + "\n"
    return f"```{language}\n{value.rstrip(chr(10))}\n```\n"


def structural_results():
    expression = Parser(Scanner("1 + 2 * 3").scan_tokens()).parse()
    fields = (
        expression.operator.type.name, expression.left.value,
        expression.right.operator.type.name, expression.right.left.value,
        expression.right.right.value,
    )
    values = []
    for source in ["true", "false", "nil", "42", '"hi"']:
        literal = Parser(Scanner(source).scan_tokens()).parse()
        values.append(f"{source}: {type(literal.value).__name__} {literal.value!r}")
    negative = Parser(Scanner("-42").scan_tokens()).parse()
    unary = (
        type(negative).__name__, negative.operator.type.name,
        type(negative.right).__name__, negative.right.value,
    )
    return [
        ("AST fields", "1 + 2 * 3",
         "The addition node has a multiplication node on its right, with numeric literal children.",
         "('PLUS', 1.0, 'STAR', 2.0, 3.0)", repr(fields)),
        ("Literal value types", 'true\nfalse\nnil\n42\n"hi"',
         "Each source is parsed separately, and each literal keeps its intended Python type.",
         'true: bool True\nfalse: bool False\nnil: NoneType None\n42: float 42.0\n"hi": str \'hi\'',
         "\n".join(values)),
        ("Negative number representation", "-42",
         "The minus token remains a unary operator rather than becoming part of the numeric literal.",
         "('Unary', 'MINUS', 'Literal', 42.0)", repr(unary)),
    ]


def main():
    sections = []
    failures = 0
    for case in CASES:
        source = (INPUTS / f"{case.name}.josh").read_text(encoding="utf-8")
        if source != case.source:
            raise ValueError(f"Fixture does not match its expected source: {case.name}")
        result = run_case(case)
        passed = case_passed(case, result)
        failures += not passed
        mode = "interactive input" if case.mode == "repl" else "source-file input"
        expected_stderr_label = "Expected stderr pattern" if case.stderr_pattern else "Expected stderr"
        sections.extend([
            f"## {case.name}\n", f"{case.purpose}\n",
            f"Mode: {mode}. Input file: `test/lab3/inputs/{case.name}.josh`.\n",
            "### Source input\n", block(source, "text", "(empty input)"),
            "### Expected stdout\n", block(case.stdout),
            f"### {expected_stderr_label}\n", block(case.stderr),
            "### Actual stdout\n", block(result.stdout),
            "### Actual stderr\n", block(result.stderr),
            f"Expected exit code: `{case.returncode}`. Actual exit code: `{result.returncode}`.\n",
            f"Result: **{'PASS' if passed else 'FAIL'}**.\n",
        ])
        if case.cause:
            sections.append(f"Explanation: {case.cause}\n")
    properties = structural_results()
    property_failures = 0
    for name, source, purpose, expected, actual in properties:
        passed = expected == actual
        property_failures += not passed
        sections.extend([
            f"## Structural check: {name}\n", f"{purpose}\n",
            "### Source input\n", block(source),
            "### Expected inspection result\n", block(expected),
            "### Actual inspection result\n", block(actual),
            f"Result: **{'PASS' if passed else 'FAIL'}**.\n",
        ])
    report = [
        "# Lab 3 test results\n",
        "These results were captured by running `python -m test.lab3.run_examples` "
        "from the repository root. Expected results are fixed in `test/lab3/cases.py`; "
        "the script does not derive them from the program's output.\n",
        f"Result: **{len(CASES) - failures}/{len(CASES)} example cases passed**. "
        "Standard output and error output are captured separately. "
        "Interactive cases use redirected stdin, so they have no terminal prompt.\n",
        f"The three structural checks also passed {len(properties) - property_failures}/{len(properties)} "
        "comparisons. Their inputs, expectations, and actual inspected values appear at the end.\n",
    ]
    path = Path(__file__).resolve().parents[2] / "report" / "lab3-test-results.md"
    path.write_text("\n".join(report + sections), encoding="utf-8")
    print(f"Lab 3: {len(CASES) - failures}/{len(CASES)} example cases passed.")
    return 1 if failures or property_failures else 0


if __name__ == "__main__":
    sys.exit(main())
