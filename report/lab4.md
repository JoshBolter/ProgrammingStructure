# Lab 4: Statements
# AI used for formatting
Josh Bolter  
CIS 343 - Structure of Programming Languages

## Overview

I extended JoshLang from the previous labs and my midterm expression evaluator. It now supports a sequence of semicolon-terminated expression statements and `print` statements. I also implemented panic-mode syntax error recovery so that an invalid statement does not prevent the parser from processing later statements.

The existing token scanner, expression AST, and evaluator were reused. The previous single-expression AST, evaluation, and trace modes are still available. To run a Lab 4 statement program, I added the `--run` command-line flag.

## Implementation

### Statements

I added `src/stmt.py`, which defines two statement AST classes:

- `ExpressionStatement` stores an expression that is evaluated without printing its value.
- `PrintStatement` stores an expression that is evaluated and printed.

The statement grammar is:

```text
program   -> statement* EOF
statement -> "print" expression ";"
           | expression ";"
```

In `src/parser.py`, `parse_statements()` processes a file as a sequence of statements. The `_statement()` method selects print or expression syntax, and `_consume()` requires a terminating semicolon. I left the earlier `parse()` entry point in place for single-expression mode.

In `src/main.py`, the `--run` option executes every valid parsed statement using the existing `Evaluator`. The `print` statement displays strings without quotation marks, numbers without unnecessary `.0`, booleans as `true` or `false`, and `None` as `nil`. Expression statements still evaluate their values, but do not print them.

### Panic-mode error recovery

The statement parser catches a syntax error, records its line, column, and message, and calls `_synchronize()`. Synchronization discards tokens until it reaches a semicolon or the beginning of another recognizable statement. I included literal and unary expression starts as synchronization points so that a statement such as `true;` can still be parsed after a missing semicolon on the preceding line.

The parser discards the malformed statement but keeps subsequent valid statements. Valid statements are then executed even when earlier syntax errors occurred. Syntax errors are written to standard error and cause exit code `65`; valid programs return `0`. Existing runtime errors use exit code `70`.

## Setup and run commands

Python 3.10 or newer is sufficient, and no third-party packages are required. All commands below are run from the repository root. On Windows, `py -3` can be substituted for `python`.

Run the first required test:

```bash
python -m src.main --run test/lab4/inputs/required_errors.josh
```

Run the second required test:

```bash
python -m src.main --run test/lab4/inputs/required_success.josh
```

Run the complete Lab 4 unit test suite:

```bash
python -m unittest discover -s test/lab4 -p "test_*.py" -v
```

Existing modes are still available: run `python -m src.main` for a single expression's AST, `--scan` for tokens, `--eval` to evaluate one expression, and `--trace` to show evaluation steps.

## Required test case 1: syntax errors

**Input** (`test/lab4/inputs/required_errors.josh`):

```text
"one"
true;
print 2 +
```

**Standard output:** None.

**Standard error:**

```text
[line 2, column 1] Syntax error: Expected ';' after expression.
[line 4, column 1] Syntax error: Expected an expression after '+'.
```

**Exit code:** `65`

The first statement is missing its semicolon. Recovery resumes at `true;`, which is a valid expression statement but intentionally produces no output. The final `print 2 +` is incomplete and produces a second syntax error. Because the input file ends with a newline, the end-of-file token is located at line 4, column 1.

## Required test case 2: valid statements

**Input** (`test/lab4/inputs/required_success.josh`):

```text
4 + 2;
print "one";
print true;
print 1 + 2;
print nil;
```

**Standard output:**

```text
one
true
3
nil
```

**Standard error:** None.  
**Exit code:** `0`

The first expression is evaluated but discarded, so `6` does not appear in the output. Only the four `print` statements produce lines of output.

## Additional recovery test

**Input** (`test/lab4/inputs/recovery.josh`):

```text
print "before";
print 2 + ;
print "after";
```

**Standard output:**

```text
before
after
```

**Standard error:**

```text
[line 2, column 11] Syntax error: Expected an expression after '+'.
```

**Exit code:** `65`

The invalid second statement is skipped, but the parser successfully continues to the third statement and the interpreter prints `after`.

I also tested recovery from missing semicolons and malformed parenthesized expressions, multiple syntax errors in one file, expression-statement output suppression, empty files, statement AST classes, and compatibility with earlier AST/evaluation behavior.

## Test results

I executed the unit tests from the repository root with the command above. **All 11 Lab 4 tests passed**. Both assignment test cases produced the output and diagnostics recorded here. A separate manual run of each assignment input matched the same results.

## Limitations

This lab adds only print and expression statements. Variables, assignments, blocks, loops, and function declarations are not implemented. Lexical errors from the scanner still prevent parsing, as in previous labs; the new panic-mode recovery applies to parser syntax errors. The interactive prompt processes input a line at a time, while file input supports multiple statements and multiline expressions.

