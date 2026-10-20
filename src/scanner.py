from math import isfinite

from .errors import Diagnostic
from .tokens import Token
from .token_type import TokenType


KEYWORDS = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}

SINGLE_CHARACTERS = {
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
    "{": TokenType.LEFT_BRACE,
    "}": TokenType.RIGHT_BRACE,
    ",": TokenType.COMMA,
    ".": TokenType.DOT,
    "-": TokenType.MINUS,
    "+": TokenType.PLUS,
    ";": TokenType.SEMICOLON,
    "*": TokenType.STAR,
    "%": TokenType.PERCENT,
}


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.errors: list[Diagnostic] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.start_line = 1
        self.start_column = 1

    def scan_tokens(self) -> list[Token]:
        while not self._at_end():
            self.start = self.current
            self.start_line = self.line
            self.start_column = self.column
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column))
        return self.tokens

    def _scan_token(self) -> None:
        character = self._advance()
        if character in SINGLE_CHARACTERS:
            self._add_token(SINGLE_CHARACTERS[character])
        elif character == "!":
            self._add_token(TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG)
        elif character == "=":
            self._add_token(TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL)
        elif character == "<":
            self._add_token(TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS)
        elif character == ">":
            self._add_token(TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER)
        elif character == "/":
            if self._match("/"):
                while self._peek() != "\n" and not self._at_end():
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)
        elif character in " \t\r\n":
            return
        elif character == '"':
            self._string()
        elif self._is_digit(character):
            self._number()
        elif self._is_alpha(character):
            self._identifier()
        else:
            self._error(f"Unexpected character {character!r}.")

    def _string(self) -> None:
        while self._peek() != '"' and not self._at_end():
            self._advance()
        if self._at_end():
            self._error("Unterminated string.")
            return
        self._advance()
        self._add_token(TokenType.STRING, self.source[self.start + 1:self.current - 1])

    def _number(self) -> None:
        while self._is_digit(self._peek()):
            self._advance()
        if self._peek() == "." and self._is_digit(self._peek_next()):
            self._advance()
            while self._is_digit(self._peek()):
                self._advance()
        value = float(self.source[self.start:self.current])
        if not isfinite(value):
            self._error("Number is outside the supported range.")
            return
        self._add_token(TokenType.NUMBER, value)

    def _identifier(self) -> None:
        while self._is_alpha(self._peek()) or self._is_digit(self._peek()):
            self._advance()
        text = self.source[self.start:self.current]
        self._add_token(KEYWORDS.get(text, TokenType.IDENTIFIER))

    def _add_token(self, token_type: TokenType, literal: object = None) -> None:
        self.tokens.append(Token(
            token_type,
            self.source[self.start:self.current],
            literal,
            self.start_line,
            self.start_column,
        ))

    def _error(self, message: str) -> None:
        self.errors.append(Diagnostic(self.start_line, self.start_column, message))

    def _at_end(self) -> bool:
        return self.current >= len(self.source)

    def _advance(self) -> str:
        character = self.source[self.current]
        self.current += 1
        if character == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return character

    def _match(self, expected: str) -> bool:
        if self._at_end() or self.source[self.current] != expected:
            return False
        self._advance()
        return True

    def _peek(self) -> str:
        return "\0" if self._at_end() else self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    @staticmethod
    def _is_digit(character: str) -> bool:
        return "0" <= character <= "9"

    @staticmethod
    def _is_alpha(character: str) -> bool:
        return "a" <= character <= "z" or "A" <= character <= "Z" or character == "_"
