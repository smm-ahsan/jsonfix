# JsonFix

Validate JSON and see exactly where it breaks, with a caret pointing at the bad spot.

## Why the caret pointer helps

Most tools just say "invalid JSON" and leave you guessing. JsonFix prints the
offending line with a `^` caret under the exact column where parsing failed,
so a trailing comma or a missing quote is obvious at a glance, even in a long
line. That turns a frustrating hunt through a config file or an API response
into a two-second fix.

## Requirements

- Python 3
- Standard library only, nothing to install

## Usage

Validate JSON text directly:

```bash
python3 jsonfix.py --text '{"name": "Ahsan", "tags": ["a", "b"]}'
```

Validate a file:

```bash
python3 jsonfix.py --file data.json
```

Print valid JSON as one compact line instead of pretty-printed:

```bash
python3 jsonfix.py --text '{"a": 1}' --minify
```

For valid JSON, JsonFix prints `Valid JSON.`, a one-line summary of the
top-level type (`Type: object with N keys.`, `Type: array with N items.`, or
`Type: <typename>.`), then the JSON itself, pretty-printed with an indent of
2 by default.

For invalid JSON, it prints the error message with the line and column, the
offending line, and a caret line pointing at the problem column.

## Exit codes

- `0` — the JSON is valid
- `2` — the JSON is invalid (scripts and CI pipelines can rely on this)

## License

MIT, see [LICENSE](LICENSE).
