# A simple model of pacing and the takeoff of automated AI R&D

Draft of 2026-11-13. Figures to come. The runnable model is `simple_model.py`: one file, one state variable, numpy only. The two full models and their evidence are in [README.md](README.md).

## The question

AI now does a growing share of AI research. If better AI makes research faster and faster research makes better AI, the pace can compound. Three kinds of policy are proposed to hold it down: comprehension audits, which let a lab deploy only what its people understand; an internal-use lag, which makes a lab work with the AI it had some months ago; and limits on research compute. This model asks what each does to the dates of two milestones:

- **Researcher-level AI:** an all-AI lab has the research judgment of the best human researcher.
- **TED-AI:** an all-AI lab is far past every human expert. The level is AI Futures' definition.

## Five ideas

**1. The loop, with research getting harder.** Progress is measured in years of progress at the rate before October 2025, and pace is years of progress per calendar year. Each year of software progress ahead of the historical schedule halves what a unit of research input buys.

```
software pace = research input / 2 ^ (years of software progress ahead of schedule)
pace          = 2/3 * software pace + 1/3
```

The last third of progress comes from more compute, which AI research does not speed up here.

**2. AI labor helps up to a ceiling.** AI labor per researcher doubles every 0.25 years of progress. Research input rises with its square root and tops out at 15 times, because experiments need compute.

**3. Judgment has no ceiling, and it comes in two kinds.** Research input is multiplied by the lab's research judgment: which experiments to run and what to make of them. AI judgment starts far below people's and improves with progress.

- **Crisp tasks** have clear evaluation criteria. AI judgment on them improves 3 SD of the human researcher distribution per year of progress.
- **Fuzzy tasks** have none, and human judgment on them is systematically flawed, so there is little to train on. AI judgment on them improves 1 SD or 0.5 SD.
- **Crisp work stands in for fuzzy work poorly.** However good the AI gets at crisp tasks, the lab's judgment is at most 4 times its judgment on fuzzy tasks.
- **Some work needs a person.** On real tasks today, 14% need a person however short the task. That share falls as AI judgment on fuzzy tasks rises.

**4. Understanding takes people's time.** Deployed changes grow with AI labor: 1% more labor, 0.4% more changes. The hours a person needs to understand one do not shrink. Understanding everything deployed takes 14% of researchers' time today.

**5. The lab chooses.** Under audits a lab may deploy only what its people understand. It splits researcher time between research and understanding to go fastest, and understands the most valuable changes first.

## The result that needs no simulation

Once AI labor is at its ceiling, the only thing still compounding is judgment. Research halves in productivity for each year ahead of schedule, so judgment must double research input once per year of progress to keep the pace rising. That gives a critical rate:

```
critical rate = ln 2 / (value of one SD of judgment * software share of progress) = 2.3 SD per year of progress
```

- **Above the critical rate the loop runs away.** At 3 SD a year the pace passes 12 times within a year.
- **Below it the pace settles.** It settles at 1.7 times the historical rate when the binding judgment improves 1 SD a year, and 1.3 times at 0.5 SD.
- **The binding judgment is the fuzzy one.** Because crisp work stands in for fuzzy work poorly, the rate on fuzzy tasks sets where the pace settles, however fast crisp judgment improves.

So whether there is an explosion at all turns on how fast AI judgment improves on the tasks that are hardest to supervise. A benchmark of exactly that, Anthropic's TASTE, has frontier models at chance as of July 2026, which fixes the starting level and not yet the rate.

## What pacing does

Dates with no pacing, and the delay each policy adds, from `results/tables_simple.md`:

| | One judgment, +3 SD | Crisp +3, fuzzy +1 SD | Crisp +3, fuzzy +0.5 SD |
|---|---|---|---|
| Researcher-level AI, no pacing | Aug 2027 | Jul 2028 | Nov 2030 |
| TED-AI, no pacing | Nov 2027 | May 2030 | Oct 2037 |
| Central audits delay TED-AI | +3 mo | +11 mo | +16 mo |
| Strict audits delay TED-AI | +5 mo | +15 mo | +20 mo |
| 3-month lag delays TED-AI | +6 mo | +3 mo | +1 mo |
| 9-month lag delays TED-AI | +12 mo | +10 mo | +3 mo |
| 3-fold compute cut delays TED-AI | +4 mo | +6 mo | +6 mo |

- **The rate on fuzzy tasks decides the dates.** Halving it moves TED-AI by seven years. Lowering the crisp rate from 3 to 2.1 SD moves it by three months.
- **Audits work where the takeoff is slow, and lags where it is fast.** An audit bites once deployed changes outgrow people's time, and it keeps biting. A lag sets the lab back a fixed distance, which is worth months in a fast takeoff and weeks in a slow one.
- **Audits barely move researcher-level AI.** They delay it by about a month in each of these cases. The gate starts to bind only about when that level arrives.
- **How fast deployed changes grow with AI labor decides the audit result.** At 0.2% more changes per 1% more labor, central audits delay TED-AI by 2 months in the middle case. At 0.6% they delay it by 22. Nobody has measured this number.
- **Work that needs a person and audits act on the same margin.** Without the 14% of work that needs a person, the middle case reaches researcher-level AI four months sooner, and central audits would delay TED-AI by 27 months, against 11 with it. Where the work itself keeps people in the loop, audits add less.

## How it compares with the full models

The simple model was written to carry four results of the full models. Where it does not, the difference is stated.

| Result of the full models | Simple model |
|---|---|
| A lag delays the milestones by about its own length | Holds where judgment improves fast: 3 and 9 months of lag delay TED-AI by 6 and 12 months. Does not hold where fuzzy judgment is slow: the delay is a third to all of the lag's length, where the full model has it at or above the lag's length |
| Audits barely move the dates when judgment improves fast on every task | Holds roughly: central audits delay TED-AI by 3 months, against a median of 1 in the full model |
| Audits delay TED-AI by a year or more when fuzzy judgment is slow | Holds: 11 to 16 months. The full model's median is 3 to 5 months at +1 SD and 18 to 22 at +0.5 SD |
| The fuzzy rate matters far more than the crisp rate | Holds |
| Work that needs a person changes nothing when judgment is fast and delays the milestones when it is slow | Holds |

Dates differ. With one judgment at +3 SD the simple model has TED-AI in November 2027, and the full model's sampled median is September 2027. In the middle case the simple model has May 2030 and the full model December 2028. The full model draws many parameter sets from AI Futures' distribution and reports the median. The simple model is one set of central values.

## Inputs

| Input | Value | Basis |
|---|---|---|
| Pace on May 1 and Nov 1, 2026 | 1.2 and 1.7 times | METR's November 2026 estimate as AI Futures reads it. The two labor inputs are fitted to these |
| Software share of progress | 2/3 | Greenblatt, via Cotra |
| Labor's exponent in research | 0.5 | Cotra |
| Ceiling on labor's effect | 15 times | AI Futures Model default. 60 in its November example |
| Halvings of research productivity per year ahead | 1 | AI Futures: research inputs grew twofold a year |
| AI judgment on Nov 1, 2026 | -3.5 SD | AI Futures' base case |
| Value of one SD of judgment | 0.445 in logs | AI Futures Model's distribution of research taste: one SD is worth about 1.55 times |
| Rate on crisp tasks | +3 SD | AI Futures' base case |
| Rate on fuzzy tasks | +1 and +0.5 SD | Judgment. No measurement |
| Weight of crisp work | 65% | Three anchors, none a measurement of it. See the full briefing |
| Substitution between crisp and fuzzy work | 0.25 | Judgment |
| Work that needs a person | 14% | OpenAI, tasks under 15 minutes, January to July 2026 |
| A person's time on that work | 4% of doing it | Assumption |
| Time understanding deployed changes today | 14% | Assumption in the full model, from counts and hours per change |
| Growth of deployed changes with AI labor | 0.4 | Assumption. Not measured |
| Pareto index of a change's value | 1.8 | Read from one developer's description of compute multipliers |

The fit puts AI labor per researcher at 12 times on Nov 1, 2026. Anthropic staff self-report 12 times and Cotra estimates about 10.

## What it leaves out

- **Sampling.** One set of central values. The full model samples AI Futures' distribution.
- **The link from comprehension to judgment.** In the full model people apply judgment only to changes they understand. It moves dates by days to weeks there.
- **Sign-off without a comprehension standard.** It does little in the full model.
- **Training compute after a cut.** A compute cut here lowers experiment compute once and leaves the compute third of progress alone.
- **Safety research.** The model has one clock, for capabilities. The source of the fuzzy definition argues that safety research is fuzzier than capabilities research, which would make it the slower of two clocks.

## Run it

```bash
pip install numpy
```

```bash
python simple_model.py
```

```bash
python -m pytest test_simple_model.py
```
