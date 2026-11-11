# Frontier R&D task and risk taxonomy: functional spec v0.1

Draft of 2026-11-11. Status: M0 built; M1 (evaluation branch) in first draft, not yet reviewed by the PI. Decisions are in section 9. This document says what the system does and what it produces.

## 1. Purpose

Maintain, as updatable records with code and agent instructions:

1. A taxonomy of the tasks in frontier AI development.
2. For each task, the safety risks it can give rise to, and how growing automation raises them.
3. Design-review questions that surface a lack of human comprehension in each area.
4. Evidence on how automated each task is, what humans still do, and its share of work and of progress.
5. Bottom-up inputs for the pacing model in `readback-ops/research/pacing-takeoff-model`, so that its gate on deployed changes rests on sourced numbers where they exist and on labeled judgment where they do not.

It serves these deliverables in `readback-ops/strategy/deliverables.md`: E2 (RSI-metrics schema and gap analysis), E4 (precursor registry: the incident library carries its comprehension-failure field), E5 (automation tracker paired with oversight capacity), A1 (safety-case review series: where a case relies on staff understanding) and P2 (comprehension-audit standard: the question sets are audit agenda templates).

## 2. Scope

- Developers training frontier language models. Chip design and datacenter construction are outside the tree; they enter the pacing model as compute.
- Ten branches (section 4). Evaluation is researched first.
- Evidence priority: incident reports, risk reports, system cards and third-party investigations first; then developers' own measurement reports and research posts; then staff statements and press. Public repositories are analogs for examples only, because they lag frontier practice (decision D2).

## 3. The three quantities

Automation, oversight and comprehension are recorded separately (`GLOSSARY.md`). The claim that automation raises risk through lost understanding is the gap between the first and the third. It is a hypothesis to test task by task. Each risk therefore names its mechanism, and comprehension gap is one of eight. Each risk also says whether a design review would catch it, so the question sets do not claim coverage they lack.

## 4. The task tree

Branches, defined by function:

| Branch | Covers |
|---|---|
| `T-infra` | Compute and infrastructure software: schedulers, kernels and compilers, training frameworks, storage, inference serving, experiment tooling, build and deploy |
| `T-data` | Data: acquisition, filtering, synthetic generation, mixture design, human data, provenance |
| `T-pretrain` | Pretraining: architecture and optimizer research, small-scale experiments and scaling prediction, large-run execution |
| `T-midtrain` | Midtraining: continued training on curated or synthetic corpora, knowledge and context extension, specification and character corpora |
| `T-posttrain` | Posttraining: supervised and preference tuning, reinforcement learning, environments, rewards and graders, safety training, distillation, harness and system prompt |
| `T-eval` | Evaluation: instruments, assessments, interpretation, reporting and release decisions, external evaluation |
| `T-safeguards` | Safeguards and monitoring: classifiers, monitors, control protocols, interpretability used for assurance |
| `T-agents` | Internal agent deployment: harnesses, permissions, sandboxes, the automation that does the other branches |
| `T-security` | Security: weights, access, logging, change management |
| `T-direction` | Research direction and decisions: prioritization, compute allocation, interpreting results, scale and ship decisions |

Only `T-eval` exists as records. The others are created when researched (milestone M2).

Each leaf carries the attributes that drive risk: output role, verifiability, feedback latency, failure visibility, reversibility, privilege and change type (`docs/codebook.md` section 1).

## 5. Records

YAML under `data/`, validated by `src/frontier_taxonomy/schema.py`.

| Folder | One file per | Holds |
|---|---|---|
| `sources/` | source | The source and its evidence items |
| `locks/` | source | Snapshot hash and verified-quote stamps. Machine-written |
| `tasks/` | branch | The branch's task tree and attributes |
| `estimates/` | task | Estimates of automation, oversight, shares and gate inputs |
| `risks/` | risk | Failure mode, harm path, mechanisms, review-catchable, evidence |
| `questions/` | task | The question set for the task's contributions |
| `incidents/` | incident | What happened, root cause, comprehension-failure field, backtest |
| `interventions/` | intervention | What it targets and how it maps to a pacing-model policy |
| `crosswalks/` | external taxonomy | How its categories map to task ids here |

A branch marked `researched` is expected to have, for every leaf: attributes, an automation estimate, an oversight estimate, at least one risk and a question set. Gaps are validation warnings.

## 6. Integrity rules

Enforced by `taxo validate`, which CI runs.

1. **No number without a basis.** An estimate cites evidence or says `basis: judgment`. Reports count judgment-only estimates and show the share.
2. **Quotes are verbatim and verified.** Every evidence item quotes its source. `taxo verify-quotes` checks each quote against the snapshot text and stamps it in the source's lock file with the hash of the quote and of the snapshot. Editing a quote or refreshing a snapshot voids the stamp. An unstamped quote is an error unless the item carries `unverified_reason`.
3. **Snapshots stay out of git.** Third-party text lives in `FRT_DATA_DIR`; its hash, retrieval date and the short quotes are committed. CI never fetches a source; it checks lock files.
4. **A site's refusal is respected.** If a site refuses automated fetches, a person saves the page and the snapshot is taken from the file. No workaround.
5. **Researcher and verifier are separate.** The agent that extracts evidence does not approve it. A verifier with no view of the researcher's reasoning checks that each quote supports its claim (`verify-evidence` skill).
6. **Source type caps the grade.** Analog evidence never grades above D.
7. **References resolve.** Every id a record names exists.
8. **Reports are generated.** `taxo report` writes everything under `reports/`. CI fails if the committed reports differ from what the records produce.
9. **Estimates go stale.** Each has a `stale_after` date. Past it, validation warns.
10. **A change to a conclusion carries a readback.** A pull request that changes an estimate, a risk's status or severity, or a question says what moved, why, and what the PI should be able to explain about it (`AGENTS.md`).

## 7. Pacing interface

The pacing model in `readback-ops` is top-down: two published models of AI R&D acceleration with a gate on deployed changes. Its gate inputs are assumptions (its README, "Where the inputs are weak or disputed"). This repository does not duplicate that model. It supplies the gate's inputs bottom-up:

- `taxo gate-inputs` writes `reports/gate-inputs.yml`: for each change type, the count per researcher-year, hours to understand one, elasticity to AI labor and share of progress, combined from leaf-task estimates, each cell with its basis and estimate ids. Counts and shares add across tasks; hours and elasticities are averaged by count.
- It also reports the share of a researcher-year needed to understand everything deployed, by change type, sampled from the ranges. The pacing model's figure for all types is 15%.
- The file lists which cells have no estimate. The pacing model keeps its assumption for those.
- `evaluation_change` and `decision` are change types the pacing model does not have. Its `monitor_change` type covers part of what `T-eval-safeguards` and the future `T-safeguards` branch produce.
- `data/crosswalks/` maps task ids to the activity categories in developers' own reports, so their published shares can be attached to tasks.

Sensitivity analysis in the pacing model ranks its inputs. Its README names the elasticity of deployed changes as the parameter to measure first. Research here follows that ranking (M3).

## 8. Milestones

| | Work | Exit |
|---|---|---|
| M0 | Schema, validators, quote verification, reports, CI, agent instructions, glossary, codebook | `make check` green; quotes verified on real sources |
| M1 | Evaluation branch end to end | Every leaf has attributes, estimates, a risk and questions; incidents backtested; the PI can answer the slice's questions |
| M2 | Remaining branches to level 2; crosswalks to developers' task categories; gate inputs for every change type on wide priors | Pacing-model sensitivity run on bottom-up inputs; ranked list of parameters to research |
| M3 | Evidence on the top-ranked parameters; risk register across branches | High-risk leaves graded; judgment-only share reported per branch |
| M4 | Question sets for high-risk leaves, backtested | Question pack shipped to `readback-skills` |
| M5 | Interventions mapped to pacing-model policies; results | Report and dated forward claims for the E1 registry |
| M6 | Monthly sweep, staleness flags, changelog of changed conclusions | Runs with the PI reviewing deltas |

## 9. Decisions

Decided 2026-11-11 (PI, in session):

- **D1 Evaluation first.** It is the measurement layer the other branches lean on and has the most public evidence and documented incidents.
- **D2 Open-source evidence is analog only.** Public repositories lag frontier practice. They supply examples and never grade above D. `ai-rd-analysis` results enter as `open_source_analog` sources.
- **D3 Evidence priority.** Incident reports, risk reports, system cards and third-party investigations come first, found by literature review and agent search.

Taken as defaults by the build, for the PI to confirm or change:

- **D4 Bottom-up feeds top-down.** The pacing model stays in `readback-ops`. This repository supplies its gate inputs and does not reimplement it.
- **D5 Question structure.** Categories follow `quiz-me` (what, why, failure, dependency, side effects) and topical areas follow the audit paper's Table 4. A sixth category, `provenance`, is added. `readback-skills` asks that changes to question wording be agreed first, so `provenance` is a proposal until confirmed.
- **D6 Two added change types.** `evaluation_change` and `decision`, beside the pacing model's four.
- **D7 Private repository, all rights reserved,** under the tiered disclosure policy (`readback-ops/decisions/0002`). A ranked map of where frontier oversight is thinnest has capability-uplift and Goodhart exposure. Nothing here is released without the policy's review.
- **D8 Snapshots outside git,** following `comprehension-analysis` for third-party data. Hashes and short quotes are committed.
- **D9 Grades measure directness, not trustworthiness.** A developer's self-reported measurement is grade A. Self-interest and redaction go in `limits` and lower estimate confidence.
- **D10 The grade follows who is speaking about whose work, item by item.** An evaluator reporting on its own evaluation is first party for that item; its reading of a developer's practice without internal access is C. Forecasts and general remarks are C. Adopted after the first verifier pass found the researchers applying this rule unwritten (codebook 3.4).
- **D11 `incident_report` covers any organization whose work failed,** including evaluators and benchmark builders.
- **D12 In-loop evaluation includes release regression checks** on serving and product changes, so the two postmortems where such checks passed and users found the fault attach to `T-eval-inloop` directly.
- **D13 Paywalled text is not used** even when a plain fetch returns it. Four items from one press summary were removed on this ground.

Open:

1. **CL scale definitions.** `comprehension_level` is reserved until the CL0 to CL5 definitions are copied into the codebook. No comprehension estimate is recorded before then.
2. **Durable snapshot storage.** Snapshots taken in a cloud session vanish with it. Options: a private data repository, a private Hugging Face dataset, or Drive. Until decided, a re-snapshot that differs voids the stamps and quotes are re-verified.
3. **Pages that refuse automated fetches** need a person to save them; nothing from them is recorded until then. Outstanding from the M1 sweep: OpenAI's "Research acceleration: The view inside OpenAI" (2026-09-06) and "Why we no longer evaluate SWE-bench Verified" (both on openai.com), the Financial Times report of April 2025 on safety testing time, an Axios piece of 2026-07-24 on evaluators' capacity, and a Bloomberg column of 2026-03-18 on safety headcounts. Two script-rendered documents also need saving: Epoch's companion document with its sixty-odd AI R&D tasks and per-task automation ratings, and the "Steps of AI Adoption" document. OpenAI's research-acceleration figures enter today only second-hand, through the pacing model's calibration file.
4. **Who is the verifier of record.** The verifier is an agent today. The audit paper's point applies here: a model checking a model shares its blind spots. A human spot-check rate per sweep is not yet set.
5. **Scope `frontier`.** Most graded evidence is from one developer. M1 records estimates per developer and uses `frontier` once, where the source covers four developers. Whether `frontier` estimates should exist at all is open; the gate-input export reads scope `frontier` and is empty for evaluation until this is settled or per-developer exports are added.
6. **Gate inputs for evaluation.** No source gives a count of evaluation contributions per researcher, the hours to understand one, or how the count grows with AI labor. M1 records none. M2 can add judgment priors so the pacing model can run, or the cells can stay empty until a pilot measures them.
7. **Tasks the evidence pointed to and the tree lacks.** Vetting of reinforcement learning environments, release checks on product and serving changes, measurement of automation and oversight itself, and monitoring of internal agents all had evidence with no evaluation task to attach to. They belong to `T-posttrain`, `T-infra`, `T-direction` and `T-safeguards` when those are built.
