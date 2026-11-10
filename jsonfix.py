#!/usr/bin/env python3
"""JsonFix - validate JSON and show exactly where it breaks.

Usage:
    python3 jsonfix.py --text '{"a": 1}'
    python3 jsonfix.py --file data.json
    python3 jsonfix.py --text '[1, 2, 3]' --minify

Exit codes: 0 = valid JSON, 2 = invalid JSON (or bad input usage).
Standard library only.
"""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Validate JSON and point at the exact spot where it breaks."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="JSON text to validate")
    group.add_argument("--file", help="Path to a file containing JSON")
    parser.add_argument(
        "--minify",
        action="store_true",
        help="Print valid JSON as one compact line instead of pretty-printed",
    )
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                raw = fh.read()
        except OSError as exc:
            print(f"Invalid JSON: could not read file: {exc}")
            return 2
    else:
        raw = args.text

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc.msg} at line {exc.lineno}, column {exc.colno}.")
        lines = raw.splitlines()
        if 1 <= exc.lineno <= len(lines):
            offending = lines[exc.lineno - 1]
        else:
            offending = ""
        print(f"Line {exc.lineno}: {offending}")
        print(" " * (len(f"Line {exc.lineno}: ") + exc.colno - 1) + "^")
        return 2

    print("Valid JSON.")
    if isinstance(data, dict):
        print(f"Type: object with {len(data)} keys.")
    elif isinstance(data, list):
        print(f"Type: array with {len(data)} items.")
    else:
        print(f"Type: {type(data).__name__}.")
    if args.minify:
        print(json.dumps(data, separators=(",", ": ")))
    else:
        print(json.dumps(data, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
