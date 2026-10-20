from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Case:
    name: str
    purpose: str
    source: str
    tokens: tuple
    errors: tuple = ()

    @property
    def path(self) -> Path:
        return Path(__file__).parent / "inputs" / f"{self.name}.josh"


def record(kind, lexeme, value=None, line=1, column=1):
    return kind, lexeme, value, line, column


def eof(line=1, column=1):
    return record("EOF", "", line=line, column=column)


keyword_pairs = (
    ("and", "AND"), ("class", "CLASS"), ("else", "ELSE"),
    ("false", "FALSE"), ("for", "FOR"), ("fun", "FUN"),
    ("if", "IF"), ("nil", "NIL"), ("or", "OR"),
    ("print", "PRINT"), ("return", "RETURN"), ("super", "SUPER"),
    ("this", "THIS"), ("true", "TRUE"), ("var", "VAR"), ("while", "WHILE"),
)
identifier_values = ("a", "Z", "_", "snake_case", "value2", "varname", "True", "FALSE", "nilValue", "anderson")
number_values = (("0", 0.0), ("0007", 7.0), ("42", 42.0), ("3.14", 3.14), ("0.5", 0.5), ("4294967296", 4294967296.0))
string_values = ("", "hello world", "true", "nil", "// not a comment", "@ é")

CASES = (
    Case("punctuation", "Scan every single-character punctuation/operator; /* is not a block comment.", "(){},.-+;/*%", (
        record("LEFT_PAREN", "(", column=1), record("RIGHT_PAREN", ")", column=2),
        record("LEFT_BRACE", "{", column=3), record("RIGHT_BRACE", "}", column=4),
        record("COMMA", ",", column=5), record("DOT", ".", column=6),
        record("MINUS", "-", column=7), record("PLUS", "+", column=8),
        record("SEMICOLON", ";", column=9), record("SLASH", "/", column=10),
        record("STAR", "*", column=11), record("PERCENT", "%", column=12), eof(column=13),
    )),
    Case("operators", "Distinguish one-character operators from their longest two-character matches.", "! != = == > >= < <=", (
        record("BANG", "!", column=1), record("BANG_EQUAL", "!=", column=3),
        record("EQUAL", "=", column=6), record("EQUAL_EQUAL", "==", column=8),
        record("GREATER", ">", column=11), record("GREATER_EQUAL", ">=", column=13),
        record("LESS", "<", column=16), record("LESS_EQUAL", "<=", column=18), eof(column=20),
    )),
    Case("keywords", "Recognize every reserved keyword and preserve each line number.", "\n".join(word for word, _ in keyword_pairs) + "\n",
         tuple(record(kind, word, line=i) for i, (word, kind) in enumerate(keyword_pairs, 1)) + (eof(line=17),)),
    Case("identifiers", "Allow ASCII letters, underscores and later digits; distinguish case and keyword prefixes.", "\n".join(identifier_values) + "\n",
         tuple(record("IDENTIFIER", word, line=i) for i, word in enumerate(identifier_values, 1)) + (eof(line=11),)),
    Case("numbers", "Convert whole and decimal number lexemes to float, including zero and leading zeros.", "\n".join(word for word, _ in number_values) + "\n",
         tuple(record("NUMBER", word, value, line=i) for i, (word, value) in enumerate(number_values, 1)) + (eof(line=7),)),
    Case("strings", "Keep empty strings, spaces, keyword text, comment markers and Unicode inside strings.", "\n".join('"' + value + '"' for value in string_values) + "\n",
         tuple(record("STRING", '"' + value + '"', value, line=i) for i, value in enumerate(string_values, 1)) + (eof(line=7),)),
    Case("raw_backslash", "Treat backslash-n as two ordinary characters, not an escape sequence.", r'"a\nb"', (
        record("STRING", r'"a\nb"', r"a\nb"), eof(column=7),
    )),
    Case("multiline_string", "Keep a newline inside a string and locate the next token correctly.", '"first\nsecond"\n42', (
        record("STRING", '"first\nsecond"', "first\nsecond"), record("NUMBER", "42", 42.0, line=3), eof(line=3, column=3),
    )),
    Case("line_comments", "Ignore comment contents, even apparent errors, and end a comment at newline or EOF.", '1 // ignored @ " \n2//end', (
        record("NUMBER", "1", 1.0), record("NUMBER", "2", 2.0, line=2), eof(line=2, column=7),
    )),
    Case("whitespace", "Ignore spaces, tabs and CRLF while retaining later token positions.", " \t\r\n42\t+\t1\n", (
        record("NUMBER", "42", 42.0, line=2), record("PLUS", "+", line=2, column=4),
        record("NUMBER", "1", 1.0, line=2, column=6), eof(line=3),
    )),
    Case("empty", "Produce exactly EOF for an empty source file.", "", (eof(),)),
    Case("comment_only", "Produce EOF when the entire file is a comment without a final newline.", "// no tokens", (eof(column=13),)),
    Case("keyword_boundaries", "Match full identifiers before testing whether they are keywords.", "varx != nilx", (
        record("IDENTIFIER", "varx"), record("BANG_EQUAL", "!=", column=6), record("IDENTIFIER", "nilx", column=9), eof(column=13),
    )),
    Case("number_boundaries", "Keep decimal points and exponent-like text outside the number grammar as separate tokens.", ".5 1. 1e3 1.2.3 -7", (
        record("DOT", "."), record("NUMBER", "5", 5.0, column=2), record("NUMBER", "1", 1.0, column=4),
        record("DOT", ".", column=5), record("NUMBER", "1", 1.0, column=7), record("IDENTIFIER", "e3", column=8),
        record("NUMBER", "1.2", 1.2, column=11), record("DOT", ".", column=14), record("NUMBER", "3", 3.0, column=15),
        record("MINUS", "-", column=17), record("NUMBER", "7", 7.0, column=18), eof(column=19),
    )),
    Case("adjacent_tokens", "Scan an expression without requiring spaces between tokens.", "1+2*3==7", (
        record("NUMBER", "1", 1.0), record("PLUS", "+", column=2), record("NUMBER", "2", 2.0, column=3),
        record("STAR", "*", column=4), record("NUMBER", "3", 3.0, column=5), record("EQUAL_EQUAL", "==", column=6),
        record("NUMBER", "7", 7.0, column=8), eof(column=9),
    )),
    Case("slash_or_comment", "Distinguish division tokens from the // comment prefix.", "/ //ignored\n/", (
        record("SLASH", "/"), record("SLASH", "/", line=2), eof(line=2, column=2),
    )),
    Case("unexpected_characters", "Report multiple unexpected characters and continue scanning later tokens.", "1 @ 2 # 3", (
        record("NUMBER", "1", 1.0), record("NUMBER", "2", 2.0, column=5), record("NUMBER", "3", 3.0, column=9), eof(column=10),
    ), ((1, 3, "Unexpected character '@'."), (1, 7, "Unexpected character '#'."))),
    Case("unicode_identifier", "Reject non-ASCII characters in identifiers.", "café", (
        record("IDENTIFIER", "caf"), eof(column=5),
    ), ((1, 4, "Unexpected character 'é'."),)),
    Case("unicode_digits", "Reject non-ASCII digits instead of silently accepting them as numbers.", "１２", (eof(column=3),), (
        (1, 1, "Unexpected character '１'."), (1, 2, "Unexpected character '２'."),
    )),
    Case("unterminated_string", "Report a missing closing quote at the opening quote's position.", '"hello', (eof(column=7),), (
        (1, 1, "Unterminated string."),
    )),
    Case("unterminated_multiline", "Locate an unterminated multiline string at its opening quote.", '\n  "hello\nworld', (eof(line=3, column=6),), (
        (2, 3, "Unterminated string."),
    )),
    Case("number_overflow", "Report a number that converts to infinity instead of storing an infinite literal.", "9" * 400, (eof(column=401),), (
        (1, 1, "Number is outside the supported range."),
    )),
    Case("form_feed", "Reject form feed because the whitespace rule only allows space, tab, CR and LF.", "1\f2", (
        record("NUMBER", "1", 1.0), record("NUMBER", "2", 2.0, column=3), eof(column=4),
    ), ((1, 2, "Unexpected character '\\x0c'."),)),
    Case("identifier_digit_boundary", "Allow digits after an identifier start and end a number before letters.", "_0 123abc", (
        record("IDENTIFIER", "_0"), record("NUMBER", "123", 123.0, column=4), record("IDENTIFIER", "abc", column=7), eof(column=10),
    )),
    Case("leading_zero_decimal", "Keep the raw number text separately from its converted literal.", "000.500", (
        record("NUMBER", "000.500", 0.5), eof(column=8),
    )),
)


def expected_stdout(case):
    return "".join(
        f"{kind} lexeme={lexeme!r} literal={value!r} line={line} column={column}\n"
        for kind, lexeme, value, line, column in case.tokens
    )


def expected_stderr(case):
    return "".join(
        f"[line {line}, column {column}] Lexical error: {message}\n"
        for line, column, message in case.errors
    )
