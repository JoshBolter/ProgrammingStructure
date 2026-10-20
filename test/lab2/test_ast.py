import unittest

from src.ast_printer import AstPrinter
from src.expr import Binary, Expr, Grouping, Literal, Unary
from src.token_type import TokenType
from src.tokens import Token
from test.lab2.examples import EXAMPLES


class AstTests(unittest.TestCase):
    def test_hard_coded_examples(self):
        printer = AstPrinter()
        for example in EXAMPLES:
            with self.subTest(example=example.name):
                self.assertEqual(printer.print(example.build()), example.expected)

    def test_binary_keeps_operands_and_operator(self):
        left = Literal(8.0)
        right = Literal(3.0)
        operator = Token(TokenType.PERCENT, "%", None, 2, 4)
        expression = Binary(left, operator, right)
        self.assertIs(expression.left, left)
        self.assertIs(expression.operator, operator)
        self.assertIs(expression.right, right)
        self.assertEqual(expression.operator.line, 2)
        self.assertEqual(expression.operator.column, 4)

    def test_unary_keeps_operator_and_operand(self):
        operator = Token(TokenType.MINUS, "-", None, 1)
        right = Literal(12.0)
        expression = Unary(operator, right)
        self.assertIs(expression.operator, operator)
        self.assertIs(expression.right, right)

    def test_grouping_keeps_its_expression(self):
        inner = Literal(45.67)
        expression = Grouping(inner)
        self.assertIs(expression.expression, inner)

    def test_literal_values_are_preserved(self):
        for value in (2.5, "hello", "", True, False, None):
            with self.subTest(value=value):
                expression = Literal(value)
                self.assertIs(expression.value, value)

    def test_examples_cover_every_node_literal_and_operator(self):
        node_types = set()
        literal_types = set()
        binary_operators = set()
        unary_operators = set()

        def visit(expression):
            node_types.add(type(expression))
            if isinstance(expression, Literal):
                literal_types.add(type(expression.value))
            elif isinstance(expression, Grouping):
                visit(expression.expression)
            elif isinstance(expression, Unary):
                unary_operators.add(expression.operator.lexeme)
                visit(expression.right)
            elif isinstance(expression, Binary):
                binary_operators.add(expression.operator.lexeme)
                visit(expression.left)
                visit(expression.right)

        for example in EXAMPLES:
            visit(example.build())

        self.assertEqual(node_types, {Literal, Unary, Binary, Grouping})
        self.assertEqual(literal_types, {float, str, bool, type(None)})
        self.assertEqual(unary_operators, {"!", "-"})
        self.assertEqual(
            binary_operators, {"+", "-", "*", "/", "%", "==", "!=", ">", ">=", "<", "<="}
        )

    def test_string_boolean_and_nil_are_distinct(self):
        printer = AstPrinter()
        expressions = (Literal("true"), Literal(True), Literal("nil"), Literal(None))
        self.assertEqual(
            [printer.print(expression) for expression in expressions],
            ['"true"', "true", '"nil"', "nil"],
        )

    def test_unsupported_node_is_rejected(self):
        with self.assertRaisesRegex(TypeError, "Unsupported expression: Expr"):
            AstPrinter().print(Expr())


if __name__ == "__main__":
    unittest.main()
