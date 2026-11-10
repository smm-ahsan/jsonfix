# JsonFix examples

Real captured output from actual runs.

## Valid JSON (object)

```bash
python3 jsonfix.py --text '{"name": "Ahsan", "tags": ["a", "b"]}'
```

Output (exit code 0):

```
Valid JSON.
Type: object with 2 keys.
{
  "name": "Ahsan",
  "tags": [
    "a",
    "b"
  ]
}
```

## Invalid JSON (trailing comma)

```bash
python3 jsonfix.py --text '{"name": "Ahsan",}'
```

Output (exit code 2):

```
Invalid JSON: Expecting property name enclosed in double quotes at line 1, column 18.
Line 1: {"name": "Ahsan",}
                         ^
```

The caret sits under the exact column where parsing failed, so the problem
character is visible at a glance.
