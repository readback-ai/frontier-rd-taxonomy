---
name: draft-questions
description: Write or revise the review question set for one task's contributions, and backtest the questions against the incident library. Use when asked to draft, revise or backtest design-review or comprehension-audit questions.
---

# Draft and backtest review questions

A question set is what a reviewer or comprehension auditor brings to one kind of contribution. Its job is to show whether the accountable people understand what they approved. Read `docs/codebook.md` sections 5 to 7 and `reports/question-pack-eval.md` for the house pattern.

## Before writing

Read, for the task: its record in `data/tasks/`, its risks, its incidents and the evidence they cite. A question that is not aimed at a recorded risk does not belong; if you find yourself wanting one, the missing thing is a risk.

## Writing the set

1. **Start the file with the canary line** copied from an existing set in `data/questions/`. `taxo validate` rejects a set without it.
2. **State the contribution** the set is for, in one line: "A new model judge and its prompt for a behavioral evaluation."
3. **Cover the five categories** (`what`, `why`, `failure`, `dependency`, `side_effects`) and add `provenance` questions where a model produced or checked part of the work.
4. **Cover both tiers.** Deep-tier areas (`architecture_design`, `implementation_behavior`, `process`) and familiarity-tier areas (`key_findings`, `analysis_of_results`).
5. **Six to ten questions.** Combine questions that overlap.
6. For each question write what a good answer shows, one to three red flags, and the record to ask for.

### What makes a question work here

- **Altitude.** Answerable by someone who understands the design, without the code or transcripts open and without asking a model. Too low: "What threshold does the judge use?" Right: "What would the judge do with an answer that is correct but phrased unlike any example it was shown, and how do you know?"
- **It separates understanding from having been told.** Prefer questions whose honest answer differs between someone who examined the work and someone who read the agent's summary: predictions ("what happens if"), counterfactuals ("what result would have changed your decision"), and boundaries ("which part of this did a person read").
- **It asks for a mechanism of detection.** For any claim of correctness: how would you know if it were wrong, and has that check ever fired?
- **It is specific to the task's silent failures.** Use the task's `failure_visibility` and `verifiability`. For a `silent`, `deferred` task, the central question is what independent ground truth exists.
- **It does not presume bad faith.** The review is Socratic and blameless.

### Red flags to listen for

Write red flags as things said or missing: "The agent's write-up said so." "We would see it in the score." "Nobody has opened the transcripts." "It was the same model." "There was no time."

## Backtest

For each incident that lists this task:

1. Read the incident and its evidence.
2. For each question in the set, ask: if the contributors had been asked this before the incident and answered honestly, would the root cause have come out?
3. Record a verdict in the incident's `backtest` with a one or two sentence rationale: `would_surface`, `might_surface`, `would_not_surface`.

Rules:

- Judge from what the source says people knew at the time. Do not assume knowledge the source does not show.
- A question that needs the reviewer to already suspect the answer is `might_surface` at best.
- Record `would_not_surface` verdicts. If no question would have surfaced an incident, do not write a question to fit it after the fact unless the question generalizes; say in the risk's `review_rationale` that review is the wrong control.
- Do not backtest your own questions. Start a `general-purpose` subagent, give it the question set and the incident files, and have it return verdicts. Apply them, and note in the pull request where you disagreed.

## Finish

`uv run taxo validate` (every question names a risk; every review-catchable risk has a question), `uv run taxo report`, then read `reports/backtest.md`. The headline is how many incidents have at least one `would_surface`, and which questions never fire.

Question wording is the product. Changes to the wording of an existing set go to the PI as a draft before they merge.
