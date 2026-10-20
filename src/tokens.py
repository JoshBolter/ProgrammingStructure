from dataclasses import dataclass

from .token_type import TokenType


@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    literal: object
    line: int
    column: int = 1

    def __str__(self) -> str:
        return (
            f"{self.type.name} lexeme={self.lexeme!r} literal={self.literal!r} "
            f"line={self.line} column={self.column}"
        )
