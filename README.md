# ProgramAsWeights agent skill

An [Agent Skill](https://agentskills.io) that teaches your AI coding agent to use
**[ProgramAsWeights (PAW)](https://programasweights.com)** - compile a natural-language
spec into a tiny neural function that runs locally - for fuzzy text tasks like
classification, extraction, format repair, fuzzy matching, log triage, and routing.

[![skills.sh](https://skills.sh/b/programasweights/skills)](https://skills.sh/programasweights/skills)

## Install

```bash
npx skills add programasweights/skills
```

Works with Claude Code, Cursor, Codex, GitHub Copilot, and 65+ other agents (the
[`skills` CLI](https://github.com/vercel-labs/skills) installs it into each one's skill
directory). Add `-g` to install globally for every project:

```bash
npx skills add programasweights/skills -g
```

Or try it without installing:

```bash
npx skills use programasweights/skills@programasweights | claude
```

## What it does

Once installed, the skill activates automatically when you ask your agent to do fuzzy
`text -> text` work that regex can't handle but a full LLM call per item is overkill for:

- Classify / categorize (sentiment, urgency, intent, topic, spam, ALERT vs QUIET)
- Extract fields from messy text (emails, names, dates, IDs)
- Repair / normalize formats (broken JSON, dates)
- Fuzzy / typo-tolerant matching and near-duplicate detection
- Log triage and intent routing

The agent will check the PAW Hub for a ready-made function, or compile one from a spec
with examples, iterate it against test cases, and reuse it locally.

## What's inside

```
skills/programasweights/
  SKILL.md          # the skill (trigger + workflow)
  references/       # api, writing-good-specs, browser-sdk, troubleshooting (loaded on demand)
  scripts/
    paw_eval.py     # compile a spec, run a test set, report accuracy + program id
```

## Manual install (without the CLI)

Copy `skills/programasweights/` into your agent's skills directory, e.g.:

- Claude Code: `~/.claude/skills/programasweights/`
- Codex: `~/.codex/skills/programasweights/`
- GitHub Copilot: `.github/skills/programasweights/`

## Data flow and trust

- **Compile** sends your spec to the hosted PAW API (`https://programasweights.com`) and
  returns a program id. Do not put secrets in a spec.
- **Inference runs locally** through the SDK and works offline after the first download.
- Auth is optional; the bundled `scripts/paw_eval.py` uses only the official
  `programasweights` SDK and contacts nothing else. MIT licensed; read every file before
  installing.

## Links

- Website: https://programasweights.com
- Agent guide (always current): https://programasweights.com/AGENTS.md
- Docs: https://programasweights.readthedocs.io

## License

MIT - see [LICENSE](LICENSE).
