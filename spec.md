# Frontier R&D task and risk taxonomy: functional spec v0.1

Draft of 2026-11-11. Status: M0 built; M1 (evaluation branch) in first draft, not yet reviewed by the PI. Decisions are in section 9. This document says what the system does and what it produces.

## 1. Purpose

Maintain, as updatable records with code and agent instructions:

1. A taxonomy of the tasks in frontier AI development.
2. For each task, the safety risks it can give rise to, and how growing automation raises them.
3. Design-review questions that surface a lack of human comprehension in each area.
4. Evidence on how automated each task is, what humans still do, and its share of work and of progress.
5. Bottom-up inputs for the pacing model in `pacing-takeoff-model/`, so that its gate on deployed changes rests on sourced numbers where they exist and on labeled judgment where they do not.
6. The pacing model itself: how comprehension audits, internal-use lags, compute limits and sign-off change the dates of automated AI research milestones.

Everything here is public under the MIT license (D16).

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

The pacing model in `pacing-takeoff-model/` is top-down: two published models of AI R&D acceleration with a gate on deployed changes. Its gate inputs are assumptions (its README, "Where the inputs are weak or disputed"). The records and reports here do not duplicate that model, and it does not read `reports/gate-inputs.yml` yet. The taxonomy supplies the gate's inputs bottom-up:

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

Decided 2026-11-12 (PI, in session):

- **D4 The pacing model lives here.** It moved from `readback-ops/research/pacing-takeoff-model` to `pacing-takeoff-model/`. This replaces the build's default that it stay in `readback-ops`. Bottom-up still feeds top-down: the taxonomy supplies the model's gate inputs and does not reimplement it.
- **D14 The pacing model is cleared for open release.** The PI sees no meaningful information hazard in it and wants outside readers to improve it and to be persuaded by it. Superseded the same day by D16, which releases the whole repository.
- **D15 Crisp work substitutes poorly for fuzzy work.** The pacing model's elasticity of substitution between crisp and fuzzy research tasks is 0.25 on the PI's judgment. No source measures it.
- **D16 The repository is public under the MIT license.** This replaces D7. The PI judged the whole repository suitable for release: the taxonomy and question sets inform comprehension audits and the pacing model, and both improve with outside readers. D7's concern, that a ranked map of thin oversight carries capability-uplift and Goodhart exposure, was weighed and accepted. Material from Readback's private repositories stays out (AGENTS.md rule 7).
- **D17 Question sets carry a training-data canary.** With the repository public, the review questions would otherwise enter training corpora, and a model that writes the work under audit could learn to answer them fluently without the comprehension they test. Every question set and the generated question pack and backtest carry a canary string in BIG-bench's form with this repository's own GUID, and validation rejects a question set without it. The canary works only where developers filter on it.
- **D18 Fuzzy tasks are defined by supervision, following Bowkis et al. (arXiv:2605.06390).** A fuzzy task is one "without clear evaluation criteria, for which human judgement is systematically flawed", which that paper calls a hard-to-supervise fuzzy task. Everything else is in the crisp class, including tasks with no clear criteria that people judge reliably. This replaces the pacing model's earlier wording, under which crisp meant fast and cheap to verify. D20 renames the two classes.
- **D19 The labs' own usage data enter the pacing model.** Three choices. The rates on fuzzy tasks stay at +1 and +0.5 SD a year: Anthropic's TASTE benchmark has frontier models at chance on judging safety research proposals, which the PI reads as a level below the point of signal and consistent with improvement, so it is recorded as a check on the level and a test to watch and does not change a rate. The share of work that needs a person however short the task starts at 14%, OpenAI's figure for tasks under 15 minutes, and falls as AI judgment on fuzzy tasks rises. The PI holds that there is no fixed ceiling on unsupervised work. The model does not anchor on Google DeepMind's delegation data, because its models were behind the frontier for most of the period they cover; a supervision schedule fitted to its fully delegated pull requests is kept as a sensitivity only. On 2026-11-13 the PI had Anthropic's session success rates added as a third developer's figure for that share, with sensitivity runs on its starting level, its supervision time, how it falls and the audit hours (`pacing-takeoff-model/residue_sensitivity.py`). The same day the PI set the central supervision of that work to 0.5% of its time, from the PI's estimate of half an hour of a person's day for each running session, with a session doing 8 to 12 person-days of work in a day. No developer reports that figure. Three benchmarks scored against human judgment (a rerun of TASTE, RedwoodBench and LMCA) were read from chart images the PI supplied; their pages were not fetched and are not source records. The five reports behind this (Google DeepMind's Gemini 4 Argon safety report, the TASTE page, Ramez Naam's essay, and Anthropic's "When AI builds itself" and "How employment is changing at Anthropic") are not yet source records here.
- **D20 The pacing model's two task classes are named supervisable and HTS fuzzy.** Decided by the PI on 2026-11-13. The slow class is the hard-to-supervise fuzzy tasks of Bowkis et al., HTS fuzzy for short. The fast class is everything else and is called supervisable, because it is defined by people being able to judge the work. It holds that paper's crisp tasks and the fuzzy tasks people judge reliably. The earlier labels, crisp and fuzzy, made benchmarks scored against human judgment look like evidence on the wrong class. Keys, parameter names and result file names in the model's code use the same two names. They kept the earlier labels for one day and were renamed on the PI's instruction before the next rerun; the one saved file that held an old key, a results meta file, was migrated.
- **D21 Supervisable work has a weight of 80% in the pacing model.** Decided by the PI on 2026-11-13. It was 65%, the importance-based anchor. No source measures the weight. The three anchors give 60% to 84% and separate well-defined work from the rest, which is wider than the HTS fuzzy class, so they are a floor. The PI moved the central value after three arguments that point above them: Bowkis et al. say fuzzy tasks are more prevalent in alignment research than in capabilities research, benchmarks scored against human judgment rise with general capability, and Dwarkesh Patel's essay of 2026-11-13 argues that AI research has verifiable proxies for its main kinds of work. The model is also run at 50%, 65% and 90%. Patel's essay is not yet a source record here.

Taken as defaults by the build, for the PI to confirm or change:

- **D5 Question structure.** Categories follow `quiz-me` (what, why, failure, dependency, side effects) and topical areas follow the audit paper's Table 4. A sixth category, `provenance`, is added. `readback-skills` asks that changes to question wording be agreed first, so `provenance` is a proposal until confirmed.
- **D6 Two added change types.** `evaluation_change` and `decision`, beside the pacing model's four.
- **D7 Private repository, all rights reserved,** under the tiered disclosure policy (`readback-ops/decisions/0002`). A ranked map of where frontier oversight is thinnest has capability-uplift and Goodhart exposure. Replaced by D16 on 2026-11-12.
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
8. **M1 exit is partly met.** Three leaves have no estimate of automation or oversight (`T-eval-elicitation`, `T-eval-dangerous`, `T-eval-safeguards`) and four more lack one of the two, because no source supports one; `taxo validate` lists them as warnings. The PI has not yet been asked the slice's questions.
9. **Question wording the backtest found wanting.** The wording is unchanged so that the recorded verdicts apply to the questions as written. Proposed changes, each needing a fresh backtest: `Q-eval-tasks-02` accepts a reference solution as proof a task is solvable; `Q-eval-tasks-06` and `Q-eval-validity-04` treat public answers as a training-data risk and miss lookup at run time; `Q-eval-graders-02` and `-04` are worded for model judges and miss test suites; the transcript set assumes a review exists; `Q-eval-harness-01` and `-02` assume isolation was intended; `Q-eval-alignment-02` and `Q-eval-determination-03` measure against past practice; `Q-eval-harness-09` lists controls only and misses side effects on scoring and limits; `Q-eval-reporting-07` bundles three questions and has to be put to the outside tester when the number is theirs; `Q-eval-safeguards-07` is satisfied by a grader metric, which in one incident was the weak channel. `T-eval-external` mixes three relationships and may need splitting.
10. **Where review is the wrong control.** In 10 of 22 incidents no question was judged to surface the root cause: code bugs in graders and harnesses, score configuration errors, model behavior nobody had seen, trade-offs the team had already accepted, and behavior that left no trace in reasoning or monitor flags. These need a measurement or an enforcement mechanism. The risk register does not yet name the alternative control per risk.
11. **What the pacing model's move leaves undone.** Two things. Sources: `S-readback-2026-11-pacing-takeoff-briefing` and `S-readback-2026-11-pacing-calibration` cite the files at their old address on a `readback-ops` working branch; they need a new address and a fresh snapshot through the tool, and the briefing has changed since it was snapshotted. Vocabulary: the briefing keeps the wording it was written in, which departs from the glossary in four places. "Research judgment" and "taste" mean the AI Futures Model's research taste, where the glossary's judgment is an estimate with no evidence behind it. "Assumption" marks what the glossary calls a judgment. "Supervision" is the glossary's oversight. "Understand" means comprehend to the audit standard.
12. **Supervisable and HTS fuzzy tasks.** The pacing model splits research judgment into supervisable and HTS fuzzy tasks (D18, D20). It takes the weight of supervisable work as 65%, anchored on a survey of scientists' importance ratings, one set of interviews with AI researchers and one developer's breakdown of agent output; none measures the quantity itself. The task tree's `verifiability` and `feedback_latency` attributes with `labor_share` and `advance_share` could supply that weight bottom-up. Neither attribute records whether human judgment on the task is reliable, which D18's definition turns on, so which leaves count as HTS fuzzy is not decided. The anchors separate well-defined work from the rest and so overstate the HTS fuzzy class as D18 defines it. The two reports behind the anchors (Epoch AI's 2024 interviews and Anthropic's 2026 study of how researchers use Claude) are not yet source records here.
