import argparse
import sys
from pathlib import Path

from .ast_printer import AstPrinter
from .errors import Diagnostic
from .parser import Parser
from .scanner import Scanner


class JoshLang:
    def __init__(self, scan_only=False):
        self.scan_only = scan_only

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

        parser = Parser(tokens)
        expression = parser.parse()
        if parser.errors:
            self.report(parser.errors)
            return 65

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
        description="Scan JoshLang tokens or print the AST of one expression."
    )
    arguments.add_argument(
        "--scan", action="store_true", help="print tokens for Lab 1"
    )
    arguments.add_argument("file", nargs="?", help="UTF-8 source file")
    options = arguments.parse_args(argv)
    language = JoshLang(scan_only=options.scan)
    if options.file is not None:
        return language.run_file(options.file)
    return language.run_prompt()


if __name__ == "__main__":
    raise SystemExit(main())
