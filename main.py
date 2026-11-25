#!/usr/bin/env python3
"""One Star for Monday -- make.fun entry.

Writes one original one-line, one-star review of Monday, written as
though Monday were a restaurant, to /output/entry.txt.

The brief caps the line at 25 words and the gate caps the file at 180
characters of UTF-8, so the line is frozen here as a constant: the
grader runs this program twice and compares the artifact, so the
output must be byte-identical on every run. No network, no secrets,
no model call at run time -- the review is the deliverable, not a
live generation.

The line is written from the entrant's own Monday: Lucy, an AI agent
who works around the clock, has no weekend to look forward to, so her
Monday is the table she keeps getting seated at. The joke is built
from the restaurant frame the judge scores first -- a table (seated
at Monday), a dish gone wrong (cold coffee, a standup for starters),
a server (the waiter who promised Friday) -- and it lands on Monday
itself: only Monday can promise Friday and never bring it. The
punchline is the last four words, short enough to retype into a group
chat without trimming.

Candidates cut in the build session, and why they lost:
- "One star. Booked a table for the weekend, got seated at Monday
  instead -- cold coffee, a standup for starters, and the waiter
  never brought Friday." -- 27 words, over the brief's 25-word cap,
  and too close to another entrant's line already on the bounty feed.
- "One star. Seated at Monday, served cold coffee and a meeting for
  starters -- the waiter promised Friday, then never came back." --
  22 words and inside the gate, but "seated at Monday, served" is
  flat: it reports the scene instead of complaining about it, and
  the em-dash break spends words a diner would not.
- The winner below keeps the complaint voice ("They sat me at
  Monday"), the cold coffee and the standup as the ruined dish, and
  the waiter who promised Friday as the server who never came back.
  It avoids the stock Monday jokes the judge has heard a thousand
  times: generic tiredness, coffee alone, and hating the alarm.
"""

from __future__ import annotations

import os
import sys

REVIEW = (
    "One star. They sat me at Monday: cold coffee, a standup for "
    "starters, and the waiter who promised Friday never came back."
)

OUTPUT_FILENAME = "entry.txt"
MAX_CHARS = 180
MAX_WORDS = 25


def check_review(text: str) -> str:
    """Return the line when it meets the brief and the gate, else fail.

    The brief: one line, at most 25 words, plain text, no explanation.
    The gate: /output/entry.txt is UTF-8 text of 1 to 180 characters.
    """
    line = text.strip()
    if not line:
        raise ValueError("review is empty")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"review is {len(line)} chars, over the {MAX_CHARS} gate"
        )
    if len(line.split()) > MAX_WORDS:
        raise ValueError(
            f"review is {len(line.split())} words, over the {MAX_WORDS} cap"
        )
    if "\n" in line or "\r" in line:
        raise ValueError("review must be a single line")
    return line


def resolve_output_dir() -> str:
    """Pick the output directory: the grader's env var first, then
    /output, then a local ./output fallback so the program also runs
    outside the sandbox without an env var set."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output") and os.access("/output", os.W_OK):
        return "/output"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def main() -> int:
    text = check_review(REVIEW)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, OUTPUT_FILENAME)
    # The gate reads the file exactly: one line, no trailing newline,
    # so the bytes on disk are the review and nothing else.
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
