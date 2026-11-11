# Glossary

Terms with one meaning in this repository. Use them exactly, in records, code, issues and reports. Scales and categories are defined in `docs/codebook.md`.

## The three quantities

**Automation**:
Who produced the work. Measured on Epoch's automation levels, AL0 to AL5.
_Avoid_: AI usage, AI involvement (as a level)

**Oversight**:
Observable human behavior that checks, questions, corrects, constrains or verifies the work. Same meaning as in `comprehension-analysis`. Oversight can happen without comprehension.
_Avoid_: Supervision, review (on its own)

**Comprehension**:
Whether the accountable people can explain a contribution, unaided, to the standard of a comprehension audit. The human side. Reported on the comprehension levels CL0 to CL5 once that scale is fixed.
_Avoid_: Understanding (in records), awareness

**Comprehensibility**:
Whether an output can be understood at all, by a competent person, in the time available. The artifact side. Not estimated here.

## Tasks

**Task**:
A kind of work done in frontier AI development, as a node in the task tree.
_Avoid_: Activity, workstream

**Branch**:
A level-1 task and everything under it. One file in `data/tasks/`.

**Leaf task**:
A task with no children. Leaves carry attributes, estimates, risks and question sets.

**Contribution**:
A meaningful unit of R&D work for which a person or team is accountable and which changes the organization's products or beliefs: a completed experiment and its conclusions, a change to a training recipe, a new dataset, an evaluation and its result. Defined by purpose and effect, as in the comprehension audit paper. It is what a review question is asked about.
_Avoid_: Change (alone), PR, artifact

**Change type**:
The class of deployed change a task produces, as the pacing model counts them. Progress types: training improvement, dataset update, system software change. Required-overhead types: monitor change, evaluation change, control change, decision.

**Deployed change**:
A contribution that reaches a production artifact: a training run, a dataset, a platform, an evaluation used for a decision, a monitor or control, or a decision. The unit the pacing model's gate counts.
_Avoid_: PR, commit, experiment

**Output role**:
What a task's output does to the model or the organization: shapes it, measures it, contains it, runs it, or decides about it.

**Frontier**:
The few developers training the most capable models. Scope `frontier` on an estimate means those developers taken together.

**Analog**:
Evidence about work outside the frontier developers' private practice, such as public repositories. Used for examples; never graded above D.

## Evidence

**Source**:
One published document. One file in `data/sources/`.

**Snapshot**:
The text of a source as fetched on a given day, stored outside git. Its hash is in the source's lock file.

**Evidence item**:
One claim a source makes, with the verbatim quote that makes it.
_Avoid_: Finding, datapoint, citation

**Quote**:
Words copied from a snapshot. `[...]` marks an omission.

**Verified quote**:
A quote the tool found in the current snapshot and stamped in the lock file. Editing the quote or refreshing the snapshot voids the stamp.

**Grade**:
How much weight an evidence item can bear, A to D. Set by who is speaking, about what, and whether they measured it.

**Lock file**:
The machine-written record in `data/locks/` of a source's snapshot hash and its verified quotes.

## Analysis

**Estimate**:
Our reading of one quantity for one task, at one time, for one scope. Carries its basis and the evidence it cites.

**Basis**:
What an estimate rests on: `evidence`, `mixed`, or `judgment`.

**Judgment**:
An estimate with no evidence behind it. A prior. Counted and shown as such in every report.
_Avoid_: Assumption (in records), guess

**Risk**:
A way a task's output can be wrong or harmful, with the mechanism by which automation makes it more likely or harder to see.

**Mechanism**:
How automation raises a risk: comprehension gap, review overload, correlated error, adversarial model, accountability diffusion, specification gap, skill atrophy, time pressure.

**Harm path**:
What the failure does: false assurance, a misshaped model, weakened containment, oversight outpaced, degraded human capacity.

**Review-catchable**:
Whether a design review that asks the question set would expose the risk. `no` marks the risks that need a different control.

**Incident**:
A documented case of something going wrong. One file in `data/incidents/`.

**Question set**:
The questions a reviewer brings to a contribution of one task's kind.

**Backtest**:
A judgment, per incident and question, of whether a good-faith answer would have surfaced the incident's root cause beforehand.

**Intervention**:
A rule or tool that changes how much human time a contribution needs or how much automation is allowed.

**Gate inputs**:
The numbers the pacing model's gate needs for each change type: count per researcher-year, hours to understand one, growth with AI labor, share of progress.

**Judgment prior**:
An estimate with no evidence behind it, recorded so the pacing model can run and its inputs can be ranked. Pooled from two independent elicitations.
_Avoid_: guess, assumption (for a recorded prior)

**Pooled estimate**:
The spread of Anthropic's, OpenAI's and Google DeepMind's own estimates of one quantity for one task. Exists only when all three do.
_Avoid_: frontier average, industry figure

**Data date**:
The latest day any quote was verified. The date printed on generated reports.

## Roles

**Researcher**:
The agent or person who finds sources and writes evidence items.

**Verifier**:
The agent or person who checks evidence items against the snapshot without seeing the researcher's reasoning.
_Avoid_: Reviewer (for this role), judge

**PI**:
The principal investigator. Decides scope and method.
