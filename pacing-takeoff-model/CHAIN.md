# The chain model: from small experiments to real value

Draft of 2026-11-15. A standalone model in one file, `chain_model.py`, with numpy and the standard library. It shares no code with the two full models or the simple model in this directory. Their write-ups are [README.md](README.md) and [SIMPLE.md](SIMPLE.md). Every number in the tables below is from `results/tables_chain.md`, which the script writes.

## What it is for

The earlier models split research judgment into two classes and joined them with a weight and a substitution parameter that nobody could measure or explain. This model replaces both with a mechanism. It keeps the parts of the AI Futures Model that are widely understood: compute-limited experiments, AI labor with diminishing returns, judgment measured in SD of the researcher distribution, and research that gets harder as it goes.

## The chain

Experiments at scale are limited by compute. Behind each one the lab runs many small experiments and backs the candidate that looks best. Two links separate how good a candidate looks from what it is worth.

```
small-scale result  ->  result on the metric at scale  ->  real value
                 transfer                            validity
```

- **Transfer** is the share of a small-scale gain that holds at scale. It depends on who judged which candidate would transfer.
- **Validity** is the share of a gain on the metric that is real. It depends on who defined the metric and checked the result for gaming.
- **A person who judges an experiment supplies both links.** Researchers judge as many experiments as they have time for. The AI judges the rest with its own transfer and metric judgment.
- **People can vouch only for gains within their range.** Their judgment applies up to what their best researcher could have proposed. The AI judges any gain beyond that.

The links multiply in the exponent of an experiment's value:

```
value = exp(kept * (standing + gain) - standing)
kept  = transfer * validity, each against people's
```

`gain` is what has been added at small scale since October 2025: better ideas from the AI, and the best of more candidates. `standing` is what an experiment was already worth.

Three kinds of AI judgment improve at their own rates, all in SD of researcher judgment per year of progress:

| Kind | What it does | Rate |
|---|---|---|
| Ideas | Proposes candidates on a well-defined problem. No ceiling | +3 SD |
| Transfer | Judges which small-scale gains hold at scale | +3, +1 or +0.5 SD |
| Metrics | Defines the next metric and debugs results that game the current one | +3, +1 or +0.5 SD |

## What it reduces to

With the AI's two links set to people's values and no gain from selection, research is the AI Futures rule exactly: experiments times the average value of candidates when each researcher uses the better of their own judgment and the AI's. A test checks this. An experiment left to the AI of November 2026 is worth 21% of one a person judged, which is the value the AI Futures taste distribution gives judgment at -3.5 SD.

## Calibration

Three inputs are fitted to three measurements.

| Measurement | Value | Source | Input fitted | Fitted value |
|---|---|---|---|---|
| Pace on May 1, 2026 | 1.2 times | AI Futures' estimate | Years of progress per doubling of AI labor | 0.19 |
| Pace on Nov 1, 2026 | 1.7 times | AI Futures' reading of METR's report | Growth of judging time with candidates | 0.006 |
| AI labor per researcher on Nov 1, 2026 | 13 agent workdays per researcher workday | OpenAI's trend | AI labor on Oct 1, 2025 | 0.10 |

- **People's time is already short.** In the fitted model researchers judge 70% of experiments at scale on Nov 1, 2026 and 51% on Jan 1, 2027.
- **The fit gives no weight to volume.** The pace of 2026 is matched with judging time per experiment that does not rise as the candidates behind it multiply. People's time runs short because there are more experiments at scale.

## Results with no pacing

| AI judgment gained per year of progress | Researcher-level AI | TED-AI | AI passes the best researcher on every kind of judgment |
|---|---|---|---|
| Ideas, transfer and metrics all +3 SD | May 2027 | Jun 2027 | May 2027 |
| Ideas and transfer +3, metrics +1 | Jul 2027 | Aug 2027 | Aug 2027 |
| Ideas and transfer +3, metrics +0.5 | Aug 2027 | Oct 2027 | Nov 2027 |
| Ideas +3, transfer and metrics +1 | Nov 2027 | Dec 2027 | Dec 2027 |
| Ideas +3, transfer +1, metrics +0.5 | Jan 2028 | Mar 2028 | Mar 2028 |
| Ideas +3, transfer and metrics +0.5 | Apr 2028 | Aug 2028 | Sep 2028 |

Researcher-level AI and TED-AI are the dates an AI-only lab's research matches a lab of researchers at AI Futures' two levels, +3.09 and +7.72 SD.

- **The model does not produce a long plateau.** It was built to test whether people's judging time holds the pace down until the AI's transfer and metric judgment arrive. At these inputs TED-AI comes between June 2027 and August 2028 in all six cases. The earlier simple model put it in 2034 with slow judgment at +0.5 SD.
- **A weak link costs a share of the slope and sets no ceiling.** An AI that keeps 25% of a gain turns ideas improving 3 SD a year into 0.75 SD a year of real judgment. The loop runs away once the AI keeps 78% of what people keep.
- **Experiments nobody judged are still worth something, and there are many of them.** With transfer at +1 SD and metrics at +0.5 SD, the lab runs 15 times the experiments in January 2028 and people judge 16% of them. The pace is 4.4 times.
- **A faster pace brings the slow judgment sooner.** The rates are per year of progress, as in the AI Futures Model. At a pace of 2 to 4 the AI gains 3.5 SD of transfer judgment in a little over a year.
- **Measured progress runs ahead of real progress.** In the same case the pace on the lab's metrics in January 2028 is 6.7 times against a real 4.4.
- **Tying slow judgment to calendar time changes the picture.** If transfer and metric judgment improve only as outcomes come in, an AI-only lab matches the +7.72 SD level in May 2029 on the strength of its ideas, and the AI passes the best researcher on every kind of judgment in January 2040. Nothing measures which holds.

## What pacing does

Delay to TED-AI:

| AI judgment gained per year of progress | Central audits | Strict audits | 9-month lag | 3-fold compute cut |
|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD | +0 mo | +1 mo | +11 mo | +2 mo |
| Ideas and transfer +3, metrics +1 | +1 mo | +3 mo | +12 mo | +2 mo |
| Ideas and transfer +3, metrics +0.5 | +4 mo | +6 mo | +13 mo | +2 mo |
| Ideas +3, transfer and metrics +1 | +4 mo | +6 mo | +11 mo | +2 mo |
| Ideas +3, transfer +1, metrics +0.5 | +7 mo | +10 mo | +12 mo | +2 mo |
| Ideas +3, transfer and metrics +0.5 | +14 mo | +17 mo | +12 mo | +2 mo |

- **Audits delay more than in the earlier models, and more the slower the AI's own judgment.** Audit hours come out of time that is already short, so each hour means experiments left to the AI.
- **Audits pass a 9-month lag only in the slowest case.**
- **The audit result rests on one assumption.** If deployed changes do not grow with AI labor, central audits delay TED-AI by nothing. The model takes the briefing's value of 0.4% more changes for each 1% more labor, which is an assumption.
- **Half of audit time is taken to count as judging.** At none of it the central delay in the fifth case is 9 months, and at all of it 5.

## Each input moved

Case: ideas +3, transfer +1, metrics +0.5. The central row has TED-AI in March 2028. Across the 19 rows in `results/tables_chain.md` it runs from November 2027 to May 2029.

- **Latest:** transfer and metric judgment that come with calendar time (May 2029), ideas at +2.1 SD (August 2028), an experiment ceiling of 5 times (June 2028).
- **Earliest:** an experiment ceiling of 60 times (November 2027), selection worth twice as much (December 2027).
- **What the AI keeps today matters little.** From 2% to 36% of a gain, TED-AI moves from May 2028 to January 2028. The link is taken to reach people's value when the AI's judgment reaches the median researcher, so a lower start means a steeper climb.

## Inputs

| Input | Value | Basis |
|---|---|---|
| Software share of progress | 2/3 | As in the simple model |
| Research halves in productivity per year ahead of schedule | 1 | As in the simple model |
| Experiments from AI labor | Square root, ceiling of 15 times | As in the simple model. Tested at 5 and 60 |
| Small experiments behind each one at scale, Oct 2025 | 20 | The briefing's one experiment in twenty that ends in a deployed change, which rests on interview quotes |
| Most candidates small-scale compute allows | 10,000 | Judgment. Tested at a million |
| Value of one SD of small-scale result | 0.3 log units | Judgment. Tested at 0.6 |
| Value of one SD of researcher judgment | 0.445 log units | AI Futures' gap between the median and the top researcher |
| AI judgment on Nov 1, 2026 | -3.5 SD, all three kinds | AI Futures' base case |
| Transfer: people, AI today, ceiling | 0.7, 0.2, 0.9 | Judgment. Only the ratios enter |
| Validity: people, AI today, ceiling | 0.8, 0.3, 0.95 | Judgment. Only the ratios enter |
| People can vouch for gains up to | +3.09 SD ideas | Judgment: the best researcher. Tested at +1 SD and with no limit |
| Researcher time on results, metrics and plans, Oct 2025 | 40% | Judgment. One of Epoch's eight interviewees said "60% of my time would be automated". Tested at 60% |
| Time to understand all deployed changes today | 14% | The briefing's gate |
| Growth of deployed changes with AI labor | 0.4 | The briefing's assumption. Tested at 0 |
| Share of audit time that counts as judging | 50% | Judgment. Tested at 0 and 100% |

## What it leaves out

- **Sampling.** One set of central values.
- **Any ceiling on ideas.** AI judgment on well-defined problems rises without limit, as in the AI Futures Model. A ceiling would change every date above.
- **Validity that falls under pressure.** Selecting harder on a metric does not lower its validity here. The AI's metric judgment is the only thing that sets validity on unjudged work.
- **A lab that cannot see validity.** The lab is taken to know what its gains are really worth.
- **Sign-off without a comprehension standard.**

## Reproduce

```
python chain_model.py > results/tables_chain.md
pytest test_chain_model.py
```

`calibrate()` refits the three fitted inputs. It takes about two minutes.
