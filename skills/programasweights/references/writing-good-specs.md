# Writing and debugging PAW specs

The single highest-leverage practice: **iterate with test cases.** Do not accept low
performance on the first try. Treat spec writing like software engineering - test, debug
the specific failures, fix the wording, retest.

## Anatomy of a good spec

A description PLUS a few `Input: ... Output: ...` examples PLUS an explicit output
constraint:

```python
fn = paw.compile_and_load("""
Classify user intent. Return ONLY one of: search, create, delete, other.

Input: Find the latest report
Output: search

Input: Make a new folder
Output: create

Input: Remove old backups
Output: delete
""")
```

## Tips

- **State output constraints explicitly** - "Return ONLY one of: X, Y, Z". Without this
  the model may produce free-form text.
- **Use examples from your actual data** - real examples outperform prose-only descriptions.
- **Debug failures before sweeping** - look at specific failing inputs and understand WHY
  before trying many variants.
- **Keep it inside the window** - spec + input + output share ~2048 tokens. For long
  inputs, trim or pre-chunk.

## The compile -> test -> iterate loop

1. Write a first spec with a few examples.
2. Build a small test set of `input -> expected` pairs (10-30 covers most signal).
3. Compile, run the test set, look at the misses.
4. Add or fix examples / tighten the wording, recompile, re-measure.
5. Stop when accuracy is good enough; save the program id or slug and reuse it.

`scripts/paw_eval.py` in this skill runs steps 3-4: it compiles a spec, runs a
JSONL/CSV test set, prints accuracy and the specific failures, and prints the program id.

```bash
python scripts/paw_eval.py --spec spec.txt --tests tests.jsonl
```

More worked examples and case studies: https://programasweights.readthedocs.io
