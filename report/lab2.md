# Lab 2: AST Printer

Josh Bolter  
CIS 343 - Structure of Programming Languages

## Language and design

I continued using JoshLang and reused the `Token` and `TokenType` classes from Lab 1. I kept the expression syntax close to Lox because the usual arithmetic and comparison operators are already familiar. The main language difference is `%`, which represents remainder and has the same precedence as multiplication and division.

For this lab, I built the expression trees directly with Python constructors. The printer shows their structure; it does not calculate answers. The Lab 3 parser is included in the same project, but none of the Lab 2 examples depend on it.

## Expression grammar

```text
expression → equality ;
equality   → comparison ( ( "!=" | "==" ) comparison )* ;
comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term       → factor ( ( "-" | "+" ) factor )* ;
factor     → unary ( ( "/" | "*" | "%" ) unary )* ;
unary      → ( "!" | "-" ) unary | primary ;
primary    → NUMBER | STRING | "true" | "false" | "nil"
           | "(" expression ")" ;
```

The lowercase names are grammar rules. `NUMBER` and `STRING` are token categories, quoted text is a terminal, and `*` after a grouped rule means zero or more repetitions. The semicolons above end grammar rules; they are not part of an expression's source text.

The literal types are numbers, strings, booleans, and `nil`. Numbers are stored as Python floats, strings as `str`, booleans as `bool`, and `nil` as `None`. Identifiers and statement keywords can be scanned in Lab 1, but they are not expression forms in this grammar.

| Precedence, lowest to highest | Operators | Associativity |
| --- | --- | --- |
| Equality | `==`, `!=` | Left |
| Comparison | `>`, `>=`, `<`, `<=` | Left |
| Addition and subtraction | `+`, `-` | Left |
| Multiplication, division, and remainder | `*`, `/`, `%` | Left |
| Unary | `!`, `-` | Right |
| Primary | Literals and parenthesized expressions | Grouping determines the enclosed structure |

I used the precedence-based grammar from the parsing notes so it could carry forward to Lab 3. For repeated binary operators, the tree nests on the left. For example, `10 - 3 - 2` has the shape `(- (- 10 3) 2)`. The printer itself does not choose precedence; it preserves the tree it receives.

## AST implementation

I used one base class, `Expr`, and four dataclasses in `src/expr.py`.

| Class | Stored fields | Purpose |
| --- | --- | --- |
| `Literal` | `value` | Hold a number, string, boolean, or nil value |
| `Unary` | `operator`, `right` | Hold one operator and its operand |
| `Binary` | `left`, `operator`, `right` | Hold two operands and their operator |
| `Grouping` | `expression` | Preserve explicit parentheses |

The operator fields store the reused `Token` objects, including their location information. The nodes are frozen dataclasses, so the fields cannot be reassigned after construction.

`AstPrinter.print()` handles each of the four classes. It prints operators before their operands and surrounds each compound expression with parentheses. For example, the first hard-coded tree prints:

```text
(* (- 123) (group 45.67))
```

I print booleans as `true` and `false`, and `None` as `nil`. Whole-valued floats print without `.0`, so `123.0` displays as `123`. Strings stay in double quotes so the string `"true"` is visibly different from the boolean `true`. Newlines and other special characters are escaped in the displayed string to keep the tree readable. This is a display choice, not an addition of string escapes to JoshLang's scanner.

## Setup and running

Python 3.10 or newer is required. There are no third-party dependencies. Run these commands from the project folder that contains `src`, `test`, and `report`.

Print the hard-coded examples:

```bash
python -m test.lab2.examples
```

Run the unit tests:

```bash
python -m unittest discover -s test/lab2 -p "test_*.py" -v
```

Reproduce the saved expected-versus-actual results:

```bash
python -m test.lab2.examples --report
```

On systems that use `python3` instead of `python`, substitute `python3` in these commands.

## Testing and results

All **20 hard-coded examples passed**. The [test results appendix](lab2-test-results.md) includes every example's purpose, constructor code, expected output, actual printer output, and whether the outputs match. The examples cover all four node classes, every literal type, all eleven binary operators, both unary operators, and nested expressions. They also include an empty string, a string containing a newline, and a string whose text is `true`.

The **8 unit tests also passed**. They check the examples, verify that the classes retain the correct operands and operator tokens, and confirm that the examples cover every supported class, literal type, and operator. The tests also verify that string values remain distinct from boolean and nil values. Passing a plain `Expr` to the printer is rejected because it does not describe a concrete expression.

## Limitations

This lab represents and prints expressions; it does not evaluate them or check whether an operation makes sense for the operand types. The output is an AST display, not a source-code round-trip format. Variables, assignments, functions, and logical `and`/`or` expressions are outside this grammar. The recursive printer is intended for normal lab-sized trees; extremely deep trees can reach Python's recursion limit. There are no known failing tests in the included suite.

I am not requesting extra credit for this lab.

## References

- Haoyu Li, *Lab 2: AST Printer*, CIS 343 course handout, pp. 1-3.
- Haoyu Li, *Context-Free Grammars*, pp. 30-45, and *Parsing*, pp. 16-20, CIS 343 lecture slides.
- Robert Nystrom, [Crafting Interpreters: Representing Code](https://craftinginterpreters.com/representing-code.html).

