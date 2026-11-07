import argparse
import sys
from pathlib import Path

from .ast_printer import AstPrinter
from .errors import Diagnostic
from .evaluator import EvaluationError, Evaluator
from .expr import Literal
from .parser import Parser
from .scanner import Scanner
from .stmt import PrintStatement


def format_value(value):
    return AstPrinter().print(Literal(value))


def format_print_value(value):
    return value if isinstance(value, str) else format_value(value)


class JoshLang:
    def __init__(self, scan_only=False, evaluate=False, trace=False,
                 run_statements=False):
        self.scan_only = scan_only
        self.evaluate = evaluate or trace
        self.trace = trace
        self.run_statements = run_statements

    def run(self, source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        if self.scan_only:
            for token in tokens:
                print(token)
            self.report(scanner.errors)
            return 65 if scanner.errors else 0

        if scanner.errors:
            self.report(scanner.errors)
            return 65

        if self.run_statements:
            parser = Parser(tokens)
            statements = parser.parse_statements()
            self.report(parser.errors)
            evaluator = Evaluator()
            for statement in statements:
                try:
                    result = evaluator.evaluate(statement.expression)
                except EvaluationError as error:
                    print(error, file=sys.stderr)
                    return 70
                if isinstance(statement, PrintStatement):
                    print(format_print_value(result))
            return 65 if parser.errors else 0

        parser = Parser(tokens)
        expression = parser.parse()
        if parser.errors:
            self.report(parser.errors)
            return 65

        if self.evaluate:
            evaluator = Evaluator()
            try:
                result = evaluator.evaluate(expression)
            except EvaluationError as error:
                print(error, file=sys.stderr)
                return 70
            if self.trace:
                for index, step in enumerate(evaluator.steps, start=1):
                    values = [format_value(value) for value in step.operands]
                    if len(values) == 1:
                        operation = f"{step.operator}{values[0]}"
                    else:
                        operation = f"{values[0]} {step.operator} {values[1]}"
                    print(f"{index}. {operation} -> {format_value(step.result)}")
                print(f"Result: {format_value(result)}")
            else:
                print(format_value(result))
            return 0

        try:
            output = AstPrinter().print(expression)
        except RecursionError:
            token = tokens[0]
            self.report([Diagnostic(
                token.line,
                token.column,
                "Expression is too deeply nested to print.",
                "Syntax error",
            )])
            return 65

        print(output)
        return 0

    def run_file(self, path):
        try:
            source = Path(path).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            print(f"Could not read {str(path)!r}: {error}", file=sys.stderr)
            return 74
        return self.run(source)

    def run_prompt(self):
        prompt = "josh> " if sys.stdin.isatty() else ""
        while True:
            try:
                line = input(prompt)
            except (EOFError, KeyboardInterrupt):
                if prompt:
                    print()
                return 0
            if line.strip(" \t\r\n"):
                self.run(line)

    @staticmethod
    def report(errors):
        for error in errors:
            print(error, file=sys.stderr)


def main(argv=None):
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors=stream.errors)

    arguments = argparse.ArgumentParser(
        description="Scan tokens, print an AST, evaluate an expression, or run statements."
    )
    mode = arguments.add_mutually_exclusive_group()
    mode.add_argument(
        "--scan", action="store_true", help="print tokens for Lab 1"
    )
    mode.add_argument(
        "--eval", action="store_true", help="evaluate expressions and print results"
    )
    mode.add_argument(
        "--trace", action="store_true",
        help="evaluate expressions and show intermediate results in evaluation order"
    )
    mode.add_argument(
        "--run", action="store_true",
        help="execute print and expression statements for Lab 4"
    )
    arguments.add_argument("file", nargs="?", help="UTF-8 source file")
    options = arguments.parse_args(argv)
    language = JoshLang(scan_only=options.scan, evaluate=options.eval,
                        trace=options.trace, run_statements=options.run)
    if options.file is not None:
        return language.run_file(options.file)
    return language.run_prompt()


if __name__ == "__main__":
    raise SystemExit(main())
