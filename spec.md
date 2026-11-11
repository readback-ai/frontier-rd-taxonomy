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

`T-eval` is researched. The other nine exist at level 2 as drafts (M2): task definitions, attributes and change types, with no evidence, risks or questions attached yet. A draft branch's tasks are our reading of how the work divides, not a finding.

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

The pacing model in `readback-ops` is top-down: two published models of AI R&D acceleration with a gate on deployed changes. Its gate inputs are assumptions (its README, "Where the inputs are weak or disputed"). This repository does not duplicate that model. It supplies the gate's inputs bottom-up and runs the model on them.

- **Gate quantities.** For each change type: deployed changes per researcher-year, hours to understand one, elasticity of the count to AI labor, and share of progress. They are recorded as estimates on a leaf, or higher in the tree with `change_type` set, for example one count of training improvements for all of `T-pretrain`. A change type is counted at one level only.
- **Two roles.** Training improvements, dataset updates and system software changes carry progress and take all four numbers. Monitor, evaluation and control changes and decisions are required overhead: they carry no progress and a developer cannot drop them to save review time. They take a count and hours, and are folded into the model's one required term, `monitor_changes`.
- **`taxo gate-inputs`** writes `reports/gate-inputs.yml`: each change type's numbers with basis and estimate ids, the split by branch, totals, what is missing, and a `pacing_model` block in the shape of the model's `comprehension_gate`. Counts and shares add across branches; hours and elasticities are averaged by count. `central` is the value at every input's central estimate; `low` and `high` are percentiles with the inputs varied independently.
- **`taxo sensitivity --model-dir <readback-ops>/research/pacing-takeoff-model`** imports the model from a checkout, replaces its gate assumptions with the bottom-up values, and writes `reports/sensitivity.md`: the two sets of inputs side by side, results under each mechanism, the spread over joint draws from the priors, and every input ranked by how far it moves the result. It needs the `pacing` extra (scipy) and runs Model A only. `taxo validate` warns when the gate inputs have changed since the report was run.
- **Pooling.** For the frontier, a pool of Anthropic, OpenAI and Google DeepMind replaces a `frontier` estimate wherever each of the three has its own number (decision D16).
- `data/crosswalks/` maps task ids to the activity categories in developers' own reports, so their published shares can be attached to tasks.

Research follows the ranking in `reports/sensitivity.md` (M3).

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

Decided 2026-11-11 (PI, in session, after M1):

- **D14 Gate inputs get judgment priors in M2.** No source gives a count of deployed changes, the hours to understand one, or an elasticity. Each is recorded as a wide prior with `basis: judgment`, pooled from two independent elicitations, so the pacing model can run and its inputs can be ranked for measurement. A prior is replaced when evidence arrives.
- **D15 Snapshots are kept in the organization's storage,** in Google Drive under Readback Labs, Research Data, "frontier-rd-taxonomy snapshots", or in a private dataset under the Hugging Face organization. `taxo pack-snapshots` writes the archive and `taxo restore-snapshots` unpacks one and checks it against the lock files.
- **D16 Pooled figures need Anthropic, OpenAI and Google DeepMind.** A pooled figure for a task and quantity exists only when each of the three has its own estimate, and it is the spread across them. A `frontier` estimate that cites evidence must cite all three; `taxo validate` warns otherwise. Judgment priors are exempt because they claim no evidence.

Taken as defaults by the M2 build, for the PI to confirm or change:

- **D17 A seventh change type, `control_change`,** for security, access, permission, review-rule and record-keeping changes. With monitor and evaluation changes and decisions it is required overhead in the gate. The alternative, calling these system software changes, would give them a share of progress and let the model drop them when review time is short.
- **D18 A developer-scoped estimate of external evaluation** describes the outside testing that developer commissions and what it does with the results. Estimates scoped to an evaluator, such as METR, describe the evaluator's own work and are not pooled.

Open:

1. **CL scale definitions.** `comprehension_level` is reserved until the CL0 to CL5 definitions are copied into the codebook. No comprehension estimate is recorded before then.
2. **Durable snapshot storage.** Decided (D15). The text-only archive of 2026-11-11 is in the Drive folder. The full archive with raw captures (94 MB) is not: the connector used from a session caps an upload at about 3 MB. It needs a person to add it, or a Hugging Face token in the environment.
3. **Pages that refuse automated fetches** need a person to save them; nothing from them is recorded until then. Outstanding from the M1 sweep: OpenAI's "Research acceleration: The view inside OpenAI" (2026-09-06) and "Why we no longer evaluate SWE-bench Verified" (both on openai.com), the Financial Times report of April 2025 on safety testing time, an Axios piece of 2026-07-24 on evaluators' capacity, and a Bloomberg column of 2026-03-18 on safety headcounts. Two script-rendered documents also need saving: Epoch's companion document with its sixty-odd AI R&D tasks and per-task automation ratings, and the "Steps of AI Adoption" document. OpenAI's research-acceleration figures enter today only second-hand, through the pacing model's calibration file.
4. **Who is the verifier of record.** The verifier is an agent today. The audit paper's point applies here: a model checking a model shares its blind spots. A human spot-check rate per sweep is not yet set.
5. **Scope `frontier`.** Decided (D16): pooled figures need all three developers.
6. **Gate inputs.** Decided (D14): judgment priors are recorded for every change type. None rests on evidence.
7. **Tasks the evidence pointed to and the tree lacked** now exist as drafts: `T-posttrain-environments`, `T-posttrain-harness`, `T-direction-measurement`, `T-safeguards-monitors` and `T-safeguards-operations`. Evidence already recorded with no task to attach to has not yet been re-tagged to them.
8. **M1 exit is partly met.** Three leaves have no estimate of automation or oversight (`T-eval-elicitation`, `T-eval-dangerous`, `T-eval-safeguards`) and four more lack one of the two, because no source supports one; `taxo validate` lists them as warnings. The PI has not yet been asked the slice's questions.
9. **Question wording the backtest found wanting.** The wording is unchanged so that the recorded verdicts apply to the questions as written. Proposed changes, each needing a fresh backtest: `Q-eval-tasks-02` accepts a reference solution as proof a task is solvable; `Q-eval-tasks-06` and `Q-eval-validity-04` treat public answers as a training-data risk and miss lookup at run time; `Q-eval-graders-02` and `-04` are worded for model judges and miss test suites; the transcript set assumes a review exists; `Q-eval-harness-01` and `-02` assume isolation was intended; `Q-eval-alignment-02` and `Q-eval-determination-03` measure against past practice; `Q-eval-harness-09` lists controls only and misses side effects on scoring and limits; `Q-eval-reporting-07` bundles three questions and has to be put to the outside tester when the number is theirs; `Q-eval-safeguards-07` is satisfied by a grader metric, which in one incident was the weak channel. `T-eval-external` mixes three relationships and may need splitting.
10. **Where review is the wrong control.** In 10 of 22 incidents no question was judged to surface the root cause: code bugs in graders and harnesses, score configuration errors, model behavior nobody had seen, trade-offs the team had already accepted, and behavior that left no trace in reasoning or monitor flags. These need a measurement or an enforcement mechanism. The risk register does not yet name the alternative control per risk.
11. **The unit of a deployed change is not tight enough to count with.** Two elicitations agreed within about a factor of two on hours, elasticities and progress shares. On counts of training improvements and dataset updates they differed by factors of 13 to 33: the first leaned on the pacing model's assumed 6 and 8 per researcher-year, the second built up from staffing and landing rates and got about 0.4 and 0.6. The same question decides whether a promotion decision and the training improvement it promotes are one change or two, whether an in-loop evaluation counts once as an instrument or once per use, and whether an access grant is a change. A pilot that counts changes needs this settled first.
12. **What the pacing model's gate cannot yet take.** It has one required term, so the growth of evaluation, control and monitor changes with AI labor is not modeled and their priors barely move its result. It treats review hours as interchangeable across staff, while only people in a branch can understand that branch's changes; a per-branch load needs staffing shares (`labor_share`), which are not recorded. Both are changes to the readback-ops model, not to this repository.
13. **M3 order.** `reports/sensitivity.md` ranks the inputs. First: how the count of posttraining training improvements grows with AI labor, and how many there are. Then the same elasticity for pretraining, infrastructure software and reinforcement learning environments. In 14 of 150 joint draws central audits do not hold the pace under 10x by January 2029; those draws have a progress-weighted elasticity near 0.29 against 0.55 in the rest, so the elasticity is what the audit result turns on.
