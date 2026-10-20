from dataclasses import dataclass


@dataclass(frozen=True)
class Diagnostic:
    line: int
    column: int
    message: str
    kind: str = "Lexical error"

    def __str__(self) -> str:
        return f"[line {self.line}, column {self.column}] {self.kind}: {self.message}"
