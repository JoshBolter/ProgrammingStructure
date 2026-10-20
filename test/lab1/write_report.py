from pathlib import Path
import subprocess
import sys

from test.lab1.cases import CASES, expected_stderr, expected_stdout


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "report" / "lab1-test-results.md"


def block(value):
    return "```text\n" + (value.rstrip("\n") if value else "(empty)") + "\n```\n"


def record_result(name, purpose, source, command, expected_out, expected_err, expected_code, result):
    passed = (result.stdout, result.stderr, result.returncode) == (expected_out, expected_err, expected_code)
    lines = [f"## {name}\n", f"{purpose}\n", "**Source input:**\n", block(source)]
    if any(character in source for character in ("\r", "\t", "\f")) or not source:
        lines.extend(["**Exact Python representation of input:**\n", block(repr(source))])
    lines.extend([
        "**Command:**\n", "```bash\n" + command + "\n```\n",
        "**Expected stdout:**\n", block(expected_out),
        "**Actual stdout:**\n", block(result.stdout),
        "**Expected stderr:**\n", block(expected_err),
        "**Actual stderr:**\n", block(result.stderr),
        f"**Exit code:** expected `{expected_code}`; actual `{result.returncode}`.\n",
        f"**Result:** {'PASS' if passed else 'FAIL'}.\n",
    ])
    return "\n".join(lines), passed


def main():
    output = [
        "# Lab 1 test results\n",
        "These are the expected results and captured output from the scanner's command-line entry point. "
        "The expected token records and diagnostics are specified in `test/lab1/cases.py`; "
        "the actual output is captured by `test/lab1/write_report.py`.\n",
        "I ran each of the 25 scanner cases as a source file and also checked three interactive sessions. "
        "The unit tests separately compare every token field and verify coverage of all 40 token types.\n",
    ]
    results = []
    for case in CASES:
        command = [sys.executable, "-m", "src.main", "--scan", str(case.path)]
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, encoding="utf-8", timeout=10)
        content, passed = record_result(
            case.name, case.purpose, case.source,
            f"python -m src.main --scan test/lab1/inputs/{case.name}.josh",
            expected_stdout(case), expected_stderr(case), 65 if case.errors else 0, result,
        )
        output.append(content)
        results.append(passed)

    sessions = (
        (
            "interactive_recovery", "Recover from both an unexpected character and an unterminated string, then continue scanning.",
            '@\n42\n"oops\n"fixed"\n',
            "EOF lexeme='' literal=None line=1 column=2\n"
            "NUMBER lexeme='42' literal=42.0 line=1 column=1\n"
            "EOF lexeme='' literal=None line=1 column=3\n"
            "EOF lexeme='' literal=None line=1 column=6\n"
            'STRING lexeme=\'"fixed"\' literal=\'fixed\' line=1 column=1\n'
            "EOF lexeme='' literal=None line=1 column=8\n",
            "[line 1, column 1] Lexical error: Unexpected character '@'.\n"
            "[line 1, column 1] Lexical error: Unterminated string.\n",
        ),
        (
            "interactive_blank_lines", "Ignore blank input, scan the next line, and exit normally at end of input.",
            "\n  \n7\n",
            "NUMBER lexeme='7' literal=7.0 line=1 column=1\n"
            "EOF lexeme='' literal=None line=1 column=2\n", "",
        ),
        (
            "interactive_unsupported_whitespace", "Reject a form-feed-only input line and recover on the next line.",
            "\f\n7\n",
            "EOF lexeme='' literal=None line=1 column=2\n"
            "NUMBER lexeme='7' literal=7.0 line=1 column=1\n"
            "EOF lexeme='' literal=None line=1 column=2\n",
            "[line 1, column 1] Lexical error: Unexpected character '\\x0c'.\n",
        ),
    )
    for name, purpose, source, expected_out, expected_err in sessions:
        result = subprocess.run(
            [sys.executable, "-m", "src.main", "--scan"], cwd=ROOT, input=source,
            text=True, capture_output=True, encoding="utf-8", timeout=10,
        )
        content, passed = record_result(
            name, purpose, source, "python -m src.main --scan (enter each input line)",
            expected_out, expected_err, 0, result,
        )
        output.append(content)
        results.append(passed)
    output.append(f"## Summary\n\n{sum(results)} of {len(results)} recorded command-line runs matched the expected output and exit code.\n")
    REPORT.write_text("\n".join(output), encoding="utf-8")
    print(f"Wrote {REPORT.relative_to(ROOT)}: {sum(results)}/{len(results)} command-line runs passed.")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
