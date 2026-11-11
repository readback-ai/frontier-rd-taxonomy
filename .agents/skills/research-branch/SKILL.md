---
name: research-branch
description: Take a branch or task group of the taxonomy from a task tree through evidence, estimates, risks, incidents and review questions, to a pull request with a readback. Use when asked to research, build out or update a branch or task group.
---

# Research a branch

Read `spec.md` sections 3 to 7, `GLOSSARY.md` and `docs/codebook.md` first. `data/tasks/T-eval.yml` and the records that cite it are the worked example.

Work in this order. Each step has an exit check; do not go on until it holds.

## 1. Task tree

Write or revise `data/tasks/<branch>.yml` with `status: draft`.

- Find the developers' own task categories first (their measurement reports list them; see `data/crosswalks/`). Name tasks the way practitioners do.
- Split a leaf when two of its contributions would get different attributes (codebook 1.1).
- Give each leaf its `contributions`: two or three concrete examples of what gets approved or deployed.
- Rate each attribute and write the `rationale`. If you cannot say why a value holds, you do not know the task well enough yet; go to step 2 and come back.

Exit: `uv run taxo validate` shows no errors for the branch.

## 2. Evidence

Run `sweep-sources` for the branch, split by source family so several researchers can work in parallel. Then run `verify-evidence` on everything added.

Exit: every item verified mechanically and by the verifier; searches that found nothing are written down.

## 3. Estimates

For each leaf, in `data/estimates/<task>.yml`:

- `automation_level` and `oversight_mode` at least. Shares and gate inputs where there is anything to go on.
- Start from what the evidence fixes. Use `scope` for one developer when the evidence is about one developer. Estimate `frontier` only when you can say why it generalizes.
- If nothing constrains the value, either leave it out or record it as `judgment` with wide bounds and low confidence. A judgment estimate is worth recording when the pacing model needs the cell; say so in `reasoning`.
- Never average an analog number into a frontier estimate.
- Estimate each of Anthropic, OpenAI and Google DeepMind separately. A pooled figure exists only where all three have their own estimate (spec decision D16), so a leaf with one developer is a gap to report, not a result. Check `reports/coverage.md`, "Pooled across", for who is missing.
- Gate quantities with no evidence get a judgment prior from two independent elicitations (`docs/codebook.md`, section 4). The second estimator must not see the first's numbers or the pacing model's assumptions.

Exit: each estimate's `reasoning` can be followed from the cited quotes by someone who has not read the sources.

## 4. Incidents

One file per incident that touches the branch, from the evidence of kind `incident`. Fill the comprehension-failure field from what the source says, and use `unknown` freely (codebook 7).

## 5. Risks

For each leaf, ask: how can this output be wrong in a way that matters for safety, and what does automation change about how likely that is or how visible? Write one risk per failure mode.

- Name every mechanism that applies. Do not default to `comprehension_gap`.
- Decide `review_catchable` honestly. A risk that works through a model hiding something, or through data nobody can read in full, is `no` or `partly`.
- `status` follows the evidence: `observed_frontier` needs an incident or an item from a frontier developer.

Exit: every leaf has a risk; every `observed` status has its evidence.

## 6. Questions

Run `draft-questions` for each leaf.

## 7. Close out

- Set the branch `status: researched`. `uv run taxo validate` now warns on every gap; fix what you can honestly fix and leave the rest.
- `uv run taxo report` and read `reports/branch-<name>.md` and `reports/coverage.md` as a reader would. If a table looks wrong, a record is wrong.
- `make check`.
- Open a pull request with the readback section from `AGENTS.md`. List the judgment-only share for the branch and the three estimates you trust least.
