from .errors import Diagnostic
from .expr import Binary, Grouping, Literal, Unary
from .token_type import TokenType
from .stmt import ExpressionStatement, PrintStatement


class _ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.errors = []

    def parse(self):
        try:
            expression = self._expression()
            if not self._check(TokenType.EOF):
                token = self._peek()
                if token.type == TokenType.RIGHT_PAREN:
                    self._fail(token, "Unexpected ')' without a matching '('.")
                self._fail(
                    token, f"Unexpected token after expression: {token.lexeme!r}."
                )
            return expression
        except _ParseError:
            return None
        except RecursionError:
            token = self._peek()
            self.errors.append(Diagnostic(
                token.line, token.column, "Expression is too deeply nested.",
                "Syntax error",
            ))
            return None

    def parse_statements(self):
        statements = []
        while not self._check(TokenType.EOF):
            try:
                statements.append(self._statement())
            except _ParseError:
                self._synchronize()
            except RecursionError:
                token = self._peek()
                self.errors.append(Diagnostic(
                    token.line, token.column,
                    "Expression is too deeply nested.", "Syntax error",
                ))
                self._synchronize()
        return statements

    def _statement(self):
        if self._match(TokenType.PRINT):
            expression = self._expression()
            self._consume(TokenType.SEMICOLON, "Expected ';' after print statement.")
            return PrintStatement(expression)
        expression = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after expression.")
        return ExpressionStatement(expression)

    def _consume(self, token_type, message):
        if self._match(token_type):
            return self._previous()
        self._fail(self._peek(), message)

    def _synchronize(self):
        if self._check(TokenType.SEMICOLON):
            self.current += 1
            return
        while not self._check(TokenType.EOF):
            if self.current > 0 and self._previous().type == TokenType.SEMICOLON:
                return
            if self._peek().type in {
                TokenType.PRINT, TokenType.NUMBER, TokenType.STRING,
                TokenType.TRUE, TokenType.FALSE, TokenType.NIL,
                TokenType.LEFT_PAREN, TokenType.BANG, TokenType.MINUS,
            }:
                return
            self.current += 1

    def _expression(self):
        return self._equality()

    def _equality(self):
        return self._binary(
            self._comparison, TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL
        )

    def _comparison(self):
        return self._binary(
            self._term, TokenType.GREATER, TokenType.GREATER_EQUAL,
            TokenType.LESS, TokenType.LESS_EQUAL,
        )

    def _term(self):
        return self._binary(self._factor, TokenType.MINUS, TokenType.PLUS)

    def _factor(self):
        return self._binary(
            self._unary, TokenType.SLASH, TokenType.STAR, TokenType.PERCENT
        )

    def _binary(self, operand, *operators):
        expression = operand()
        while self._match(*operators):
            operator = self._previous()
            self._require_operand(operator)
            expression = Binary(expression, operator, operand())
        return expression

    def _unary(self):
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            self._require_operand(operator)
            return Unary(operator, self._unary())
        return self._primary()

    def _primary(self):
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.NIL):
            return Literal(None)
        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)
        if self._match(TokenType.LEFT_PAREN):
            opening = self._previous()
            if self._check(TokenType.RIGHT_PAREN):
                self._fail(self._peek(), "Expected an expression inside parentheses.")
            expression = self._expression()
            if not self._match(TokenType.RIGHT_PAREN):
                self._fail(
                    self._peek(),
                    f"Expected ')' to close '(' from line {opening.line}, "
                    f"column {opening.column}.",
                )
            return Grouping(expression)

        token = self._peek()
        if token.type == TokenType.EOF:
            self._fail(token, "Expected an expression before end of input.")
        if token.type == TokenType.RIGHT_PAREN:
            self._fail(token, "Unexpected ')' without a matching '('.")
        if token.type in {
            TokenType.PLUS, TokenType.SLASH, TokenType.STAR, TokenType.PERCENT,
            TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL, TokenType.GREATER,
            TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL,
        }:
            self._fail(token, f"Missing left operand before {token.lexeme!r}.")
        self._fail(token, f"Expected an expression; found {token.lexeme!r}.")

    def _require_operand(self, operator):
        if self._peek().type not in {
            TokenType.NUMBER, TokenType.STRING, TokenType.TRUE, TokenType.FALSE,
            TokenType.NIL, TokenType.LEFT_PAREN, TokenType.BANG, TokenType.MINUS,
        }:
            self._fail(
                self._peek(), f"Expected an expression after {operator.lexeme!r}."
            )

    def _match(self, *types):
        if self._peek().type in types:
            self.current += 1
            return True
        return False

    def _check(self, token_type):
        return self._peek().type == token_type

    def _peek(self):
        return self.tokens[self.current]

    def _previous(self):
        return self.tokens[self.current - 1]

    def _fail(self, token, message):
        self.errors.append(Diagnostic(
            token.line, token.column, message, "Syntax error"
        ))
        raise _ParseError()
