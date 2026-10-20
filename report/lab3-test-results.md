# Lab 3 test results

These results were captured by running `python -m test.lab3.run_examples` from the repository root. Expected results are fixed in `test/lab3/cases.py`; the script does not derive them from the program's output.

Result: **64/64 example cases passed**. Standard output and error output are captured separately. Interactive cases use redirected stdin, so they have no terminal prompt.

The three structural checks also passed 3/3 comparisons. Their inputs, expectations, and actual inspected values appear at the end.

## precedence

Multiplication binds more tightly than addition.

Mode: source-file input. Input file: `test/lab3/inputs/precedence.josh`.

### Source input

```text
1 + 2 * 3
```

### Expected stdout

```text
(+ 1 (* 2 3))
```

### Expected stderr

(no output)

### Actual stdout

```text
(+ 1 (* 2 3))
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## grouping

Parentheses change which operation is grouped first.

Mode: source-file input. Input file: `test/lab3/inputs/grouping.josh`.

### Source input

```text
(1 + 2) * 3
```

### Expected stdout

```text
(* (group (+ 1 2)) 3)
```

### Expected stderr

(no output)

### Actual stdout

```text
(* (group (+ 1 2)) 3)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## subtraction_associativity

Subtraction is left-associative.

Mode: source-file input. Input file: `test/lab3/inputs/subtraction_associativity.josh`.

### Source input

```text
10 - 3 - 2
```

### Expected stdout

```text
(- (- 10 3) 2)
```

### Expected stderr

(no output)

### Actual stdout

```text
(- (- 10 3) 2)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## division_associativity

Division is left-associative.

Mode: source-file input. Input file: `test/lab3/inputs/division_associativity.josh`.

### Source input

```text
20 / 5 / 2
```

### Expected stdout

```text
(/ (/ 20 5) 2)
```

### Expected stderr

(no output)

### Actual stdout

```text
(/ (/ 20 5) 2)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## addition_associativity

Addition is left-associative.

Mode: source-file input. Input file: `test/lab3/inputs/addition_associativity.josh`.

### Source input

```text
1 + 2 + 3
```

### Expected stdout

```text
(+ (+ 1 2) 3)
```

### Expected stderr

(no output)

### Actual stdout

```text
(+ (+ 1 2) 3)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## multiplication_associativity

Multiplication is left-associative.

Mode: source-file input. Input file: `test/lab3/inputs/multiplication_associativity.josh`.

### Source input

```text
2 * 3 * 4
```

### Expected stdout

```text
(* (* 2 3) 4)
```

### Expected stderr

(no output)

### Actual stdout

```text
(* (* 2 3) 4)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## remainder

Remainder shares precedence with multiplication and division.

Mode: source-file input. Input file: `test/lab3/inputs/remainder.josh`.

### Source input

```text
20 % 6 * 2 / 4
```

### Expected stdout

```text
(/ (* (% 20 6) 2) 4)
```

### Expected stderr

(no output)

### Actual stdout

```text
(/ (* (% 20 6) 2) 4)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## remainder_associativity

Remainder is left-associative.

Mode: source-file input. Input file: `test/lab3/inputs/remainder_associativity.josh`.

### Source input

```text
20 % 6 % 3
```

### Expected stdout

```text
(% (% 20 6) 3)
```

### Expected stderr

(no output)

### Actual stdout

```text
(% (% 20 6) 3)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## remainder_precedence

Remainder binds more tightly than addition.

Mode: source-file input. Input file: `test/lab3/inputs/remainder_precedence.josh`.

### Source input

```text
1 + 8 % 3
```

### Expected stdout

```text
(+ 1 (% 8 3))
```

### Expected stderr

(no output)

### Actual stdout

```text
(+ 1 (% 8 3))
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## unary_minus

A negative number is represented by a Unary node.

Mode: source-file input. Input file: `test/lab3/inputs/unary_minus.josh`.

### Source input

```text
-123
```

### Expected stdout

```text
(- 123)
```

### Expected stderr

(no output)

### Actual stdout

```text
(- 123)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## unary_not

Logical negation uses a Unary node.

Mode: source-file input. Input file: `test/lab3/inputs/unary_not.josh`.

### Source input

```text
!false
```

### Expected stdout

```text
(! false)
```

### Expected stderr

(no output)

### Actual stdout

```text
(! false)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## unary_associativity

Chained unary operators nest to the right.

Mode: source-file input. Input file: `test/lab3/inputs/unary_associativity.josh`.

### Source input

```text
!!-2
```

### Expected stdout

```text
(! (! (- 2)))
```

### Expected stderr

(no output)

### Actual stdout

```text
(! (! (- 2)))
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## unary_grouping

Unary operators can apply to grouped expressions.

Mode: source-file input. Input file: `test/lab3/inputs/unary_grouping.josh`.

### Source input

```text
!-(-2)
```

### Expected stdout

```text
(! (- (group (- 2))))
```

### Expected stderr

(no output)

### Actual stdout

```text
(! (- (group (- 2))))
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## unary_precedence

Unary negation binds more tightly than multiplication.

Mode: source-file input. Input file: `test/lab3/inputs/unary_precedence.josh`.

### Source input

```text
-2 * 3 % 2 + 4
```

### Expected stdout

```text
(+ (% (* (- 2) 3) 2) 4)
```

### Expected stderr

(no output)

### Actual stdout

```text
(+ (% (* (- 2) 3) 2) 4)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## negative_right_operand

Adjacent minus tokens can mean subtraction and negation.

Mode: source-file input. Input file: `test/lab3/inputs/negative_right_operand.josh`.

### Source input

```text
3--2
```

### Expected stdout

```text
(- 3 (- 2))
```

### Expected stderr

(no output)

### Actual stdout

```text
(- 3 (- 2))
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## equality_precedence

Arithmetic and comparisons bind more tightly than equality.

Mode: source-file input. Input file: `test/lab3/inputs/equality_precedence.josh`.

### Source input

```text
1 + 2 == 3 < 4
```

### Expected stdout

```text
(== (+ 1 2) (< 3 4))
```

### Expected stderr

(no output)

### Actual stdout

```text
(== (+ 1 2) (< 3 4))
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## inequality

Inequality supports literal operands.

Mode: source-file input. Input file: `test/lab3/inputs/inequality.josh`.

### Source input

```text
nil != false
```

### Expected stdout

```text
(!= nil false)
```

### Expected stderr

(no output)

### Actual stdout

```text
(!= nil false)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## comparison_associativity

All comparison operators are supported and left-associative.

Mode: source-file input. Input file: `test/lab3/inputs/comparison_associativity.josh`.

### Source input

```text
4 > 3 >= 2 < 5 <= 6
```

### Expected stdout

```text
(<= (< (>= (> 4 3) 2) 5) 6)
```

### Expected stderr

(no output)

### Actual stdout

```text
(<= (< (>= (> 4 3) 2) 5) 6)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## equality_associativity

Equality and inequality are left-associative.

Mode: source-file input. Input file: `test/lab3/inputs/equality_associativity.josh`.

### Source input

```text
true == false != nil
```

### Expected stdout

```text
(!= (== true false) nil)
```

### Expected stderr

(no output)

### Actual stdout

```text
(!= (== true false) nil)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## integer

A whole-number literal is accepted.

Mode: source-file input. Input file: `test/lab3/inputs/integer.josh`.

### Source input

```text
42
```

### Expected stdout

```text
42
```

### Expected stderr

(no output)

### Actual stdout

```text
42
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## decimal

A decimal literal is accepted.

Mode: source-file input. Input file: `test/lab3/inputs/decimal.josh`.

### Source input

```text
0.125
```

### Expected stdout

```text
0.125
```

### Expected stderr

(no output)

### Actual stdout

```text
0.125
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## zero

Zero remains a numeric literal.

Mode: source-file input. Input file: `test/lab3/inputs/zero.josh`.

### Source input

```text
0
```

### Expected stdout

```text
0
```

### Expected stderr

(no output)

### Actual stdout

```text
0
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## string

A string literal retains spaces and quotation marks in the AST output.

Mode: source-file input. Input file: `test/lab3/inputs/string.josh`.

### Source input

```text
"hello world"
```

### Expected stdout

```text
"hello world"
```

### Expected stderr

(no output)

### Actual stdout

```text
"hello world"
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## empty_string

An empty string remains distinct from nil.

Mode: source-file input. Input file: `test/lab3/inputs/empty_string.josh`.

### Source input

```text
""
```

### Expected stdout

```text
""
```

### Expected stderr

(no output)

### Actual stdout

```text
""
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## true_literal

The true token becomes a Boolean literal.

Mode: source-file input. Input file: `test/lab3/inputs/true_literal.josh`.

### Source input

```text
true
```

### Expected stdout

```text
true
```

### Expected stderr

(no output)

### Actual stdout

```text
true
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## false_literal

The false token becomes a Boolean literal.

Mode: source-file input. Input file: `test/lab3/inputs/false_literal.josh`.

### Source input

```text
false
```

### Expected stdout

```text
false
```

### Expected stderr

(no output)

### Actual stdout

```text
false
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## nil_literal

The nil token becomes a null literal.

Mode: source-file input. Input file: `test/lab3/inputs/nil_literal.josh`.

### Source input

```text
nil
```

### Expected stdout

```text
nil
```

### Expected stderr

(no output)

### Actual stdout

```text
nil
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## nested_grouping

Every explicit pair of parentheses produces a Grouping node.

Mode: source-file input. Input file: `test/lab3/inputs/nested_grouping.josh`.

### Source input

```text
(((1 + 2)))
```

### Expected stdout

```text
(group (group (group (+ 1 2))))
```

### Expected stderr

(no output)

### Actual stdout

```text
(group (group (group (+ 1 2))))
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## comment

The scanner removes a line comment before parsing continues.

Mode: source-file input. Input file: `test/lab3/inputs/comment.josh`.

### Source input

```text
1 + // second operand follows
2
```

### Expected stdout

```text
(+ 1 2)
```

### Expected stderr

(no output)

### Actual stdout

```text
(+ 1 2)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## multiline_expression

A file may contain one expression across several lines.

Mode: source-file input. Input file: `test/lab3/inputs/multiline_expression.josh`.

### Source input

```text
(1 +
2)
*3
```

### Expected stdout

```text
(* (group (+ 1 2)) 3)
```

### Expected stderr

(no output)

### Actual stdout

```text
(* (group (+ 1 2)) 3)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## multiline_string

A multiline string is one literal token.

Mode: source-file input. Input file: `test/lab3/inputs/multiline_string.josh`.

### Source input

```text
"line one
line two"
```

### Expected stdout

```text
"line one\nline two"
```

### Expected stderr

(no output)

### Actual stdout

```text
"line one\nline two"
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## literal_backslash

Backslashes are literal characters, not source escape sequences.

Mode: source-file input. Input file: `test/lab3/inputs/literal_backslash.josh`.

### Source input

```text
"bad\q"
```

### Expected stdout

```text
"bad\\q"
```

### Expected stderr

(no output)

### Actual stdout

```text
"bad\\q"
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## full_expression

Several precedence levels work inside and outside grouping.

Mode: source-file input. Input file: `test/lab3/inputs/full_expression.josh`.

### Source input

```text
1 - (2 * 3) < 4 == false
```

### Expected stdout

```text
(== (< (- 1 (group (* 2 3))) 4) false)
```

### Expected stderr

(no output)

### Actual stdout

```text
(== (< (- 1 (group (* 2 3))) 4) false)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## syntax_without_evaluation

Parsing does not perform runtime type checking.

Mode: source-file input. Input file: `test/lab3/inputs/syntax_without_evaluation.josh`.

### Source input

```text
"a" - true
```

### Expected stdout

```text
(- "a" true)
```

### Expected stderr

(no output)

### Actual stdout

```text
(- "a" true)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## division_without_evaluation

Parsing division by zero builds a tree without evaluating it.

Mode: source-file input. Input file: `test/lab3/inputs/division_without_evaluation.josh`.

### Source input

```text
1 / 0
```

### Expected stdout

```text
(/ 1 0)
```

### Expected stderr

(no output)

### Actual stdout

```text
(/ 1 0)
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## empty_file

An empty file contains no expression.

Mode: source-file input. Input file: `test/lab3/inputs/empty_file.josh`.

### Source input

(empty input)

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 1] Syntax error: Expected an expression before end of input.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 1] Syntax error: Expected an expression before end of input.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The parser reaches EOF before finding a primary expression.

## missing_right_parenthesis

A grouping must have a closing parenthesis.

Mode: source-file input. Input file: `test/lab3/inputs/missing_right_parenthesis.josh`.

### Source input

```text
(1 + 2
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 7] Syntax error: Expected ')' to close '(' from line 1, column 1.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 7] Syntax error: Expected ')' to close '(' from line 1, column 1.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The opening parenthesis at column 1 has no matching closing token.

## unmatched_closing_parenthesis

A closing parenthesis cannot start an expression.

Mode: source-file input. Input file: `test/lab3/inputs/unmatched_closing_parenthesis.josh`.

### Source input

```text
)1
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 1] Syntax error: Unexpected ')' without a matching '('.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 1] Syntax error: Unexpected ')' without a matching '('.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: There is no earlier opening parenthesis for the first token.

## extra_closing_parenthesis

An extra closing parenthesis is rejected after an expression.

Mode: source-file input. Input file: `test/lab3/inputs/extra_closing_parenthesis.josh`.

### Source input

```text
(1 + 2))
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 8] Syntax error: Unexpected ')' without a matching '('.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 8] Syntax error: Unexpected ')' without a matching '('.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The first closing parenthesis completes the group; the next one has no opening match.

## missing_right_operand

A binary operator must have a right operand.

Mode: source-file input. Input file: `test/lab3/inputs/missing_right_operand.josh`.

### Source input

```text
1 +
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 4] Syntax error: Expected an expression after '+'.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 4] Syntax error: Expected an expression after '+'.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The plus operator is followed by EOF instead of an expression.

## invalid_right_operand

Another binary operator cannot serve as the right operand.

Mode: source-file input. Input file: `test/lab3/inputs/invalid_right_operand.josh`.

### Source input

```text
1 + * 2
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 5] Syntax error: Expected an expression after '+'.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 5] Syntax error: Expected an expression after '+'.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The star token cannot begin an operand; JoshLang has no unary star operator.

## missing_unary_minus_operand

Unary minus requires an operand.

Mode: source-file input. Input file: `test/lab3/inputs/missing_unary_minus_operand.josh`.

### Source input

```text
-
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 2] Syntax error: Expected an expression after '-'.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 2] Syntax error: Expected an expression after '-'.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The unary minus reaches EOF without an operand.

## missing_unary_not_operand

Unary negation requires an operand.

Mode: source-file input. Input file: `test/lab3/inputs/missing_unary_not_operand.josh`.

### Source input

```text
!
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 2] Syntax error: Expected an expression after '!'.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 2] Syntax error: Expected an expression after '!'.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The negation operator reaches EOF without an operand.

## missing_left_operand

A binary-only operator cannot begin an expression.

Mode: source-file input. Input file: `test/lab3/inputs/missing_left_operand.josh`.

### Source input

```text
* 2
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 1] Syntax error: Missing left operand before '*'.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 1] Syntax error: Missing left operand before '*'.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: Multiplication has no expression to its left.

## unsupported_unary_plus

JoshLang does not define a unary plus operator.

Mode: source-file input. Input file: `test/lab3/inputs/unsupported_unary_plus.josh`.

### Source input

```text
+2
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 1] Syntax error: Missing left operand before '+'.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 1] Syntax error: Missing left operand before '+'.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: Plus is defined only as a binary operator, so its left operand is missing.

## empty_group

Grouping must contain an expression.

Mode: source-file input. Input file: `test/lab3/inputs/empty_group.josh`.

### Source input

```text
()
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 2] Syntax error: Expected an expression inside parentheses.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 2] Syntax error: Expected an expression inside parentheses.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The closing parenthesis appears immediately after the opening one.

## missing_operand_in_group

A closing parenthesis cannot replace an operand.

Mode: source-file input. Input file: `test/lab3/inputs/missing_operand_in_group.josh`.

### Source input

```text
(1 + )
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 6] Syntax error: Expected an expression after '+'.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 6] Syntax error: Expected an expression after '+'.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The addition needs a right operand before the group can close.

## identifier_expression

Variables are not part of this expression grammar yet.

Mode: source-file input. Input file: `test/lab3/inputs/identifier_expression.josh`.

### Source input

```text
name + 1
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 1] Syntax error: Expected an expression; found 'name'.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 1] Syntax error: Expected an expression; found 'name'.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The scanner recognizes an identifier, but primary does not yet include identifiers.

## statement_token

A statement keyword is not an expression.

Mode: source-file input. Input file: `test/lab3/inputs/statement_token.josh`.

### Source input

```text
print 1
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 1] Syntax error: Expected an expression; found 'print'.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 1] Syntax error: Expected an expression; found 'print'.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The scanner reserves print, but statement parsing is outside this lab.

## trailing_expression

The program accepts only one expression per file.

Mode: source-file input. Input file: `test/lab3/inputs/trailing_expression.josh`.

### Source input

```text
1 2
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 3] Syntax error: Unexpected token after expression: '2'.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 3] Syntax error: Unexpected token after expression: '2'.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The first number already forms a complete expression; the second is left over.

## trailing_semicolon

The expression-only grammar does not consume statement terminators.

Mode: source-file input. Input file: `test/lab3/inputs/trailing_semicolon.josh`.

### Source input

```text
1;
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 2] Syntax error: Unexpected token after expression: ';'.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 2] Syntax error: Unexpected token after expression: ';'.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: Semicolons are scanned for future statements but are not part of this grammar.

## assignment_token

Assignment is not an expression operator in this lab.

Mode: source-file input. Input file: `test/lab3/inputs/assignment_token.josh`.

### Source input

```text
1 = 2
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 3] Syntax error: Unexpected token after expression: '='.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 3] Syntax error: Unexpected token after expression: '='.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: A single equals token is assignment syntax, not the equality operator ==.

## logical_and

Logical and is reserved but not implemented in this expression grammar.

Mode: source-file input. Input file: `test/lab3/inputs/logical_and.josh`.

### Source input

```text
true and false
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 6] Syntax error: Unexpected token after expression: 'and'.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 6] Syntax error: Unexpected token after expression: 'and'.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The parser finishes true and then rejects the unsupported and token.

## logical_or

Logical or is reserved but not implemented in this expression grammar.

Mode: source-file input. Input file: `test/lab3/inputs/logical_or.josh`.

### Source input

```text
true or false
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 6] Syntax error: Unexpected token after expression: 'or'.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 6] Syntax error: Unexpected token after expression: 'or'.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The parser finishes true and then rejects the unsupported or token.

## multiline_error_location

Syntax errors report the line and column of the offending token.

Mode: source-file input. Input file: `test/lab3/inputs/multiline_error_location.josh`.

### Source input

```text
1 +
 * 2
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 2, column 2] Syntax error: Expected an expression after '+'.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 2, column 2] Syntax error: Expected an expression after '+'.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The unexpected multiplication operator is at line 2, column 2.

## multiline_unclosed_group

An EOF diagnostic also identifies the opening parenthesis.

Mode: source-file input. Input file: `test/lab3/inputs/multiline_unclosed_group.josh`.

### Source input

```text
(1
 + 2
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 2, column 5] Syntax error: Expected ')' to close '(' from line 1, column 1.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 2, column 5] Syntax error: Expected ')' to close '(' from line 1, column 1.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The expression ends on line 2 while the group opened on line 1 remains unclosed.

## trailing_dot

A dot token cannot trail a numeric expression.

Mode: source-file input. Input file: `test/lab3/inputs/trailing_dot.josh`.

### Source input

```text
12.
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 3] Syntax error: Unexpected token after expression: '.'.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 3] Syntax error: Unexpected token after expression: '.'.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The scanner reads NUMBER 12 and DOT, rather than accepting a trailing decimal point.

## lexical_character

A lexical error prevents any AST from being printed.

Mode: source-file input. Input file: `test/lab3/inputs/lexical_character.josh`.

### Source input

```text
1 + @2
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 5] Lexical error: Unexpected character '@'.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 5] Lexical error: Unexpected character '@'.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The scanner rejects @, and the main program stops before constructing a parser.

## lexical_string

An unterminated string prevents parsing.

Mode: source-file input. Input file: `test/lab3/inputs/lexical_string.josh`.

### Source input

```text
"hello
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 1] Lexical error: Unterminated string.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 1] Lexical error: Unterminated string.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The string has no closing quotation mark.

## lexical_number_range

A number outside the scanner's finite range prevents parsing.

Mode: source-file input. Input file: `test/lab3/inputs/lexical_number_range.josh`.

### Source input

```text
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
```

### Expected stdout

(no output)

### Expected stderr

```text
[line 1, column 1] Lexical error: Number is outside the supported range.
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 1] Lexical error: Number is outside the supported range.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: The decimal literal is too large for the scanner's finite floating-point representation.

## depth_limit

Excessive recursive nesting produces a diagnostic instead of a traceback.

Mode: source-file input. Input file: `test/lab3/inputs/depth_limit.josh`.

### Source input

```text
((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((1))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
```

### Expected stdout

(no output)

### Expected stderr pattern

```text
\[line 1, column \d+\] Syntax error: Expression is too deeply nested\.\n
```

### Actual stdout

(no output)

### Actual stderr

```text
[line 1, column 91] Syntax error: Expression is too deeply nested.
```

Expected exit code: `65`. Actual exit code: `65`.

Result: **PASS**.

Explanation: This expression exceeds Python's practical recursion depth. The exact column depends on the runtime.

## interactive_recovery

Interactive mode recovers from both lexical and syntax errors.

Mode: interactive input. Input file: `test/lab3/inputs/interactive_recovery.josh`.

### Source input

```text
1 + @2
1 +
1 + 2 * 3
false
```

### Expected stdout

```text
(+ 1 (* 2 3))
false
```

### Expected stderr

```text
[line 1, column 5] Lexical error: Unexpected character '@'.
[line 1, column 4] Syntax error: Expected an expression after '+'.
```

### Actual stdout

```text
(+ 1 (* 2 3))
false
```

### Actual stderr

```text
[line 1, column 5] Lexical error: Unexpected character '@'.
[line 1, column 4] Syntax error: Expected an expression after '+'.
```

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

Explanation: The first two inputs fail independently. The next two inputs still produce ASTs.

## interactive_blank_lines

Blank interactive inputs are ignored before the next expression.

Mode: interactive input. Input file: `test/lab3/inputs/interactive_blank_lines.josh`.

### Source input

```text

   
42
```

### Expected stdout

```text
42
```

### Expected stderr

(no output)

### Actual stdout

```text
42
```

### Actual stderr

(no output)

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

## interactive_trailing_recovery

Interactive mode also recovers after rejecting trailing tokens.

Mode: interactive input. Input file: `test/lab3/inputs/interactive_trailing_recovery.josh`.

### Source input

```text
1 2
(3 + 4) * 2
```

### Expected stdout

```text
(* (group (+ 3 4)) 2)
```

### Expected stderr

```text
[line 1, column 3] Syntax error: Unexpected token after expression: '2'.
```

### Actual stdout

```text
(* (group (+ 3 4)) 2)
```

### Actual stderr

```text
[line 1, column 3] Syntax error: Unexpected token after expression: '2'.
```

Expected exit code: `0`. Actual exit code: `0`.

Result: **PASS**.

Explanation: The first input contains two expressions. The next input is parsed normally.

## Structural check: AST fields

The addition node has a multiplication node on its right, with numeric literal children.

### Source input

```text
1 + 2 * 3
```

### Expected inspection result

```text
('PLUS', 1.0, 'STAR', 2.0, 3.0)
```

### Actual inspection result

```text
('PLUS', 1.0, 'STAR', 2.0, 3.0)
```

Result: **PASS**.

## Structural check: Literal value types

Each source is parsed separately, and each literal keeps its intended Python type.

### Source input

```text
true
false
nil
42
"hi"
```

### Expected inspection result

```text
true: bool True
false: bool False
nil: NoneType None
42: float 42.0
"hi": str 'hi'
```

### Actual inspection result

```text
true: bool True
false: bool False
nil: NoneType None
42: float 42.0
"hi": str 'hi'
```

Result: **PASS**.

## Structural check: Negative number representation

The minus token remains a unary operator rather than becoming part of the numeric literal.

### Source input

```text
-42
```

### Expected inspection result

```text
('Unary', 'MINUS', 'Literal', 42.0)
```

### Actual inspection result

```text
('Unary', 'MINUS', 'Literal', 42.0)
```

Result: **PASS**.
