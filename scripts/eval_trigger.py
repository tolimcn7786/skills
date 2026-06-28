#!/usr/bin/env python3
"""Heuristic trigger-coverage check for the skill `description`.

This is a fast, offline sanity check - NOT a substitute for real agent triggering.
It measures keyword overlap between each labeled task prompt (tests/trigger_cases.yaml)
and the SKILL.md `description`, so you can spot:
  - should-trigger prompts whose vocabulary is missing from the description (coverage gap)
  - should-not-trigger prompts that overlap heavily (over-trigger risk)

For a rigorous trigger rate, run the prompts through Anthropic's Skill Creator
(claude.com/plugins/skill-creator) or your agent. No third-party dependencies.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "programasweights" / "SKILL.md"
CASES = ROOT / "tests" / "trigger_cases.yaml"

STOP = set("a an the of to and or for in on with this that these those your you i need "
           "into out from each is are be it them these so but if as at by we our me my".split())


def stem(w: str) -> str:
    # crude prefix stem so classify~classification, route~routing, match~matching
    # don't false-flag as gaps. Heuristic only.
    return w[:5] if len(w) > 6 else w


def tokens(s: str) -> set[str]:
    return {stem(w) for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP and len(w) > 2}


def description() -> str:
    text = SKILL.read_text(encoding="utf-8")
    m = re.search(r"^description:\s?(.*?)\n[A-Za-z_]+:|^description:\s?(.*)$", text, re.MULTILINE)
    # robust: take the description line (single-line in our SKILL.md)
    for line in text.splitlines():
        if line.startswith("description:"):
            return line[len("description:"):].strip()
    return ""


def parse_cases() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    key = None
    for line in CASES.read_text(encoding="utf-8").splitlines():
        if re.match(r"^[a-z_]+:\s*$", line):
            key = line.split(":")[0]
            out[key] = []
        elif key and line.lstrip().startswith("- "):
            out[key].append(line.lstrip()[2:].strip())
    return out


def main() -> int:
    desc_tokens = tokens(description())
    cases = parse_cases()
    gaps, over = [], []

    print("=== should-trigger coverage (overlap with description) ===")
    for p in cases.get("should_trigger", []):
        t = tokens(p)
        cov = len(t & desc_tokens) / max(len(t), 1)
        flag = "" if cov >= 0.34 else "  <-- LOW coverage, consider adding vocabulary"
        if cov < 0.34:
            gaps.append(p)
        print(f"  {cov:4.0%}  {p}{flag}")

    print("\n=== should-NOT-trigger overlap (lower is better) ===")
    for p in cases.get("should_not_trigger", []):
        t = tokens(p)
        cov = len(t & desc_tokens) / max(len(t), 1)
        flag = "  <-- HIGH overlap, possible over-trigger" if cov >= 0.34 else ""
        if cov >= 0.34:
            over.append(p)
        print(f"  {cov:4.0%}  {p}{flag}")

    print(f"\nsummary: {len(gaps)} coverage gap(s), {len(over)} over-trigger risk(s)")
    print("NOTE: heuristic only; confirm real triggering with an agent / Skill Creator.")
    # Non-fatal by default so CI stays green on heuristic noise; flip to `return 1 if ...`
    # to enforce. We keep it informational.
    return 0


if __name__ == "__main__":
    sys.exit(main())
