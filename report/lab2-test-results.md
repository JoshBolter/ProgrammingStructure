# Lab 2 test results

These results were produced by running python -m test.lab2.examples --report.
Each expected result is written separately from the printer. The actual results below come from running the hard-coded constructors.

Result: **20/20 examples passed.**

## textbook_nested

Purpose: Combine all four node classes and both whole and fractional numbers.

Hard-coded AST:

```python
def textbook_nested():
    return Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123.0)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )
```

Expected:

```text
(* (- 123) (group 45.67))
```

Actual:

```text
(* (- 123) (group 45.67))
```

Matches expectations: **Yes**.

## string_addition

Purpose: Print a binary plus expression with quoted string literals.

Hard-coded AST:

```python
def string_addition():
    return Binary(
        Literal("hello"),
        Token(TokenType.PLUS, "+", None, 1),
        Literal(" world"),
    )
```

Expected:

```text
(+ "hello" " world")
```

Actual:

```text
(+ "hello" " world")
```

Matches expectations: **Yes**.

## subtraction

Purpose: Print binary subtraction.

Hard-coded AST:

```python
def subtraction():
    return Binary(
        Literal(10.0), Token(TokenType.MINUS, "-", None, 1), Literal(3.0)
    )
```

Expected:

```text
(- 10 3)
```

Actual:

```text
(- 10 3)
```

Matches expectations: **Yes**.

## division

Purpose: Print division.

Hard-coded AST:

```python
def division():
    return Binary(
        Literal(20.0), Token(TokenType.SLASH, "/", None, 1), Literal(4.0)
    )
```

Expected:

```text
(/ 20 4)
```

Actual:

```text
(/ 20 4)
```

Matches expectations: **Yes**.

## remainder

Purpose: Print JoshLang's added % operator.

Hard-coded AST:

```python
def remainder():
    return Binary(
        Literal(17.0), Token(TokenType.PERCENT, "%", None, 1), Literal(5.0)
    )
```

Expected:

```text
(% 17 5)
```

Actual:

```text
(% 17 5)
```

Matches expectations: **Yes**.

## unary_not

Purpose: Print unary ! and a true literal.

Hard-coded AST:

```python
def unary_not():
    return Unary(Token(TokenType.BANG, "!", None, 1), Literal(True))
```

Expected:

```text
(! true)
```

Actual:

```text
(! true)
```

Matches expectations: **Yes**.

## nil_equality

Purpose: Print == and nil values.

Hard-coded AST:

```python
def nil_equality():
    return Binary(
        Literal(None), Token(TokenType.EQUAL_EQUAL, "==", None, 1), Literal(None)
    )
```

Expected:

```text
(== nil nil)
```

Actual:

```text
(== nil nil)
```

Matches expectations: **Yes**.

## boolean_inequality

Purpose: Print != and preserve both boolean spellings.

Hard-coded AST:

```python
def boolean_inequality():
    return Binary(
        Literal(True), Token(TokenType.BANG_EQUAL, "!=", None, 1), Literal(False)
    )
```

Expected:

```text
(!= true false)
```

Actual:

```text
(!= true false)
```

Matches expectations: **Yes**.

## less_than

Purpose: Print <.

Hard-coded AST:

```python
def less_than():
    return Binary(
        Literal(1.0), Token(TokenType.LESS, "<", None, 1), Literal(2.0)
    )
```

Expected:

```text
(< 1 2)
```

Actual:

```text
(< 1 2)
```

Matches expectations: **Yes**.

## less_equal

Purpose: Print <=.

Hard-coded AST:

```python
def less_equal():
    return Binary(
        Literal(1.0), Token(TokenType.LESS_EQUAL, "<=", None, 1), Literal(1.0)
    )
```

Expected:

```text
(<= 1 1)
```

Actual:

```text
(<= 1 1)
```

Matches expectations: **Yes**.

## greater_than

Purpose: Print >.

Hard-coded AST:

```python
def greater_than():
    return Binary(
        Literal(3.0), Token(TokenType.GREATER, ">", None, 1), Literal(2.0)
    )
```

Expected:

```text
(> 3 2)
```

Actual:

```text
(> 3 2)
```

Matches expectations: **Yes**.

## greater_equal

Purpose: Print >=.

Hard-coded AST:

```python
def greater_equal():
    return Binary(
        Literal(3.0), Token(TokenType.GREATER_EQUAL, ">=", None, 1), Literal(3.0)
    )
```

Expected:

```text
(>= 3 3)
```

Actual:

```text
(>= 3 3)
```

Matches expectations: **Yes**.

## left_associative_subtraction

Purpose: Preserve a left-nested tree for 10 - 3 - 2.

Hard-coded AST:

```python
def left_associative_subtraction():
    return Binary(
        Binary(
            Literal(10.0), Token(TokenType.MINUS, "-", None, 1), Literal(3.0)
        ),
        Token(TokenType.MINUS, "-", None, 1),
        Literal(2.0),
    )
```

Expected:

```text
(- (- 10 3) 2)
```

Actual:

```text
(- (- 10 3) 2)
```

Matches expectations: **Yes**.

## nested_grouping

Purpose: Keep both explicit grouping nodes.

Hard-coded AST:

```python
def nested_grouping():
    return Grouping(
        Grouping(
            Binary(
                Literal(2.0), Token(TokenType.PLUS, "+", None, 1), Literal(3.0)
            )
        )
    )
```

Expected:

```text
(group (group (+ 2 3)))
```

Actual:

```text
(group (group (+ 2 3)))
```

Matches expectations: **Yes**.

## double_not

Purpose: Preserve nested unary expressions.

Hard-coded AST:

```python
def double_not():
    return Unary(
        Token(TokenType.BANG, "!", None, 1),
        Unary(Token(TokenType.BANG, "!", None, 1), Literal(False)),
    )
```

Expected:

```text
(! (! false))
```

Actual:

```text
(! (! false))
```

Matches expectations: **Yes**.

## empty_string

Purpose: Keep an empty string visible.

Hard-coded AST:

```python
def empty_string():
    return Literal("")
```

Expected:

```text
""
```

Actual:

```text
""
```

Matches expectations: **Yes**.

## string_true

Purpose: Distinguish the string true from the boolean true.

Hard-coded AST:

```python
def string_true():
    return Literal("true")
```

Expected:

```text
"true"
```

Actual:

```text
"true"
```

Matches expectations: **Yes**.

## multiline_string

Purpose: Display a newline without splitting the printed tree across lines.

Hard-coded AST:

```python
def multiline_string():
    return Literal("line one\nline two")
```

Expected:

```text
"line one\nline two"
```

Actual:

```text
"line one\nline two"
```

Matches expectations: **Yes**.

## zero

Purpose: Print a whole-valued float without .0.

Hard-coded AST:

```python
def zero():
    return Literal(0.0)
```

Expected:

```text
0
```

Actual:

```text
0
```

Matches expectations: **Yes**.

## mixed_precedence

Purpose: Preserve multiplication inside addition inside equality.

Hard-coded AST:

```python
def mixed_precedence():
    return Binary(
        Binary(
            Literal(1.0),
            Token(TokenType.PLUS, "+", None, 1),
            Binary(
                Literal(2.0), Token(TokenType.STAR, "*", None, 1), Literal(3.0)
            ),
        ),
        Token(TokenType.EQUAL_EQUAL, "==", None, 1),
        Literal(7.0),
    )
```

Expected:

```text
(== (+ 1 (* 2 3)) 7)
```

Actual:

```text
(== (+ 1 (* 2 3)) 7)
```

Matches expectations: **Yes**.
