# Codebook

How to fill in every field that takes a category or a scale. `GLOSSARY.md` defines the terms; `src/frontier_taxonomy/schema.py` enforces the allowed values. If a case does not fit, raise it on an issue. Do not stretch a category to cover it.

Version 0, 2026-11-11. Written against the evaluation branch. Expect revisions as other branches are researched; hard cases become worked examples here.

## 1. Tasks

### 1.1 The tree

- Level 1 is a branch: a stage or function of frontier development (evaluation, data, pretraining and so on). Stages are defined by function, since developers name them differently.
- Level 2 groups tasks the pacing model treats together.
- Leaves are tasks whose contributions share one risk profile. Split a leaf when two of its contributions would get different attributes. Writing an RL environment and writing its grader are different leaves.

### 1.2 Attributes of a leaf

Rate the task as it is done at a frontier developer today. Write the reason in `rationale`.

**`output_roles`**: what the output does. One or more.

| Value | The output | Example |
|---|---|---|
| `shapes` | Changes what the model becomes | Training data, reward functions, a model spec |
| `measures` | Tells people what the model is or does | Evaluations, graders, monitors' recall tests |
| `contains` | Limits what the model can do or reach | Sandboxes, permissions, weight security |
| `runs` | Executes training or inference without changing the first three | Schedulers, serving code |
| `decides` | Is a decision or the stated basis for one | Threshold determinations, a system card |

**`verifiability`**: how a wrong output would be found.

| Value | Meaning | Example |
|---|---|---|
| `mechanical` | An automated check that exists today would fail | A unit-tested data loader |
| `empirical` | The error shows in an outcome people watch, within the feedback latency | A training change that hurts loss |
| `judgment` | Only a competent person examining the work can tell | Whether a task measures what it claims |
| `deferred` | It cannot be told until the event the work exists to prevent or predict | An under-elicited dangerous-capability result |

**`feedback_latency`**: how long before an error would normally surface: `minutes`, `hours`, `days`, `weeks`, `months`, `never`.

**`failure_visibility`**: what a wrong output looks like.

| Value | Meaning |
|---|---|
| `loud` | It crashes or errors |
| `quiet` | It gives a plausible wrong result that someone looking would find |
| `silent` | A wrong result looks the same as a right one without independent ground truth |

**`reversibility`**: `cheap` (rerun it), `costly` (retrain, re-evaluate or slip a schedule), `irreversible` (a release, a published claim, lost containment).

**`privilege`**: access the work needs: `none`, `internal_code`, `training_infra`, `eval_infra`, `weights`, `production`, `security`.

**`change_type`**: the pacing model's class for what the task deploys: `training_improvement`, `dataset_update`, `system_software_change`, `monitor_change`, `evaluation_change`, `decision`, or `none` for analysis that deploys nothing. The first four are the readback-ops model's own types. `evaluation_change` and `decision` are added here (spec decision D6).

## 2. Scales

### 2.1 Automation level (AL0 to AL5)

Epoch AI's scale, as Anthropic uses it for its R&D Automation Index.

| Level | Name | Human role |
|---|---|---|
| AL0 | No AI involvement | Does all of it |
| AL1 | Minimal AI involvement | Does nearly all of it |
| AL2 | AI assists | Does the work with AI help |
| AL3 | AI collaborates | Directs closely; AI does large chunks; human may review line by line |
| AL4 | AI leads | Gives a high-level ask, supervises, course-corrects, approves |
| AL5 | AI is autonomous | None required |

Anthropic's worked example (`EV-anthropic-2026-09-measuring-pace-06`) fixes the line between AL3 and AL4: at AL3 the engineer stays in the loop and may review the change line by line; at AL4 the engineer reads the write-up, skims the change and decides whether it ships.

An automation estimate is either one level, or `levels` with the share of the task's work at each level. Use `levels` when a source gives shares or when practice clearly splits.

A level says who did the work. It does not say whether anyone understood it. AL4 with a skim and AL4 with a passed comprehension audit are the same automation level.

### 2.2 Comprehension level (CL0 to CL5)

Reserved. The CL scale is a draft outside this repository. Until its definitions are copied here, record no `comprehension_level` estimate. Record what sources say about understanding as evidence items of kind `comprehension`.

### 2.3 Oversight mode

What human checking a contribution of this task normally gets before it takes effect.

| Value | Meaning |
|---|---|
| `human_every_change` | A person reviews each contribution in substance |
| `human_sampled` | A person reviews a sample; the rest take effect unreviewed by people |
| `ai_review_human_by_exception` | Models review everything; people see what models escalate |
| `ai_review_only` | Models review; no routine route to a person |
| `none` | No review |

A person approving a model's summary without examining the work is `ai_review_human_by_exception`, not `human_every_change`.

### 2.4 Numeric quantities

| Quantity | Unit | Notes |
|---|---|---|
| `labor_share` | share of person-time | Give the denominator, such as "all model R&D person-time" |
| `compute_share` | share of compute | Give the denominator |
| `advance_share` | share of capability progress riding on the task | The pacing model's progress weight. Usually judgment |
| `human_review_coverage` | share of contributions a person reviews in substance | Denominator: contributions of this task |
| `changes_per_researcher_year` | deployed contributions per researcher-year | Per researcher across model R&D, as in the pacing model |
| `hours_to_understand` | researcher-hours to understand one contribution to audit standard | |
| `elasticity_to_ai_labor` | percent growth in the count per percent growth in AI labor | |

A `range` is an 80% interval: `low` is the 10th percentile, `high` the 90th, `central` the median. Use `point` only for a number a source states outright.

## 3. Sources and evidence

### 3.1 Source `type`, in search priority order

| Type | What it is | Best grade |
|---|---|---|
| `incident_report` | A developer's postmortem or incident disclosure | A |
| `risk_report` | A report under a developer's safety framework | A |
| `system_card` | A system card or model card | A |
| `third_party_investigation` | An independent party's assessment of a developer | A |
| `lab_measurement_report` | A developer's published numbers on its own R&D | A |
| `lab_research_post` | A developer's research or engineering post | B |
| `academic_paper` | A paper not covered above | B |
| `standard_or_policy` | A standard, framework or policy text | B |
| `staff_statement` | A named person's interview, talk or post | C |
| `press_report` | Journalism | C |
| `forecast_or_model` | A forecast or model of AI progress | C |
| `readback_internal` | Readback's own analyses and data files | C |
| `open_source_analog` | Evidence from public repositories | D |

Public repositories lag frontier practice. They supply examples and a floor on trends. They do not show what frontier developers do in private.

### 3.2 `vantage`

`first_party` (an organization on itself), `embedded_third_party` (an outside party with internal access, stated in the document), `external_third_party` (an outside party without it), `secondary` (reporting what others said).

### 3.3 `strength`

| Value | Meaning |
|---|---|
| `measured` | A quantity the source measured and reports, with enough method to know what was counted |
| `reported` | Stated as fact about the source's own or the examined organization's work |
| `anecdote` | One person's account |
| `inferred` | Our reading of what the quote implies. Say how in `note` |

### 3.4 `grade`

| Grade | Requires |
|---|---|
| A | `measured`, from a first party or embedded third party, in a source type that allows A |
| B | A specific, documented statement by a first party or embedded third party |
| C | A staff anecdote, press report, forecast, or an external party's analysis |
| D | An analog, or an inference more than one step from the quote |

A self-reported measurement is still A: the grade says how direct the evidence is. Self-interest, redaction and small samples go in the source's `limits` and should lower the confidence of any estimate that leans on it.

### 3.5 Writing an item

- One claim per item. The claim says no more than the quote supports.
- The quote is verbatim, under about 60 words. `[...]` marks an omission.
- Every number in the claim is in the quote.
- `kind` is what the item is evidence of: `automation`, `oversight`, `comprehension`, `incident`, `share`, `practice`, `risk`, `method`, `pace`.
- `describes` is the period the claim is about when that differs from publication.
- A quote from a page that refuses automated fetches carries `unverified_reason` until a person saves the page and the quote is verified.

## 4. Estimates

- `scope` is a developer's name or `frontier`. Do not generalize one developer's number to `frontier` without saying so in `reasoning` and lowering `confidence`.
- `basis: evidence` means the value can be read from the cited items. `mixed` means the items constrain it and judgment fills the rest. `judgment` means nothing cited constrains it.
- `reasoning` says how the value follows from the evidence, in two to four sentences.
- `confidence` is `low` unless a grade A or B item about this task and scope supports the value directly. Judgment is never `high`.
- `stale_after`: six months from `as_of` for automation and oversight; twelve for shares and gate inputs. Automation evidence ages fast.

## 5. Risks

- One risk per failure mode. If two tasks fail the same way for the same reason, list both tasks on one risk.
- `harm_path`: `false_assurance` (people believe something is safe or true that is not), `model_misshaped` (the trained model is worse or different than believed), `containment_weakened`, `oversight_outpaced` (work takes effect faster than it can be checked), `capacity_degraded` (people lose the ability to do or check the work).
- `mechanisms`: how automation raises the risk.

| Mechanism | Meaning |
|---|---|
| `comprehension_gap` | Nobody accountable understands the contribution |
| `review_overload` | More is produced than can be checked |
| `correlated_error` | The model that checks shares the blind spots of the model that produced |
| `adversarial_model` | The model acts to pass the check: gaming, sandbagging, sabotage |
| `accountability_diffusion` | No person owns the outcome |
| `spec_gap` | The request left out what mattered and the model filled it in |
| `skill_atrophy` | People lose the skill to do or check the work |
| `time_pressure` | The schedule sets the depth of checking |

- `review_catchable`: would a reviewer asking this task's question set, and getting honest answers, see the problem? `yes`, `partly`, or `no`. A design review catches what the contributors do not know. It does not catch what a model has hidden from them, or an error in data nobody can read in full. Say which in `review_rationale`.
- `severity`: `critical` (could lead directly to a wrong release or internal-deployment decision for a dangerous model, or to loss of containment), `high` (corrupts a safety-relevant measurement or the model itself), `moderate`, `low`.
- `status`: `observed_frontier` (an incident or evidence item shows it at a frontier developer), `observed_analog`, `hypothesized`.

## 6. Review questions

A question set is an agenda template for a design review or a comprehension audit of one kind of contribution.

- **Altitude.** A question tests understanding of the design. Someone who understands the contribution can answer without the code or transcripts open and without asking a model. Do not ask for names, values or syntax.
- **`category`** follows `quiz-me`: `what` (what it does, traced end to end), `why` (design rationale against real alternatives), `failure` (how it fails and what that looks like), `dependency` (what it relies on), `side_effects` (what else it changed). `provenance` is added here: who or what produced each part, and what a person examined directly (spec decision D5).
- **`topical_area`** follows the comprehension audit paper's Table 4: `architecture_design`, `implementation_behavior`, `process` (deep tier) and `key_findings`, `analysis_of_results` (familiarity tier).
- **`good_answer_shows`** is what the reviewer listens for. **`red_flags`** are answers that indicate a gap, such as "the agent's summary said so".
- **`evidence_to_request`** is a record that should exist if the understanding existed when the work was approved.
- Each question names the risks it is aimed at.

## 7. Incidents

- `frontier` is true when the incident is in a frontier developer's own work.
- `automation_involved`: did a model produce or check the faulty part? `unknown` when the source does not say. Do not infer.
- `comprehension_failure`: `yes` when the source shows the responsible people did not understand the faulty part when it took effect; `partly` when some did or the gap was narrow; `no` when they understood and erred anyway, or the failure was the model's concealment; `unknown` otherwise. Give the reason in `comprehension_note`.
- `backtest`: one entry per question tested. `would_surface` means an honest answer before the incident would have exposed the root cause. `might_surface` means it depends on follow-up. `would_not_surface` means the contributors could have answered well and the incident would still have happened. Record `would_not_surface` verdicts: they mark where review is the wrong control.
