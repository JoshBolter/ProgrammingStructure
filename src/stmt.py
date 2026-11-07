from dataclasses import dataclass

from .expr import Expr


class Stmt:
    pass


@dataclass(frozen=True)
class ExpressionStatement(Stmt):
    expression: Expr


@dataclass(frozen=True)
class PrintStatement(Stmt):
    expression: Expr
