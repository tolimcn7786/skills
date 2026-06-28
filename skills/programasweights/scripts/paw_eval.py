#!/usr/bin/env python3
"""Compile a PAW spec, run it over a labeled test set, and report accuracy.

This automates the recommended "iterate with test cases" loop: compile a spec, run
each input, compare to the expected output, print the misses and the accuracy, and
print the program id you can reuse.

Only the official `programasweights` SDK is used. Compiling sends the spec to the
hosted PAW API; inference runs locally. Nothing else is contacted.

Install:
    pip install programasweights --extra-index-url https://pypi.programasweights.com/simple/

Usage:
    python paw_eval.py --spec spec.txt --tests tests.jsonl
    python paw_eval.py --spec spec.txt --tests tests.csv --case-insensitive --compiler paw-4b-gpt2

Test-set formats:
    JSONL: one object per line, e.g. {"input": "...", "expected": "..."}
    CSV:   header row with columns "input" and "expected"
"""

import argparse
import csv
import json
import pathlib
import sys


def load_tests(path: pathlib.Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".csv":
        rows = list(csv.DictReader(text.splitlines()))
    else:  # treat everything else as JSONL
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
    cases = []
    for i, r in enumerate(rows, 1):
        if "input" not in r or "expected" not in r:
            sys.exit(f"row {i} is missing 'input' or 'expected': {r!r}")
        cases.append({"input": str(r["input"]), "expected": str(r["expected"])})
    if not cases:
        sys.exit(f"no test cases found in {path}")
    return cases


def norm(s: str, ci: bool) -> str:
    s = s.strip()
    return s.lower() if ci else s


def main() -> None:
    ap = argparse.ArgumentParser(description="Compile a PAW spec and grade it on a test set.")
    ap.add_argument("--spec", required=True, help="Path to a file containing the spec.")
    ap.add_argument("--tests", required=True, help="Path to a JSONL or CSV test set (input/expected).")
    ap.add_argument("--compiler", default=None, help="Compiler alias (omit for the server default).")
    ap.add_argument("--slug", default=None, help="Optional slug to name the program (requires auth).")
    ap.add_argument("--case-insensitive", action="store_true", help="Compare outputs case-insensitively.")
    ap.add_argument("--max-tokens", type=int, default=None, help="max_tokens passed to inference.")
    args = ap.parse_args()

    import programasweights as paw

    spec = pathlib.Path(args.spec).read_text(encoding="utf-8")
    cases = load_tests(pathlib.Path(args.tests))

    print(f"Compiling spec ({len(spec)} chars) over {len(cases)} test cases ...")
    program = paw.compile(spec, compiler=args.compiler, slug=args.slug)
    if getattr(program, "error", None):
        sys.exit(f"compile failed: {program.error}")
    fn = paw.function(program.id)

    correct, misses = 0, []
    for c in cases:
        got = fn(c["input"], max_tokens=args.max_tokens).strip()
        if norm(got, args.case_insensitive) == norm(c["expected"], args.case_insensitive):
            correct += 1
        else:
            misses.append((c["input"], c["expected"], got))

    n = len(cases)
    print(f"\nAccuracy: {correct}/{n} = {correct / n:.0%}")
    if misses:
        print(f"\n{len(misses)} miss(es) - refine the spec/examples for these and recompile:")
        for inp, exp, got in misses:
            print(f"  input:    {inp[:80]!r}")
            print(f"  expected: {exp!r}")
            print(f"  got:      {got!r}\n")

    print(f"program id: {program.id}" + (f"  slug: {program.slug}" if getattr(program, "slug", None) else ""))
    print("Reuse it locally with:  paw.function(\"%s\")" % (program.slug or program.id))


if __name__ == "__main__":
    main()
