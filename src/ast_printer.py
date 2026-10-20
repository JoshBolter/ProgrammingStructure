import json

from .expr import Binary, Expr, Grouping, Literal, Unary


class AstPrinter:
    def print(self, expression: Expr) -> str:
        if isinstance(expression, Binary):
            return self._parenthesize(
                expression.operator.lexeme, expression.left, expression.right
            )
        if isinstance(expression, Unary):
            return self._parenthesize(expression.operator.lexeme, expression.right)
        if isinstance(expression, Grouping):
            return self._parenthesize("group", expression.expression)
        if isinstance(expression, Literal):
            value = expression.value
            if value is None:
                return "nil"
            if isinstance(value, bool):
                return "true" if value else "false"
            if isinstance(value, str):
                return json.dumps(value, ensure_ascii=False)
            if isinstance(value, float) and value.is_integer():
                return str(int(value))
            return str(value)
        raise TypeError(f"Unsupported expression: {type(expression).__name__}")

    def _parenthesize(self, name: str, *expressions: Expr) -> str:
        contents = " ".join(self.print(expression) for expression in expressions)
        return f"({name} {contents})"
