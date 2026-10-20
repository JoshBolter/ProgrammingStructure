# Lab 1 test results

These are the expected results and captured output from the scanner's command-line entry point. The expected token records and diagnostics are specified in `test/lab1/cases.py`; the actual output is captured by `test/lab1/write_report.py`.

I ran each of the 25 scanner cases as a source file and also checked three interactive sessions. The unit tests separately compare every token field and verify coverage of all 40 token types.

## punctuation

Scan every single-character punctuation/operator; /* is not a block comment.

**Source input:**

```text
(){},.-+;/*%
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/punctuation.josh
```

**Expected stdout:**

```text
LEFT_PAREN lexeme='(' literal=None line=1 column=1
RIGHT_PAREN lexeme=')' literal=None line=1 column=2
LEFT_BRACE lexeme='{' literal=None line=1 column=3
RIGHT_BRACE lexeme='}' literal=None line=1 column=4
COMMA lexeme=',' literal=None line=1 column=5
DOT lexeme='.' literal=None line=1 column=6
MINUS lexeme='-' literal=None line=1 column=7
PLUS lexeme='+' literal=None line=1 column=8
SEMICOLON lexeme=';' literal=None line=1 column=9
SLASH lexeme='/' literal=None line=1 column=10
STAR lexeme='*' literal=None line=1 column=11
PERCENT lexeme='%' literal=None line=1 column=12
EOF lexeme='' literal=None line=1 column=13
```

**Actual stdout:**

```text
LEFT_PAREN lexeme='(' literal=None line=1 column=1
RIGHT_PAREN lexeme=')' literal=None line=1 column=2
LEFT_BRACE lexeme='{' literal=None line=1 column=3
RIGHT_BRACE lexeme='}' literal=None line=1 column=4
COMMA lexeme=',' literal=None line=1 column=5
DOT lexeme='.' literal=None line=1 column=6
MINUS lexeme='-' literal=None line=1 column=7
PLUS lexeme='+' literal=None line=1 column=8
SEMICOLON lexeme=';' literal=None line=1 column=9
SLASH lexeme='/' literal=None line=1 column=10
STAR lexeme='*' literal=None line=1 column=11
PERCENT lexeme='%' literal=None line=1 column=12
EOF lexeme='' literal=None line=1 column=13
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## operators

Distinguish one-character operators from their longest two-character matches.

**Source input:**

```text
! != = == > >= < <=
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/operators.josh
```

**Expected stdout:**

```text
BANG lexeme='!' literal=None line=1 column=1
BANG_EQUAL lexeme='!=' literal=None line=1 column=3
EQUAL lexeme='=' literal=None line=1 column=6
EQUAL_EQUAL lexeme='==' literal=None line=1 column=8
GREATER lexeme='>' literal=None line=1 column=11
GREATER_EQUAL lexeme='>=' literal=None line=1 column=13
LESS lexeme='<' literal=None line=1 column=16
LESS_EQUAL lexeme='<=' literal=None line=1 column=18
EOF lexeme='' literal=None line=1 column=20
```

**Actual stdout:**

```text
BANG lexeme='!' literal=None line=1 column=1
BANG_EQUAL lexeme='!=' literal=None line=1 column=3
EQUAL lexeme='=' literal=None line=1 column=6
EQUAL_EQUAL lexeme='==' literal=None line=1 column=8
GREATER lexeme='>' literal=None line=1 column=11
GREATER_EQUAL lexeme='>=' literal=None line=1 column=13
LESS lexeme='<' literal=None line=1 column=16
LESS_EQUAL lexeme='<=' literal=None line=1 column=18
EOF lexeme='' literal=None line=1 column=20
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## keywords

Recognize every reserved keyword and preserve each line number.

**Source input:**

```text
and
class
else
false
for
fun
if
nil
or
print
return
super
this
true
var
while
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/keywords.josh
```

**Expected stdout:**

```text
AND lexeme='and' literal=None line=1 column=1
CLASS lexeme='class' literal=None line=2 column=1
ELSE lexeme='else' literal=None line=3 column=1
FALSE lexeme='false' literal=None line=4 column=1
FOR lexeme='for' literal=None line=5 column=1
FUN lexeme='fun' literal=None line=6 column=1
IF lexeme='if' literal=None line=7 column=1
NIL lexeme='nil' literal=None line=8 column=1
OR lexeme='or' literal=None line=9 column=1
PRINT lexeme='print' literal=None line=10 column=1
RETURN lexeme='return' literal=None line=11 column=1
SUPER lexeme='super' literal=None line=12 column=1
THIS lexeme='this' literal=None line=13 column=1
TRUE lexeme='true' literal=None line=14 column=1
VAR lexeme='var' literal=None line=15 column=1
WHILE lexeme='while' literal=None line=16 column=1
EOF lexeme='' literal=None line=17 column=1
```

**Actual stdout:**

```text
AND lexeme='and' literal=None line=1 column=1
CLASS lexeme='class' literal=None line=2 column=1
ELSE lexeme='else' literal=None line=3 column=1
FALSE lexeme='false' literal=None line=4 column=1
FOR lexeme='for' literal=None line=5 column=1
FUN lexeme='fun' literal=None line=6 column=1
IF lexeme='if' literal=None line=7 column=1
NIL lexeme='nil' literal=None line=8 column=1
OR lexeme='or' literal=None line=9 column=1
PRINT lexeme='print' literal=None line=10 column=1
RETURN lexeme='return' literal=None line=11 column=1
SUPER lexeme='super' literal=None line=12 column=1
THIS lexeme='this' literal=None line=13 column=1
TRUE lexeme='true' literal=None line=14 column=1
VAR lexeme='var' literal=None line=15 column=1
WHILE lexeme='while' literal=None line=16 column=1
EOF lexeme='' literal=None line=17 column=1
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## identifiers

Allow ASCII letters, underscores and later digits; distinguish case and keyword prefixes.

**Source input:**

```text
a
Z
_
snake_case
value2
varname
True
FALSE
nilValue
anderson
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/identifiers.josh
```

**Expected stdout:**

```text
IDENTIFIER lexeme='a' literal=None line=1 column=1
IDENTIFIER lexeme='Z' literal=None line=2 column=1
IDENTIFIER lexeme='_' literal=None line=3 column=1
IDENTIFIER lexeme='snake_case' literal=None line=4 column=1
IDENTIFIER lexeme='value2' literal=None line=5 column=1
IDENTIFIER lexeme='varname' literal=None line=6 column=1
IDENTIFIER lexeme='True' literal=None line=7 column=1
IDENTIFIER lexeme='FALSE' literal=None line=8 column=1
IDENTIFIER lexeme='nilValue' literal=None line=9 column=1
IDENTIFIER lexeme='anderson' literal=None line=10 column=1
EOF lexeme='' literal=None line=11 column=1
```

**Actual stdout:**

```text
IDENTIFIER lexeme='a' literal=None line=1 column=1
IDENTIFIER lexeme='Z' literal=None line=2 column=1
IDENTIFIER lexeme='_' literal=None line=3 column=1
IDENTIFIER lexeme='snake_case' literal=None line=4 column=1
IDENTIFIER lexeme='value2' literal=None line=5 column=1
IDENTIFIER lexeme='varname' literal=None line=6 column=1
IDENTIFIER lexeme='True' literal=None line=7 column=1
IDENTIFIER lexeme='FALSE' literal=None line=8 column=1
IDENTIFIER lexeme='nilValue' literal=None line=9 column=1
IDENTIFIER lexeme='anderson' literal=None line=10 column=1
EOF lexeme='' literal=None line=11 column=1
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## numbers

Convert whole and decimal number lexemes to float, including zero and leading zeros.

**Source input:**

```text
0
0007
42
3.14
0.5
4294967296
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/numbers.josh
```

**Expected stdout:**

```text
NUMBER lexeme='0' literal=0.0 line=1 column=1
NUMBER lexeme='0007' literal=7.0 line=2 column=1
NUMBER lexeme='42' literal=42.0 line=3 column=1
NUMBER lexeme='3.14' literal=3.14 line=4 column=1
NUMBER lexeme='0.5' literal=0.5 line=5 column=1
NUMBER lexeme='4294967296' literal=4294967296.0 line=6 column=1
EOF lexeme='' literal=None line=7 column=1
```

**Actual stdout:**

```text
NUMBER lexeme='0' literal=0.0 line=1 column=1
NUMBER lexeme='0007' literal=7.0 line=2 column=1
NUMBER lexeme='42' literal=42.0 line=3 column=1
NUMBER lexeme='3.14' literal=3.14 line=4 column=1
NUMBER lexeme='0.5' literal=0.5 line=5 column=1
NUMBER lexeme='4294967296' literal=4294967296.0 line=6 column=1
EOF lexeme='' literal=None line=7 column=1
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## strings

Keep empty strings, spaces, keyword text, comment markers and Unicode inside strings.

**Source input:**

```text
""
"hello world"
"true"
"nil"
"// not a comment"
"@ é"
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/strings.josh
```

**Expected stdout:**

```text
STRING lexeme='""' literal='' line=1 column=1
STRING lexeme='"hello world"' literal='hello world' line=2 column=1
STRING lexeme='"true"' literal='true' line=3 column=1
STRING lexeme='"nil"' literal='nil' line=4 column=1
STRING lexeme='"// not a comment"' literal='// not a comment' line=5 column=1
STRING lexeme='"@ é"' literal='@ é' line=6 column=1
EOF lexeme='' literal=None line=7 column=1
```

**Actual stdout:**

```text
STRING lexeme='""' literal='' line=1 column=1
STRING lexeme='"hello world"' literal='hello world' line=2 column=1
STRING lexeme='"true"' literal='true' line=3 column=1
STRING lexeme='"nil"' literal='nil' line=4 column=1
STRING lexeme='"// not a comment"' literal='// not a comment' line=5 column=1
STRING lexeme='"@ é"' literal='@ é' line=6 column=1
EOF lexeme='' literal=None line=7 column=1
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## raw_backslash

Treat backslash-n as two ordinary characters, not an escape sequence.

**Source input:**

```text
"a\nb"
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/raw_backslash.josh
```

**Expected stdout:**

```text
STRING lexeme='"a\\nb"' literal='a\\nb' line=1 column=1
EOF lexeme='' literal=None line=1 column=7
```

**Actual stdout:**

```text
STRING lexeme='"a\\nb"' literal='a\\nb' line=1 column=1
EOF lexeme='' literal=None line=1 column=7
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## multiline_string

Keep a newline inside a string and locate the next token correctly.

**Source input:**

```text
"first
second"
42
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/multiline_string.josh
```

**Expected stdout:**

```text
STRING lexeme='"first\nsecond"' literal='first\nsecond' line=1 column=1
NUMBER lexeme='42' literal=42.0 line=3 column=1
EOF lexeme='' literal=None line=3 column=3
```

**Actual stdout:**

```text
STRING lexeme='"first\nsecond"' literal='first\nsecond' line=1 column=1
NUMBER lexeme='42' literal=42.0 line=3 column=1
EOF lexeme='' literal=None line=3 column=3
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## line_comments

Ignore comment contents, even apparent errors, and end a comment at newline or EOF.

**Source input:**

```text
1 // ignored @ " 
2//end
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/line_comments.josh
```

**Expected stdout:**

```text
NUMBER lexeme='1' literal=1.0 line=1 column=1
NUMBER lexeme='2' literal=2.0 line=2 column=1
EOF lexeme='' literal=None line=2 column=7
```

**Actual stdout:**

```text
NUMBER lexeme='1' literal=1.0 line=1 column=1
NUMBER lexeme='2' literal=2.0 line=2 column=1
EOF lexeme='' literal=None line=2 column=7
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## whitespace

Ignore spaces, tabs and CRLF while retaining later token positions.

**Source input:**

```text
 	
42	+	1
```

**Exact Python representation of input:**

```text
' \t\r\n42\t+\t1\n'
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/whitespace.josh
```

**Expected stdout:**

```text
NUMBER lexeme='42' literal=42.0 line=2 column=1
PLUS lexeme='+' literal=None line=2 column=4
NUMBER lexeme='1' literal=1.0 line=2 column=6
EOF lexeme='' literal=None line=3 column=1
```

**Actual stdout:**

```text
NUMBER lexeme='42' literal=42.0 line=2 column=1
PLUS lexeme='+' literal=None line=2 column=4
NUMBER lexeme='1' literal=1.0 line=2 column=6
EOF lexeme='' literal=None line=3 column=1
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## empty

Produce exactly EOF for an empty source file.

**Source input:**

```text
(empty)
```

**Exact Python representation of input:**

```text
''
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/empty.josh
```

**Expected stdout:**

```text
EOF lexeme='' literal=None line=1 column=1
```

**Actual stdout:**

```text
EOF lexeme='' literal=None line=1 column=1
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## comment_only

Produce EOF when the entire file is a comment without a final newline.

**Source input:**

```text
// no tokens
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/comment_only.josh
```

**Expected stdout:**

```text
EOF lexeme='' literal=None line=1 column=13
```

**Actual stdout:**

```text
EOF lexeme='' literal=None line=1 column=13
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## keyword_boundaries

Match full identifiers before testing whether they are keywords.

**Source input:**

```text
varx != nilx
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/keyword_boundaries.josh
```

**Expected stdout:**

```text
IDENTIFIER lexeme='varx' literal=None line=1 column=1
BANG_EQUAL lexeme='!=' literal=None line=1 column=6
IDENTIFIER lexeme='nilx' literal=None line=1 column=9
EOF lexeme='' literal=None line=1 column=13
```

**Actual stdout:**

```text
IDENTIFIER lexeme='varx' literal=None line=1 column=1
BANG_EQUAL lexeme='!=' literal=None line=1 column=6
IDENTIFIER lexeme='nilx' literal=None line=1 column=9
EOF lexeme='' literal=None line=1 column=13
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## number_boundaries

Keep decimal points and exponent-like text outside the number grammar as separate tokens.

**Source input:**

```text
.5 1. 1e3 1.2.3 -7
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/number_boundaries.josh
```

**Expected stdout:**

```text
DOT lexeme='.' literal=None line=1 column=1
NUMBER lexeme='5' literal=5.0 line=1 column=2
NUMBER lexeme='1' literal=1.0 line=1 column=4
DOT lexeme='.' literal=None line=1 column=5
NUMBER lexeme='1' literal=1.0 line=1 column=7
IDENTIFIER lexeme='e3' literal=None line=1 column=8
NUMBER lexeme='1.2' literal=1.2 line=1 column=11
DOT lexeme='.' literal=None line=1 column=14
NUMBER lexeme='3' literal=3.0 line=1 column=15
MINUS lexeme='-' literal=None line=1 column=17
NUMBER lexeme='7' literal=7.0 line=1 column=18
EOF lexeme='' literal=None line=1 column=19
```

**Actual stdout:**

```text
DOT lexeme='.' literal=None line=1 column=1
NUMBER lexeme='5' literal=5.0 line=1 column=2
NUMBER lexeme='1' literal=1.0 line=1 column=4
DOT lexeme='.' literal=None line=1 column=5
NUMBER lexeme='1' literal=1.0 line=1 column=7
IDENTIFIER lexeme='e3' literal=None line=1 column=8
NUMBER lexeme='1.2' literal=1.2 line=1 column=11
DOT lexeme='.' literal=None line=1 column=14
NUMBER lexeme='3' literal=3.0 line=1 column=15
MINUS lexeme='-' literal=None line=1 column=17
NUMBER lexeme='7' literal=7.0 line=1 column=18
EOF lexeme='' literal=None line=1 column=19
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## adjacent_tokens

Scan an expression without requiring spaces between tokens.

**Source input:**

```text
1+2*3==7
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/adjacent_tokens.josh
```

**Expected stdout:**

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

**Actual stdout:**

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

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## slash_or_comment

Distinguish division tokens from the // comment prefix.

**Source input:**

```text
/ //ignored
/
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/slash_or_comment.josh
```

**Expected stdout:**

```text
SLASH lexeme='/' literal=None line=1 column=1
SLASH lexeme='/' literal=None line=2 column=1
EOF lexeme='' literal=None line=2 column=2
```

**Actual stdout:**

```text
SLASH lexeme='/' literal=None line=1 column=1
SLASH lexeme='/' literal=None line=2 column=1
EOF lexeme='' literal=None line=2 column=2
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## unexpected_characters

Report multiple unexpected characters and continue scanning later tokens.

**Source input:**

```text
1 @ 2 # 3
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/unexpected_characters.josh
```

**Expected stdout:**

```text
NUMBER lexeme='1' literal=1.0 line=1 column=1
NUMBER lexeme='2' literal=2.0 line=1 column=5
NUMBER lexeme='3' literal=3.0 line=1 column=9
EOF lexeme='' literal=None line=1 column=10
```

**Actual stdout:**

```text
NUMBER lexeme='1' literal=1.0 line=1 column=1
NUMBER lexeme='2' literal=2.0 line=1 column=5
NUMBER lexeme='3' literal=3.0 line=1 column=9
EOF lexeme='' literal=None line=1 column=10
```

**Expected stderr:**

```text
[line 1, column 3] Lexical error: Unexpected character '@'.
[line 1, column 7] Lexical error: Unexpected character '#'.
```

**Actual stderr:**

```text
[line 1, column 3] Lexical error: Unexpected character '@'.
[line 1, column 7] Lexical error: Unexpected character '#'.
```

**Exit code:** expected `65`; actual `65`.

**Result:** PASS.

## unicode_identifier

Reject non-ASCII characters in identifiers.

**Source input:**

```text
café
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/unicode_identifier.josh
```

**Expected stdout:**

```text
IDENTIFIER lexeme='caf' literal=None line=1 column=1
EOF lexeme='' literal=None line=1 column=5
```

**Actual stdout:**

```text
IDENTIFIER lexeme='caf' literal=None line=1 column=1
EOF lexeme='' literal=None line=1 column=5
```

**Expected stderr:**

```text
[line 1, column 4] Lexical error: Unexpected character 'é'.
```

**Actual stderr:**

```text
[line 1, column 4] Lexical error: Unexpected character 'é'.
```

**Exit code:** expected `65`; actual `65`.

**Result:** PASS.

## unicode_digits

Reject non-ASCII digits instead of silently accepting them as numbers.

**Source input:**

```text
１２
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/unicode_digits.josh
```

**Expected stdout:**

```text
EOF lexeme='' literal=None line=1 column=3
```

**Actual stdout:**

```text
EOF lexeme='' literal=None line=1 column=3
```

**Expected stderr:**

```text
[line 1, column 1] Lexical error: Unexpected character '１'.
[line 1, column 2] Lexical error: Unexpected character '２'.
```

**Actual stderr:**

```text
[line 1, column 1] Lexical error: Unexpected character '１'.
[line 1, column 2] Lexical error: Unexpected character '２'.
```

**Exit code:** expected `65`; actual `65`.

**Result:** PASS.

## unterminated_string

Report a missing closing quote at the opening quote's position.

**Source input:**

```text
"hello
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/unterminated_string.josh
```

**Expected stdout:**

```text
EOF lexeme='' literal=None line=1 column=7
```

**Actual stdout:**

```text
EOF lexeme='' literal=None line=1 column=7
```

**Expected stderr:**

```text
[line 1, column 1] Lexical error: Unterminated string.
```

**Actual stderr:**

```text
[line 1, column 1] Lexical error: Unterminated string.
```

**Exit code:** expected `65`; actual `65`.

**Result:** PASS.

## unterminated_multiline

Locate an unterminated multiline string at its opening quote.

**Source input:**

```text

  "hello
world
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/unterminated_multiline.josh
```

**Expected stdout:**

```text
EOF lexeme='' literal=None line=3 column=6
```

**Actual stdout:**

```text
EOF lexeme='' literal=None line=3 column=6
```

**Expected stderr:**

```text
[line 2, column 3] Lexical error: Unterminated string.
```

**Actual stderr:**

```text
[line 2, column 3] Lexical error: Unterminated string.
```

**Exit code:** expected `65`; actual `65`.

**Result:** PASS.

## number_overflow

Report a number that converts to infinity instead of storing an infinite literal.

**Source input:**

```text
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/number_overflow.josh
```

**Expected stdout:**

```text
EOF lexeme='' literal=None line=1 column=401
```

**Actual stdout:**

```text
EOF lexeme='' literal=None line=1 column=401
```

**Expected stderr:**

```text
[line 1, column 1] Lexical error: Number is outside the supported range.
```

**Actual stderr:**

```text
[line 1, column 1] Lexical error: Number is outside the supported range.
```

**Exit code:** expected `65`; actual `65`.

**Result:** PASS.

## form_feed

Reject form feed because the whitespace rule only allows space, tab, CR and LF.

**Source input:**

```text
12
```

**Exact Python representation of input:**

```text
'1\x0c2'
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/form_feed.josh
```

**Expected stdout:**

```text
NUMBER lexeme='1' literal=1.0 line=1 column=1
NUMBER lexeme='2' literal=2.0 line=1 column=3
EOF lexeme='' literal=None line=1 column=4
```

**Actual stdout:**

```text
NUMBER lexeme='1' literal=1.0 line=1 column=1
NUMBER lexeme='2' literal=2.0 line=1 column=3
EOF lexeme='' literal=None line=1 column=4
```

**Expected stderr:**

```text
[line 1, column 2] Lexical error: Unexpected character '\x0c'.
```

**Actual stderr:**

```text
[line 1, column 2] Lexical error: Unexpected character '\x0c'.
```

**Exit code:** expected `65`; actual `65`.

**Result:** PASS.

## identifier_digit_boundary

Allow digits after an identifier start and end a number before letters.

**Source input:**

```text
_0 123abc
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/identifier_digit_boundary.josh
```

**Expected stdout:**

```text
IDENTIFIER lexeme='_0' literal=None line=1 column=1
NUMBER lexeme='123' literal=123.0 line=1 column=4
IDENTIFIER lexeme='abc' literal=None line=1 column=7
EOF lexeme='' literal=None line=1 column=10
```

**Actual stdout:**

```text
IDENTIFIER lexeme='_0' literal=None line=1 column=1
NUMBER lexeme='123' literal=123.0 line=1 column=4
IDENTIFIER lexeme='abc' literal=None line=1 column=7
EOF lexeme='' literal=None line=1 column=10
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## leading_zero_decimal

Keep the raw number text separately from its converted literal.

**Source input:**

```text
000.500
```

**Command:**

```bash
python -m src.main --scan test/lab1/inputs/leading_zero_decimal.josh
```

**Expected stdout:**

```text
NUMBER lexeme='000.500' literal=0.5 line=1 column=1
EOF lexeme='' literal=None line=1 column=8
```

**Actual stdout:**

```text
NUMBER lexeme='000.500' literal=0.5 line=1 column=1
EOF lexeme='' literal=None line=1 column=8
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## interactive_recovery

Recover from both an unexpected character and an unterminated string, then continue scanning.

**Source input:**

```text
@
42
"oops
"fixed"
```

**Command:**

```bash
python -m src.main --scan (enter each input line)
```

**Expected stdout:**

```text
EOF lexeme='' literal=None line=1 column=2
NUMBER lexeme='42' literal=42.0 line=1 column=1
EOF lexeme='' literal=None line=1 column=3
EOF lexeme='' literal=None line=1 column=6
STRING lexeme='"fixed"' literal='fixed' line=1 column=1
EOF lexeme='' literal=None line=1 column=8
```

**Actual stdout:**

```text
EOF lexeme='' literal=None line=1 column=2
NUMBER lexeme='42' literal=42.0 line=1 column=1
EOF lexeme='' literal=None line=1 column=3
EOF lexeme='' literal=None line=1 column=6
STRING lexeme='"fixed"' literal='fixed' line=1 column=1
EOF lexeme='' literal=None line=1 column=8
```

**Expected stderr:**

```text
[line 1, column 1] Lexical error: Unexpected character '@'.
[line 1, column 1] Lexical error: Unterminated string.
```

**Actual stderr:**

```text
[line 1, column 1] Lexical error: Unexpected character '@'.
[line 1, column 1] Lexical error: Unterminated string.
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## interactive_blank_lines

Ignore blank input, scan the next line, and exit normally at end of input.

**Source input:**

```text

  
7
```

**Command:**

```bash
python -m src.main --scan (enter each input line)
```

**Expected stdout:**

```text
NUMBER lexeme='7' literal=7.0 line=1 column=1
EOF lexeme='' literal=None line=1 column=2
```

**Actual stdout:**

```text
NUMBER lexeme='7' literal=7.0 line=1 column=1
EOF lexeme='' literal=None line=1 column=2
```

**Expected stderr:**

```text
(empty)
```

**Actual stderr:**

```text
(empty)
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## interactive_unsupported_whitespace

Reject a form-feed-only input line and recover on the next line.

**Source input:**

```text

7
```

**Exact Python representation of input:**

```text
'\x0c\n7\n'
```

**Command:**

```bash
python -m src.main --scan (enter each input line)
```

**Expected stdout:**

```text
EOF lexeme='' literal=None line=1 column=2
NUMBER lexeme='7' literal=7.0 line=1 column=1
EOF lexeme='' literal=None line=1 column=2
```

**Actual stdout:**

```text
EOF lexeme='' literal=None line=1 column=2
NUMBER lexeme='7' literal=7.0 line=1 column=1
EOF lexeme='' literal=None line=1 column=2
```

**Expected stderr:**

```text
[line 1, column 1] Lexical error: Unexpected character '\x0c'.
```

**Actual stderr:**

```text
[line 1, column 1] Lexical error: Unexpected character '\x0c'.
```

**Exit code:** expected `0`; actual `0`.

**Result:** PASS.

## Summary

28 of 28 recorded command-line runs matched the expected output and exit code.
