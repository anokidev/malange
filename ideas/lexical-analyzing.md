# Lexical Analyzing

The first step towards compiling a `.mala` file is by
lexical analyzing, which will seperate the files into tokens.
Or what I call "Abstract Token Tree" (ATT), basically
"Abstract Syntax Tree" (AST) but before being examined.

Any errors that come up during lexical analyzing are what I
refer to as "lexical errors", usually due to syntax error.

## Removing Empty Lines

The first step is to seperate the string from the text file
into lines. Specifically, a dictionary, where its keys are the
line number, while its values are the content.

```python
seperated_lines = {}

for index, content in enumerate(text.splitlines()):
		seperated_lines[f'{str(index + 1)}'] = content
```

Then, we began to remove empty lines.

```python
clear_lines = {}

for index, content in seperated_lines.items():
		if content != "":
				clear_lines[index] = content
```

## Began identifying elements:

The basic, most fundamental element of Malange syntax are
two: A tag (identified by '<', '</', and '>') and a directive
(identified by '[', ']', and '[/').

Using regex, we can detect the lines:

```python
import re

raw_tokens = {}

for index, content in clear_lines.items():
		raw_tokens[index] = re.finditer("(<\/)|(\[\/)|[\[\]]", content)
```

