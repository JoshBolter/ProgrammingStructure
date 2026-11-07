from dataclasses import dataclass
from math import isfinite

from .expr import Binary, Grouping, Literal, Unary
from .token_type import TokenType


@dataclass(frozen=True)
class EvaluationStep:
    operator: str
    operands: tuple[object, ...]
    result: object


class EvaluationError(Exception):
    def __init__(self, operator, message):
        super().__init__(
            f"[line {operator.line}, column {operator.column}] Runtime error: {message}"
        )


class Evaluator:
    def __init__(self):
        self.steps: list[EvaluationStep] = []

    def evaluate(self, expression):
        self.steps.clear()
        return self._evaluate(expression)

    def _evaluate(self, expression):
        if isinstance(expression, Literal):
            return expression.value
        if isinstance(expression, Grouping):
            return self._evaluate(expression.expression)
        if isinstance(expression, Unary):
            right = self._evaluate(expression.right)
            operator = expression.operator
            if operator.type == TokenType.MINUS:
                result = -self._number(right, operator)
            elif operator.type == TokenType.BANG:
                result = not self._truthy(right)
            else:
                raise EvaluationError(operator, "Unsupported unary operator.")
            self._record(operator, (right,), result)
            return result
        if isinstance(expression, Binary):
            left = self._evaluate(expression.left)
            right = self._evaluate(expression.right)
            operator = expression.operator
            result = self._binary(operator, left, right)
            self._record(operator, (left, right), result)
            return result
        raise TypeError(f"Unsupported expression: {type(expression).__name__}")

    def _binary(self, operator, left, right):
        kind = operator.type
        if kind == TokenType.EQUAL_EQUAL:
            return self._equal(left, right)
        if kind == TokenType.BANG_EQUAL:
            return not self._equal(left, right)
        if kind == TokenType.PLUS and isinstance(left, str) and isinstance(right, str):
            return left + right
        if kind in {
            TokenType.PLUS, TokenType.MINUS, TokenType.STAR,
            TokenType.SLASH, TokenType.PERCENT,
            TokenType.GREATER, TokenType.GREATER_EQUAL,
            TokenType.LESS, TokenType.LESS_EQUAL,
        }:
            a = self._number(left, operator)
            b = self._number(right, operator)
            if kind == TokenType.PLUS:
                result = a + b
            elif kind == TokenType.MINUS:
                result = a - b
            elif kind == TokenType.STAR:
                result = a * b
            elif kind == TokenType.SLASH:
                if b == 0:
                    raise EvaluationError(operator, "Division by zero.")
                result = a / b
            elif kind == TokenType.PERCENT:
                if b == 0:
                    raise EvaluationError(operator, "Division by zero in remainder.")
                result = a % b
            elif kind == TokenType.GREATER:
                return a > b
            elif kind == TokenType.GREATER_EQUAL:
                return a >= b
            elif kind == TokenType.LESS:
                return a < b
            else:
                return a <= b
            if not isfinite(result):
                raise EvaluationError(operator, "Numeric result is outside the supported range.")
            return result
        raise EvaluationError(operator, "Unsupported binary operator.")

    @staticmethod
    def _number(value, operator):
        if isinstance(value, bool):
            return float(value)
        if isinstance(value, (int, float)):
            return float(value)
        raise EvaluationError(operator, "Operand must be a number or boolean.")

    @staticmethod
    def _truthy(value):
        if value is None or value is False:
            return False
        if isinstance(value, (int, float)) and value == 0:
            return False
        return True

    @staticmethod
    def _equal(left, right):
        numeric = (int, float, bool)
        if isinstance(left, numeric) and isinstance(right, numeric):
            return float(left) == float(right)
        if isinstance(left, str) and isinstance(right, str):
            return left == right
        return left is None and right is None

    def _record(self, operator, operands, result):
        self.steps.append(EvaluationStep(operator.lexeme, operands, result))
