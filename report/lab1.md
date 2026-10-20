# Lab 1: Scanning

Josh Bolter  
CIS 343 - Structure of Programming Languages

## Language design

My language is called **JoshLang**. I kept most of its lexical rules close to Lox so that the scanner is straightforward to extend in later labs. I added `%` as a remainder operator. Keeping familiar operator and keyword spellings lets me focus on how scanning works before adding more language features.

JoshLang is case-sensitive. Identifiers use ASCII letters and underscores, followed by any number of ASCII letters, digits, or underscores. This means `count2` and `_count` are identifiers, while `true` is a keyword and `True` is an identifier. I scan the entire identifier before checking the keyword table, so `varname` is not split into `var` and `name`.

### Token types

| Category | Spellings or token types |
| --- | --- |
| Punctuation | `(`, `)`, `{`, `}`, `,`, `.`, `;` |
| Arithmetic | `+`, `-`, `*`, `/`, `%` |
| Other operators | `!`, `!=`, `=`, `==`, `<`, `<=`, `>`, `>=` |
| Literals and identifiers | `NUMBER`, `STRING`, `IDENTIFIER` |
| Keywords | `and`, `class`, `else`, `false`, `for`, `fun`, `if`, `nil`, `or`, `print`, `return`, `super`, `this`, `true`, `var`, `while` |
| End of input | `EOF` |

The scanner recognizes the whole keyword set even though this lab does not execute statements or expressions. Later expression labs also do not need every token recognized here.

### Regular expressions

These describe complete lexemes. In the scanner, I apply the same rules by advancing through the source one character at a time.

| Kind | Regular expression |
| --- | --- |
| Number | `[0-9]+(\.[0-9]+)?` |
| String | `"[^"]*"` |
| Identifier | `[A-Za-z_][A-Za-z0-9_]*` |

Numbers must have a digit before a decimal point and at least one after it when a fractional part is present. A minus sign is a separate operator. All numbers are stored as Python `float` values, but their original text is retained in the lexeme. For example, `000.500` retains that text and has the literal value `0.5`.

The number rule does not include scientific notation or leading decimal points. The scanner therefore reads `.5` as `DOT` followed by `NUMBER`, and `1e3` as `NUMBER` followed by `IDENTIFIER`. Those inputs can be tokenized without being valid expressions. A number matching the regular expression is still rejected if conversion produces an infinite value.

Strings begin and end with double quotes. They can be empty or span multiple source lines. The character class in the string expression includes newlines. Backslashes are ordinary characters, so the source `"a\nb"` contains a literal backslash and `n`; it does not contain a newline. Quotes cannot be escaped. Unicode text is allowed inside strings even though identifiers use ASCII characters.

### Whitespace and comments

Spaces, tabs, carriage returns, and line feeds do not become tokens. Line feeds increase the line number, and columns start at 1. A tab counts as one source character when calculating a column. Source files use UTF-8; the entry point normalizes ordinary text-file line endings while reading them.

Two forward slashes start a comment that continues to the next line feed or the end of the source. Comment text is discarded. A single slash remains a division token. Block comments are not part of the language, so `/*` is scanned as `/` and `*`.

## Implementation

`Token` stores the token type, raw lexeme, converted literal value, line, and column. Only number and string tokens have converted literal values at the scanning stage. Keywords such as `true`, `false`, and `nil` are identified by their token types. The output prints all five fields, making it possible to check both the token and its location.

`Scanner` walks through the source using a start index and a current index. It checks two-character operators before finishing their one-character versions. It appends an `EOF` token after scanning, including when it reports lexical errors. In scanning mode, valid tokens found around errors are still printed.

The entry point uses `JoshLang` in `src/main.py`. The `--scan` option connects source-file and interactive input to the scanner. The interactive loop starts a new scanner for each entered line, so an error does not carry over to the next input. Blank interactive lines are ignored. The terminal prompt is `josh> `; it is omitted when input is redirected for automated testing.

## Error handling

| Error | Behavior |
| --- | --- |
| Unexpected character | Report the character and its line/column, then continue scanning. This includes non-ASCII identifier characters and unsupported whitespace. |
| Unterminated string | Report the opening quote's line/column. No incomplete string token is emitted. |
| Number outside the supported range | Report the beginning of the number. No infinite number token is emitted. |

Diagnostics go to standard error, while token output goes to standard output. A source file with lexical errors exits with status `65`. Interactive mode stays available after an error and exits normally when input ends.

## Setup and running

The project uses Python 3.10 or newer and only the standard library. No packages need to be installed. All commands below are run from the project directory containing `src`, `test`, and `report`. If the Python command on Windows is `py`, I can replace `python` with `py -3`.

Scan a source file:

```bash
python -m src.main --scan test/lab1/inputs/adjacent_tokens.josh
```

Start interactive scanning:

```bash
python -m src.main --scan
```

For example, entering `1+2*3==7` prints:

```text
NUMBER lexeme='1' literal=1.0 line=1 column=1
PLUS lexeme='+' literal=None line=1 column=2
NUMBER lexeme='2' literal=2.0 line=1 column=3
STAR lexeme='*' literal=None line=1 column=4
NUMBER lexeme='3' literal=3.0 line=1 column=5
EQUAL_EQUAL lexeme='==' literal=None line=1 column=6
NUMBER lexeme='7' literal=7.0 line=1 column=8
EOF lexeme='' literal=None line=1 column=9
```

End interactive input with Ctrl+D on macOS/Linux, or Ctrl+Z followed by Enter on Windows. Ctrl+C also closes the interactive loop.

Run the tests and reproduce the captured output:

```bash
python -m unittest discover -s test/lab1 -p "test_*.py" -v
python -m test.lab1.write_report
```

## Test results

I used 25 scanner inputs to cover all 40 token types, numeric and identifier boundaries, empty input, comments, strings, line/column information, and every supported lexical error. Each case is checked directly against the scanner and again through source-file mode. I also tested interactive recovery after two different errors, a session with blank input followed by valid input, and a session containing unsupported whitespace followed by valid input.

All six unittest methods passed. All 25 input cases passed both the scanner and source-file checks, and all three interactive sessions passed. The [test results appendix](lab1-test-results.md) records each case's purpose, source, expected output, actual output, diagnostics, exit code, and result. The inputs and scripts are in `test/lab1/`.

## Limitations

The scanner does not parse or execute code. It does not support block comments, scientific notation, string escapes, or Unicode identifiers. File input can contain multiline strings, but each interactive entry is limited to one line. Numbers use floating-point storage, so very small values can round to zero and some decimal values cannot be represented exactly. There are no known failing tests in the included suite. I am not requesting extra credit for this lab.

## References

I used the Lab 1 handout, the scanning lecture slides, and Robert Nystrom's [Crafting Interpreters, Chapter 4: Scanning](https://craftinginterpreters.com/scanning.html) as references. The scanner follows the chapter's general character-by-character approach.
