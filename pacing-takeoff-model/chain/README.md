# The chain model: from small experiments to real value

Draft of 2026-11-16, from Readback Labs. This folder is self-contained: one model file, its checks, its results and this write-up. It needs Python with numpy. Every number in the tables below is from `results/tables.md`, which the script writes.

## The question

AI now does a growing share of AI research. If better AI makes research faster and faster research makes better AI, the pace can compound. This model asks when that happens and what three pacing policies do to the date.

It is built for one disagreement. One side holds that AI research is mostly hill-climbing on measurable targets, so AI will soon do it all. The other holds that the hard part is deciding what to climb: defining a metric that means what you want, noticing when a result games it, and telling which small-scale results will hold at scale. The model gives each of those its own place, so that the disagreement becomes a question about a few inputs.

Terms used below:

- **Progress** is measured in years of AI progress at the rate before October 2025. **Pace** is years of progress per calendar year.
- **SD** is a standard deviation of research judgment across a lab's researchers. The best researcher is at +3.09 SD.
- **Researcher-level AI** is the date an AI-only lab's research matches a lab made up of its best researchers. **TED-AI** is the date it matches the level the AI Futures Project uses for top-expert-dominating AI, +7.72 SD. "Where the two levels come from" below gives their source.
- **Comprehension audits** let a lab deploy only the changes its own people understand. An **internal-use lag** makes a lab work with the AI it had some months ago. A **compute limit** holds a lab to a share of the compute it would otherwise use for research and for training.

## The chain

Experiments at scale are limited by compute. Behind each one the lab runs many small experiments and backs the candidate that looks best. Two links separate how good a candidate looks from what it is worth.

```
small-scale result  ->  result on the metric at scale  ->  real value
                 transfer                            validity
```

1. **Throughput.** AI labor raises the number of experiments a lab gets from its compute, with diminishing returns and a ceiling.
2. **Candidates.** AI labor multiplies the small experiments behind each experiment at scale. The best of n candidates is about sqrt(2 ln n) SD better than a typical one, so volume helps less and less. AI also proposes better candidates as its judgment on well-defined problems improves.
3. **Transfer** is the share of a small-scale gain that holds at scale. It depends on who judged which candidate would transfer.
4. **Validity** is the share of a gain on the metric that is real. It depends on who defined the metric and checked the result for gaming.
5. **People's time.** A person who judges an experiment supplies both links. Researchers judge as many experiments as they have time for, and the AI judges the rest with its own transfer and metric judgment. AI takes over implementation, which frees researcher time. More experiments use it up.
6. **What people can vouch for.** People's judgment applies to gains up to what their best researcher could have proposed. The AI judges any gain beyond that.
7. **The loop.** Real research makes software progress, and progress makes better AI.
8. **Difficulty.** Research gets harder as software advances: each year of software progress halves what a unit of research buys. A lab's other inputs, compute and people, have grown fast enough to offset that, which is what a pace of 1 means. Whether the loop runs away or peters out turns on whether the AI's judgment adds research faster than difficulty takes it away.

The links multiply in the exponent of an experiment's value:

```
value = exp(kept * (standing + gain) - standing)
kept  = transfer * validity, each against people's
```

`gain` is what has been added at small scale since October 2025: better ideas from the AI, and the best of more candidates. `standing` is what an experiment was already worth. An experiment people judged keeps all of its gain. One left to an AI with weak transfer and metric judgment keeps part.

Three kinds of AI judgment improve at their own rates, in SD per year of progress:

| Kind | What it does | Rate |
|---|---|---|
| Ideas | Proposes candidates on a well-defined problem. No ceiling | +3 SD |
| Transfer | Judges which small-scale gains hold at scale | +3, +1 or +0.5 SD |
| Metrics | Defines the next metric and debugs results that game the current one | +3, +1 or +0.5 SD |

All three start at -3.5 SD on November 1, 2026 and improve with progress, so a lab that goes faster gets better judgment sooner.

## What it builds on

The outer structure is the AI Futures Project's model: experiments limited by compute, AI labor with diminishing returns, judgment in SD of the researcher distribution, and research that gets harder. With the AI's two links set to people's values and no gain from selection, research here is the AI Futures rule exactly: experiments times the average value of candidates when each researcher uses the better of their own judgment and the AI's. A check confirms this.

An experiment left to the AI of November 2026 is worth 21% of one a person judged. That is the value the AI Futures taste distribution gives judgment at -3.5 SD, and `standing` is set to match it.

## Calibration

Three inputs are fitted to three measurements.

| Measurement | Value | Source | Input fitted | Fitted value |
|---|---|---|---|---|
| Pace on May 1, 2026 | 1.2 times | The AI Futures Project's estimate in its update of November 10, 2026 | Years of progress per doubling of AI labor | 0.19 |
| Pace on Nov 1, 2026 | 1.7 times | The same update's reading of METR's assessment of November 5, 2026, which put the pace at about 2 times with a range of 1.3 to 3 and attributed 80% of the rise to AI | Growth of judging time with candidates | 0.005 |
| AI labor per researcher on Nov 1, 2026 | 13 agent workdays per researcher workday | OpenAI reported 3.15 in mid-August 2026, doubling every 39 days. 13 is that trend continued | AI labor on Oct 1, 2025 | 0.10 |

- **People's time is already short.** In the fitted model researchers judge 70% of experiments at scale on November 1, 2026 and 51% on January 1, 2027.
- **The fit gives no weight to volume.** The pace of 2026 is matched with judging time per experiment that does not rise as the candidates behind it multiply. People's time runs short because there are more experiments at scale.

## Results with no pacing

| AI judgment gained per year of progress | Researcher-level AI | TED-AI | Pace in Jan 2028 | Pace as measured |
|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD | Jun 2027 | Jun 2027 | over | over |
| Ideas and transfer +3, metrics +1 | Oct 2027 | Nov 2027 | over | over |
| Ideas and transfer +3, metrics +0.5 | Mar 2028 | Jun 2028 | 3.3x | 7.1x |
| Ideas +3, transfer and metrics +1 | Feb 2028 | Mar 2028 | 3.1x | 4.5x |
| Ideas +3, transfer +1, metrics +0.5 | Aug 2028 | Nov 2028 | 2.2x | 4.0x |
| Ideas +3, transfer and metrics +0.5 | Mar 2029 | Jul 2029 | 2.1x | 2.9x |

`over` means TED-AI had arrived by then.

- **Slow transfer and metric judgment delay the takeoff by one to two years.** TED-AI arrives in June 2027 if all three kinds of judgment improve 3 SD a year, and between March 2028 and July 2029 if transfer and metric judgment improve 1 or 0.5 SD a year.
- **They do not prevent it.** In the slower cases the pace holds at about 2 to 3 times for one to two years. At that pace the AI gains the 3.5 SD of transfer and metric judgment it needs to match the median researcher, and the loop then runs away.
- **A weak link costs a share of the slope and sets no ceiling.** An AI that keeps 10% of a gain turns ideas improving 3 SD a year into 0.3 SD a year of real judgment. The loop runs away once the AI keeps 78% of what people keep.
- **People's judgment carries the pace before the takeoff.** With transfer at +1 SD and metrics at +0.5 SD, researchers judge 17% of experiments in January 2028 and those carry 73% of the real research. People can vouch for the AI's ideas up to their best researcher's level, and the AI keeps 11% of a gain on its own.
- **Measured progress runs ahead of real progress.** In the same case the pace on the lab's metrics is 4.0 times in January 2028 against a real 2.2, and 6.4 against 2.4 in July 2028.

The path in that case:

| Date | Pace | Pace as measured | Experiments at scale | Share of experiments people judge | Share of a gain the AI keeps | AI ideas | AI transfer judgment | AI metric judgment |
|---|---|---|---|---|---|---|---|---|
| Jan 2027 | 1.8x | 1.9x | 4.5x | 51% | 2% | -2.6 SD | -3.2 SD | -3.4 SD |
| Jul 2027 | 2.1x | 2.5x | 10.7x | 23% | 5% | +0.3 SD | -2.2 SD | -2.9 SD |
| Jan 2028 | 2.2x | 4.0x | 14.5x | 17% | 11% | +3.9 SD | -1.0 SD | -2.3 SD |
| Jul 2028 | 2.4x | 6.4x | 15.2x | 16% | 26% | +7.1 SD | +0.0 SD | -1.7 SD |

## What pacing does

Delay to TED-AI. Pacing starts January 1, 2027.

| AI judgment gained per year of progress | Central audits | Strict audits | 9-month lag | Compute at a third of baseline |
|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD | +0 mo | +1 mo | +11 mo | +5 mo |
| Ideas and transfer +3, metrics +1 | +4 mo | +6 mo | +11 mo | +5 mo |
| Ideas and transfer +3, metrics +0.5 | +16 mo | +19 mo | +12 mo | +5 mo |
| Ideas +3, transfer and metrics +1 | +6 mo | +8 mo | +10 mo | +6 mo |
| Ideas +3, transfer +1, metrics +0.5 | +16 mo | +19 mo | +12 mo | +6 mo |
| Ideas +3, transfer and metrics +0.5 | +23 mo | +26 mo | +10 mo | +6 mo |

Central audits take the hours to understand every deployed change that researchers are assumed to spend today, 14% of their time. Strict audits take twice the hours. The compute limit holds a lab to a third of the compute it would otherwise use for experiments at scale, for small experiments, for running AI labor and for training the next model.

- **Audits delay TED-AI more the slower the AI's metric judgment.** Central audits delay it by nothing where all judgment improves 3 SD a year, by 4 to 6 months with metrics at +1 SD and by 16 to 23 months at +0.5 SD.
- **The reason is people's time.** Audit hours come out of time that is already short, so each hour means experiments left to the AI. That costs most where the AI's own judgment is weak for longest.
- **With metrics at +0.5 SD audits pass a 9-month lag.** The lag delays TED-AI by 10 to 12 months in every case.
- **The audit result rests on one assumption.** If deployed changes do not grow with AI labor, central audits delay TED-AI by nothing. The model assumes 0.4% more changes for each 1% more labor.
- **Half of audit time is taken to count as judging.** At none of it the central delay in the fifth case is 19 months, and at all of it 12.
- **A compute limit at a third of baseline is a one-time setback of 5 to 6 months.** Training waits about a year for its allowance to catch up with what it has already used, and research runs on a third of the compute from then on. The delay is about the same in every case, and less than a 9-month lag.
- **A third is a tight limit.** In the AI Futures Project's input series, experiments, training and running AI researchers take 62% of the leading company's compute in 2026: 50%, 7% and 5%. A third of that is 21%, which matches a rule that about 79% of compute go to other uses. A rule of 60% would leave research about two thirds of baseline and delay TED-AI by 2 to 3 months. That run is not in the results file.

## Where the two levels come from

Both levels are the AI Futures Project's, read from its public code.

- **Its definitions.** A superhuman AI researcher "can fully automate AI R&D". A TED-AI "is at least as good as top human experts at virtually all cognitive tasks".
- **How its model marks them.** Both are levels of one quantity, AI research taste, in SD of the researcher distribution. The superhuman AI researcher is at the top researcher's level, which the model takes as the 99.9th percentile of a normal distribution, +3.09 SD (`TOP_RESEARCHER_SD` in the code's `progress_model/config.py`). TED-AI is a number of median-to-top gaps further on, each 3.09 SD (`ted_ai_m2b`, used in `progress_model/_impl.py`).
- **The +7.72 SD.** The number of gaps is a forecaster's judgment. It is 1.50 in the parameters of the example trajectory in the project's update of November 10, 2026, which gives 3.09 times 2.50, or +7.72 SD. The default in the public code is 1.00, which gives +6.18 SD.
- **What this model does with them.** It applies both levels to the research an AI-only lab gets from an experiment, after transfer and validity. It does not test "virtually all cognitive tasks". `chain_model.py` computes both levels from the percentile and the number of gaps, in the constants at the top of the file.

## How fast research gets harder

The debate over whether automated research runs away or peters out is a debate about this input. The model's value is 1: each year of software progress halves what research buys. The three fitted inputs are refitted at each value below.

| Halvings of what research buys per year of software progress | Share of a gain the AI must keep for the loop to run away | TED-AI, all judgment +3 SD | TED-AI, transfer +1 and metrics +0.5 | Central audits delay it |
|---|---|---|---|---|
| 0.25 | 19% | May 2027 | Mar 2028 | +15 mo |
| 0.5 | 39% | May 2027 | Jun 2028 | +16 mo |
| 0.75 | 58% | May 2027 | Aug 2028 | +16 mo |
| 1 | 78% | Jun 2027 | Nov 2028 | +16 mo |

The table stops at 1 because the model cannot reach the pace measured in November 2026 at much higher values. The highest difficulty that still fits, and how it moves with the inputs it rests on:

| Inputs | Highest difficulty that fits the pace of Nov 2026 | Share of a gain the AI must keep for the loop to run away at that difficulty |
|---|---|---|
| Central | 1.02 | 79% |
| AI labor per researcher on Nov 1, 2026: 26, twice OpenAI's trend | 1.53 | 119% |
| AI labor per researcher on Nov 1, 2026: 6.5, half of it | 0.37 | 29% |
| 25% of researcher time was on judging in Oct 2025 | 2.02 | 157% |
| 60% of researcher time was on judging in Oct 2025 | none above 0.3 | |
| Experiments rise with AI labor to the power 0.4 | 0.98 | 76% |
| Experiments rise with AI labor to the power 0.6 | 1.12 | 87% |
| Experiments from unlimited AI labor: 60 times | 1.06 | 83% |

- **The pace of 2026 caps how hard research can be getting.** At the central inputs the model reaches 1.7 times in November 2026 only if difficulty is 1.02 or less. Harder than that, 13 units of AI labor per researcher and the researcher time they free cannot add enough research.
- **At that cap the loop runs away once the AI keeps 79% of what people keep.** The most it can keep here is 153%. So the measured pace leaves room for a runaway. It does not show one: a runaway also needs the AI's judgment to improve as fast as the AI Futures Project assumes.
- **The cap is only as good as two inputs.** It is 1.53 if AI labor in November 2026 was twice OpenAI's trend and 0.37 if it was half. It is 2.02 if a quarter of researcher time went to judging in 2025, and at 60% the model cannot reach the measured pace at all. At 2.02 the loop cannot run away on ideas alone. The labor figure is OpenAI's and the pace was measured at Anthropic.
- **The cap takes the 1.7 times as the AI's doing.** METR attributed 80% of the rise in pace to AI and called the estimate uncertain. Garicano and Imas (November 2026) read the same period as faster growth in spending with diminishing returns and a one-time gain from AI tools.
- **Easier research brings the takeoff forward by months.** At 0.25, TED-AI in the slower case comes in March 2028 against November 2028.
- **One outside estimate is of the same order.** Garicano and Imas fit a research production function to Anthropic's capability index against its R&D spending. Their estimates have progress per unit of input falling about 0.8% to 6% for each index point. At about 13 index points for a year of progress before October 2025, that is 0.15 to 1.2 halvings a year. The conversion is ours, and their measure covers all progress and all R&D spending, so the comparison is rough.

## Each input moved

Case: ideas +3, transfer +1, metrics +0.5. TED-AI is November 2028 in the central row. Across the 18 rows in `results/tables.md` it runs from April 2028 to May 2029.

- **Earliest.** Validity of 0.3 with the AI judging today, and people able to vouch for any gain (both April 2028). An experiment ceiling of 60 times (June 2028).
- **Latest.** Judging time that grows with candidates (May 2029). Ideas at +2.1 SD (April 2029). Validity of 0.01 with the AI judging today (March 2029).
- **What the AI keeps today moves the date by about a year.** Validity with the AI judging runs from 0.3 to 0.01, against 0.05 in the central case, and TED-AI moves from April 2028 to March 2029.
- **The delay from central audits runs from 8 to 21 months** across the rows that leave the audit inputs alone.
- **The level set for TED-AI matters little.** At the public code's default of +6.18 SD, TED-AI in this case comes in October 2028, a month earlier. That run is not in the results file.

## Inputs

| Input | Value | Basis |
|---|---|---|
| Software share of progress | 2/3 | Judgment. The rest is more compute |
| Difficulty: halvings of what research buys per year of software progress | 1 | Judgment, at the top of what the pace of 2026 allows at the central inputs. Tested at 0.25, 0.5 and 0.75 |
| Experiments from AI labor | Square root, ceiling of 15 times | Judgment. Tested at 5 and 60 |
| Small experiments behind each one at scale, Oct 2025 | 20 | Judgment, from researchers' accounts that most experiments are discarded |
| Most candidates small-scale compute allows | 10,000 | Judgment. Tested at a million |
| Value of one SD of small-scale result | 0.3 log units | Judgment. Tested at 0.6 |
| Value of one SD of researcher judgment | 0.445 log units | The AI Futures Model's gap between the median and the top researcher, a factor of 3.97 over 3.09 SD |
| AI judgment on Nov 1, 2026 | -3.5 SD, all three kinds | The AI Futures Project's base case |
| Rate of ideas | +3 SD per year of progress | The AI Futures Project's base case. Tested at +2.1 |
| Rates of transfer and metric judgment | +3, +1 and +0.5 SD | +1 is the low end of the AI Futures Project's 80% interval and +0.5 is half of it. Neither is a measurement |
| Transfer: people, AI today, ceiling | 0.7, 0.2, 0.9 | Judgment. Only the ratios enter. AI today tested at 0.4 |
| Validity: people, AI today, ceiling | 0.8, 0.05, 0.95 | Judgment. Only the ratios enter. AI today tested at 0.3 and 0.01 |
| Shape of a link between the AI today and people's level | The same ratio for each SD | As research value is in the AI Futures Model |
| People can vouch for gains up to | +3.09 SD ideas | Judgment: the best researcher. Tested at +1 SD and with no limit |
| Researcher time on results, metrics and plans, Oct 2025 | 40% | Judgment. One of eight researchers Epoch AI interviewed said "60% of my time would be automated". Tested at 60% |
| Time to understand all deployed changes today | 14% | Judgment |
| Growth of deployed changes with AI labor | 0.4 | Judgment. Tested at 0 |
| Spread of value across deployed changes | Pareto index 1.8 | Judgment |
| Share of audit time that counts as judging | 50% | Judgment. Tested at 0 and 100% |

## What to hold loosely

- **The takeoff brings everything at once.** Transfer and metric judgment improve with progress, with no limit on how fast. In the case tabled above, the AI's metric judgment is at -1.2 SD in October 2028 and past the best researcher within two months. A lab would need its feedback on metrics to keep up with that.
- **Ideas have no ceiling.** AI judgment on well-defined problems rises without limit, as in the AI Futures Model.
- **Research is one stream.** Pretraining and post-training are not separated. A model in which gains on a fixed metric run out and progress waits for the next valid target would need two.
- **Validity does not fall under pressure.** Selecting harder on a metric does not lower its validity here.
- **The lab sees validity.** It is taken to know what its gains are really worth.
- **One set of central values.** Nothing is sampled.

## Run it

```
pip install -r requirements.txt
python chain_model.py > results/tables.md
pytest
```

`calibrate()` in `chain_model.py` refits the three fitted inputs. It takes about two minutes.

| File | What it is |
|---|---|
| `chain_model.py` | The model and the code that writes the tables |
| `test_chain_model.py` | Fifteen checks: the calibration, the AI Futures case the model reduces to, and the directions its results must move in |
| `results/tables.md` | Every table, written by the script |
| `LICENSE` | MIT |

This model is a companion to Readback's pacing briefing, which sits one folder up in the repository it comes from. Nothing here depends on it.
