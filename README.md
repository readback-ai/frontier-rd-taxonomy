# frontier-rd-taxonomy

A maintained map of the tasks in frontier AI development: how automated each is, how much people check and understand the work, what can go wrong for safety, the review questions that expose a lack of comprehension, and bottom-up inputs for Readback's pacing model. What it does and what is decided is in [spec.md](spec.md).

This repository is private and unreleased under Readback's tiered disclosure policy; see [LICENSE](LICENSE). Agents and people working here start with [AGENTS.md](AGENTS.md).

## What is in it

| Path | Contents |
|---|---|
| `data/tasks/` | The task tree, one file per branch, with the attributes that drive risk |
| `data/sources/` | One file per published source, with its evidence items: a claim and the verbatim quote behind it |
| `data/locks/` | Snapshot hashes and verified-quote stamps. Written by the tool only |
| `data/estimates/` | Automation, oversight, shares and pacing inputs per task, each citing evidence or marked judgment |
| `data/risks/` | Failure modes, the mechanism by which automation raises each, and whether a design review would catch it |
| `data/questions/` | Review question sets per task |
| `data/incidents/` | Documented incidents with a comprehension-failure field, backtested against the questions |
| `data/interventions/`, `data/crosswalks/` | Pacing interventions; mappings to developers' own task categories |
| `reports/` | Generated. Start with [reports/coverage.md](reports/coverage.md) |
| `docs/codebook.md` | Every scale and category |
| `.agents/skills/` | The agent workflows: sweep sources, verify evidence, research a branch, draft questions, monthly sweep |

Status: the evaluation branch (`T-eval`) is researched in first draft. The other nine branches are named in the spec and not yet built.

## Reading the results

| Question | Where |
|---|---|
| What do we know and how well? | `reports/coverage.md`: evidence by grade, share of estimates that are judgment, gaps per task |
| What are the tasks and risks in a branch? | `reports/branch-eval.md` |
| What should a reviewer ask? | `reports/question-pack-eval.md` |
| Would those questions have caught real incidents? | `reports/backtest.md` |
| What does this give the pacing model? | `reports/gate-inputs.yml` |

## Set up

You need `git`, `make` and [uv](https://docs.astral.sh/uv/).

```sh
make setup
```

```sh
make check
```

`make check` lints, runs the tests, validates every record and confirms the committed reports match the records. CI runs the same command.

Snapshots of third-party pages are kept outside git, in `FRT_DATA_DIR` (default `~/frontier-rd-taxonomy-data`). You only need them to add or re-verify evidence:

```sh
uv run taxo snapshot S-anthropic-2026-09-measuring-pace
```

```sh
uv run taxo verify-quotes S-anthropic-2026-09-measuring-pace
```

## How the evidence is kept honest

- Every number cites evidence or says it is judgment. Reports show the judgment-only share.
- Every evidence quote is checked by the tool against a snapshot of the source and stamped with both hashes. Editing a quote or refreshing a snapshot voids the stamp.
- The agent that extracts evidence does not approve it. A separate verifier checks that each quote supports its claim.
- Evidence from public repositories is an analog and never grades above D.
- A site that refuses automated fetches is not worked around. A person saves the page.

Details: [spec.md](spec.md) section 6.

## Related repositories

| Repository | Relation |
|---|---|
| `readback-ops` | Holds the pacing and takeoff model (`research/pacing-takeoff-model`) that reads `reports/gate-inputs.yml`, and the deliverables this work serves |
| `readback-skills` | `quiz-me` supplies the question categories; question packs ship back there |
| `comprehension-analysis` | Source of the oversight vocabulary and metrics |
| `ai-rd-analysis` | Public-repository evidence, used here as analog only |
