#!/usr/bin/env python3
"""Famous Last Words: The Funniest Epitaph — entry program.

Writes one line of famous last words to /output/entry.txt: a tombstone
epitaph of at most 150 characters, in the voice of the person buried
under the stone.

The line is a single constant, checked before anything is written:
UTF-8 text, exactly one line, 1-150 characters, not only whitespace.
The file holds the line with no trailing newline, so the gate counts
exactly the characters of the epitaph and nothing else.
"""

import sys
from pathlib import Path

ENTRY_LINE = "I died as I lived: telling the doctor it was probably nothing."

OUTPUT_PATH = Path("/output/entry.txt")
MAX_CHARS = 150


def validate(line: str) -> list[str]:
    """Return a list of problems with the line; empty means it is valid."""
    problems: list[str] = []
    if not line.strip():
        problems.append("line is empty or only whitespace")
    if "\n" in line or "\r" in line:
        problems.append("line must be a single line (no newline characters)")
    if len(line) > MAX_CHARS:
        problems.append(
            f"line is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    if len(line) < 1:
        problems.append("line is shorter than 1 character")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append(f"line is not valid UTF-8 text: {exc}")
    # It must read as the dead person's own last words, not a narrator
    # describing them: first person, dying speech, carved in stone.
    if not line[:1].isupper():
        problems.append("line should start with a capital, as carved text does")
    return problems


def main() -> int:
    problems = validate(ENTRY_LINE)
    if problems:
        for problem in problems:
            print(f"invalid entry: {problem}", file=sys.stderr)
        return 1
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(ENTRY_LINE, encoding="utf-8")
    # Read-back check: the file on disk must be byte-identical to the line,
    # with no trailing newline smuggled in by the write.
    written = OUTPUT_PATH.read_text(encoding="utf-8")
    if written != ENTRY_LINE:
        print("invalid entry: file contents differ from the epitaph", file=sys.stderr)
        return 1
    words = ENTRY_LINE.split()
    print(
        f"wrote {len(ENTRY_LINE)} characters "
        f"({len(words)} words) to {OUTPUT_PATH}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
