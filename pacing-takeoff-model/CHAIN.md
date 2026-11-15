# The chain model: from small experiments to real value

Draft of 2026-11-15, revised the same day. A standalone model in one file, `chain_model.py`, with numpy and the standard library. It shares no code with the two full models or the simple model in this directory. Their write-ups are [README.md](README.md) and [SIMPLE.md](SIMPLE.md). Every number in the tables below is from `results/tables_chain.md`, which the script writes.

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

Three kinds of AI judgment improve at their own rates, in SD of researcher judgment:

| Kind | What it does | Rate |
|---|---|---|
| Ideas | Proposes candidates on a well-defined problem. No ceiling | +3 SD per year of progress |
| Transfer | Judges which small-scale gains hold at scale | +3, +1 or +0.5 SD |
| Metrics | Defines the next metric and debugs results that game the current one | +3, +1 or +0.5 SD |

Transfer and metric judgment can come with progress, as all judgment does in the AI Futures Model, or with calendar time, as outcomes at scale come in. Nothing measures which holds, and it moves the results more than any other input, so every table is given both ways.

## What it reduces to

With the AI's two links set to people's values and no gain from selection, research is the AI Futures rule exactly: experiments times the average value of candidates when each researcher uses the better of their own judgment and the AI's. A test checks this. An experiment left to the AI of November 2026 is worth 21% of one a person judged, which is the value the AI Futures taste distribution gives judgment at -3.5 SD.

## Calibration

Three inputs are fitted to three measurements.

| Measurement | Value | Source | Input fitted | Fitted value |
|---|---|---|---|---|
| Pace on May 1, 2026 | 1.2 times | AI Futures' estimate | Years of progress per doubling of AI labor | 0.19 |
| Pace on Nov 1, 2026 | 1.7 times | AI Futures' reading of METR's report | Growth of judging time with candidates | 0.005 |
| AI labor per researcher on Nov 1, 2026 | 13 agent workdays per researcher workday | OpenAI's trend | AI labor on Oct 1, 2025 | 0.10 |

- **People's time is already short.** In the fitted model researchers judge 70% of experiments at scale on Nov 1, 2026 and 51% on Jan 1, 2027.
- **The fit gives no weight to volume.** The pace of 2026 is matched with judging time per experiment that does not rise as the candidates behind it multiply. People's time runs short because there are more experiments at scale.

## Results with no pacing

Researcher-level AI and TED-AI are the dates an AI-only lab's research matches a lab of researchers at AI Futures' two levels, +3.09 and +7.72 SD. The last column is when the AI's weakest kind of judgment passes the best researcher's.

Transfer and metric judgment come with progress:

| AI judgment gained per year | Researcher-level AI | TED-AI | AI passes the best researcher on every kind of judgment |
|---|---|---|---|
| Ideas, transfer and metrics all +3 SD | Jun 2027 | Jun 2027 | Jun 2027 |
| Ideas and transfer +3, metrics +1 | Oct 2027 | Nov 2027 | Nov 2027 |
| Ideas and transfer +3, metrics +0.5 | Mar 2028 | Jun 2028 | Jul 2028 |
| Ideas +3, transfer and metrics +1 | Feb 2028 | Mar 2028 | Mar 2028 |
| Ideas +3, transfer +1, metrics +0.5 | Aug 2028 | Nov 2028 | Nov 2028 |
| Ideas +3, transfer and metrics +0.5 | Mar 2029 | Jul 2029 | Aug 2029 |

Transfer and metric judgment come with calendar time:

| AI judgment gained per year | Researcher-level AI | TED-AI | AI passes the best researcher on every kind of judgment |
|---|---|---|---|
| Ideas, transfer and metrics all +3 SD | Nov 2027 | Dec 2027 | Jan 2029 |
| Ideas and transfer +3, metrics +1 | Aug 2028 | Feb 2029 | Jun 2033 |
| Ideas and transfer +3, metrics +0.5 | Jun 2029 | Jul 2030 | Jan 2040 |
| Ideas +3, transfer and metrics +1 | Mar 2029 | Sep 2029 | Jun 2033 |
| Ideas +3, transfer +1, metrics +0.5 | Feb 2030 | Nov 2030 | Jan 2040 |
| Ideas +3, transfer and metrics +0.5 | Nov 2030 | Nov 2031 | Jan 2040 |

- **If slow judgment comes with progress there is no long plateau.** TED-AI arrives between June 2027 and July 2029. The pace holds at about 2 to 3 times for one to two years in the slower cases, and at that pace the AI gains its 3.5 SD of transfer and metric judgment quickly.
- **If it comes with calendar time the pace holds between 1.4 and 2.7 times for two to four years.** With transfer at +1 SD and metrics at +0.5 SD the pace is 2.1 times in January 2028, 1.5 in January 2029 and 1.8 in January 2030.
- **In that case TED-AI is reached on ideas alone.** An AI-only lab matches the +7.72 SD level in November 2030 with its metric judgment still below the median researcher's. Its ideas are then about 20 SD above the median researcher's and it keeps 37% of their gain. The AI passes the best researcher on every kind of judgment in 2033 with metrics at +1 SD and in 2040 at +0.5 SD.
- **Ideas have no ceiling here, and the last result depends on that.** If gains on well-defined problems run into diminishing returns, the date to trust is the last column.
- **A weak link costs a share of the slope and sets no ceiling.** An AI that keeps 10% of a gain turns ideas improving 3 SD a year into 0.3 SD a year of real judgment. The loop runs away once the AI keeps 78% of what people keep.
- **Work nobody judged is not what drives the pace.** People judge 17% of experiments in January 2028, and those carry 73% of the real research, because people can vouch for AI ideas up to their best researcher's level. A cap that tied unjudged work to judged work was tested and never bound, so it is not in the model.
- **Measured progress runs ahead of real progress.** With transfer at +1 SD and metrics at +0.5 SD, the pace on the lab's metrics in January 2028 is 4.0 times against a real 2.2 if judgment comes with progress, and 2.8 against 2.1 if it comes with calendar time.

## What pacing does

Delay to TED-AI, transfer and metric judgment coming with progress:

| AI judgment gained per year | Central audits | Strict audits | 9-month lag | 3-fold compute cut |
|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD | +0 mo | +1 mo | +11 mo | +1 mo |
| Ideas and transfer +3, metrics +1 | +4 mo | +6 mo | +11 mo | +1 mo |
| Ideas and transfer +3, metrics +0.5 | +16 mo | +19 mo | +12 mo | +1 mo |
| Ideas +3, transfer and metrics +1 | +6 mo | +8 mo | +10 mo | +2 mo |
| Ideas +3, transfer +1, metrics +0.5 | +16 mo | +19 mo | +12 mo | +2 mo |
| Ideas +3, transfer and metrics +0.5 | +23 mo | +26 mo | +10 mo | +2 mo |

Coming with calendar time:

| AI judgment gained per year | Central audits | Strict audits | 9-month lag | 3-fold compute cut |
|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD | +1 mo | +1 mo | +7 mo | +0 mo |
| Ideas and transfer +3, metrics +1 | +5 mo | +5 mo | +4 mo | +0 mo |
| Ideas and transfer +3, metrics +0.5 | +10 mo | +11 mo | +3 mo | +0 mo |
| Ideas +3, transfer and metrics +1 | +3 mo | +4 mo | +3 mo | +0 mo |
| Ideas +3, transfer +1, metrics +0.5 | +7 mo | +8 mo | +3 mo | +0 mo |
| Ideas +3, transfer and metrics +0.5 | +7 mo | +8 mo | +2 mo | +0 mo |

- **Audits delay more than in the earlier models, and more the slower the AI's metric judgment.** Audit hours come out of time that is already short, so each hour means experiments left to the AI.
- **With metrics at +0.5 SD audits pass a 9-month lag under either reading.** They delay TED-AI by 16 to 23 months against the lag's 10 to 12 if judgment comes with progress, and by 7 to 10 months against 2 to 3 if it comes with calendar time.
- **A lag does little if slow judgment comes with calendar time.** The lag holds back the AI a lab may use, and the judgment the lab is waiting for arrives on the calendar either way.
- **The audit result rests on one assumption.** If deployed changes do not grow with AI labor, central audits delay TED-AI by nothing. The model takes the briefing's value of 0.4% more changes for each 1% more labor, which is an assumption.
- **Half of audit time is taken to count as judging.** With judgment coming with progress, the central delay in the fifth case is 19 months at none of it and 12 at all of it.

## Each input moved

Case: ideas +3, transfer +1, metrics +0.5. `results/tables_chain.md` has 18 rows for each reading.

- **Judgment with progress.** TED-AI is November 2028 in the central row and runs from April 2028 to May 2029. Earliest: validity of 0.3 with the AI judging today, and people able to vouch for any gain (both April 2028). Latest: judging time that grows with candidates (May 2029) and ideas at +2.1 SD (April 2029).
- **Judgment with calendar time.** TED-AI is November 2030 in the central row and within three months of that in 13 of the 18 rows. Earliest: people able to vouch for any gain (September 2028). Latest: validity of 0.01 with the AI judging today (August 2031).
- **What the AI keeps today moves the date by about a year.** Validity with the AI judging runs from 0.3 to 0.01, against 0.05 in the central case. TED-AI moves from April 2028 to March 2029 with progress, and from September 2029 to August 2031 with calendar time.
- **The limit on what people can vouch for matters most where slow judgment comes with calendar time.** Without it, people-judged experiments carry the AI's ideas at full value and TED-AI comes in September 2028.

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
| Transfer: people, AI today, ceiling | 0.7, 0.2, 0.9 | Judgment. Only the ratios enter. AI today tested at 0.4 |
| Validity: people, AI today, ceiling | 0.8, 0.05, 0.95 | The PI's judgment of 2026-11-15 that the first draft's 0.3 was too high. Tested at 0.3 and 0.01 |
| Shape of a link between the AI today and people's level | The same ratio for each SD | As research value is in the AI Futures Model |
| People can vouch for gains up to | +3.09 SD ideas | Judgment: the best researcher. Tested at +1 SD and with no limit |
| Researcher time on results, metrics and plans, Oct 2025 | 40% | Judgment. One of Epoch's eight interviewees said "60% of my time would be automated". Tested at 60% |
| Time to understand all deployed changes today | 14% | The briefing's gate |
| Growth of deployed changes with AI labor | 0.4 | The briefing's assumption. Tested at 0 |
| Share of audit time that counts as judging | 50% | Judgment. Tested at 0 and 100% |

## What it leaves out

- **Sampling.** One set of central values.
- **Any ceiling on ideas.** AI judgment on well-defined problems rises without limit, as in the AI Futures Model. A ceiling would move every output-based date above.
- **Separate streams of research.** Pretraining and post-training are one stream. A model in which gains on a fixed metric run out and progress waits for the next valid target would need two.
- **Validity that falls under pressure.** Selecting harder on a metric does not lower its validity here. The AI's metric judgment is the only thing that sets validity on unjudged work.
- **A lab that cannot see validity.** The lab is taken to know what its gains are really worth.
- **Sign-off without a comprehension standard.**

## Reproduce

```
python chain_model.py > results/tables_chain.md
pytest test_chain_model.py
```

`calibrate()` refits the three fitted inputs. It takes about two minutes.
