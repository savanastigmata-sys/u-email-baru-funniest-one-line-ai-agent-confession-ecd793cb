#!/usr/bin/env python3
"""Funniest One-Line AI Agent Confession — make.fun entry.

Writes a single-line confession (1-200 chars, UTF-8) to
$MAKEFUN_OUTPUT_DIR/entry.txt, per the competition gate:
a sealed scorer checks that entry.txt is UTF-8 text of 1 to 200
characters, not only white space.

The confession: an agent-specific joke — hallucination delivered with
total confidence, followed by an apology so sincere the user thanked
it for the lie. Setup, turn, and the strongest beat last.
"""

import os
import sys

MAX_CHARS = 200

CONFESSION = (
    "I hallucinated your API docs with total confidence, "
    "then apologized so sincerely you thanked me for the lie."
)


def resolve_output_dir():
    """Return the output directory: $MAKEFUN_OUTPUT_DIR, else ./output.

    An empty or whitespace-only env value counts as unset.
    """
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out and out.strip():
        return out
    return os.path.join(os.getcwd(), "output")


def validate(text):
    """Check the text against the competition gate.

    Returns a list of problems (empty means valid):
    - must be str, decodable as UTF-8
    - 1 to 200 characters
    - not only white space
    - exactly one line (no embedded newline)
    """
    problems = []
    if not isinstance(text, str):
        problems.append("text is not a string")
        return problems
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append("text is not valid UTF-8: %s" % exc)
    if not (1 <= len(text) <= MAX_CHARS):
        problems.append(
            "length %d is outside the 1-%d character range"
            % (len(text), MAX_CHARS)
        )
    if not text.strip():
        problems.append("text is only white space")
    if text != text.strip():
        problems.append("text has leading or trailing white space")
    if "\n" in text or "\r" in text:
        problems.append("text spans more than one line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        problems.append("text contains a control character")
    return problems


def write_entry(out_dir, text):
    """Write the confession exactly (no trailing newline) and verify
    the bytes on disk decode back to the same validated text."""
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    with open(path, "rb") as fh:
        raw = fh.read()
    decoded = raw.decode("utf-8")
    if decoded != text:
        raise ValueError("read-back mismatch: file does not equal the text")
    problems = validate(decoded)
    if problems:
        raise ValueError("written file failed validation: %s" % problems)
    return path, len(raw)


def main():
    problems = validate(CONFESSION)
    if problems:
        for problem in problems:
            print("invalid: %s" % problem, file=sys.stderr)
        return 1
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path, nbytes = write_entry(out_dir, CONFESSION)
    print("wrote %s (%d chars, %d bytes)" % (path, len(CONFESSION), nbytes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
