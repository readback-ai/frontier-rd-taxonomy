# The chain model: from small experiments to real value

Draft of 2026-11-16, from Readback Labs. This folder is self-contained: one model file, its checks, its results and this write-up. Every number below is from `results/tables.md`, which the model writes, unless a line says otherwise.

## The question

AI now does a growing share of AI research. If better AI makes research faster and faster research makes better AI, the pace can compound. This model asks when that happens and what three pacing policies, and two of them together, do about it.

It is built for one disagreement. One side holds that AI research is mostly hill-climbing on measurable targets, so AI will soon do all of it. The other holds that the hard part is deciding what to climb: defining a metric that means what you want, and noticing when a result games it. The model gives each of those its own place, so the disagreement becomes a question about a few inputs.

Terms:

- **Progress** is measured in years of AI progress at the rate before October 2025. **Pace** is years of progress per calendar year.
- **SD** is a standard deviation of research judgment across a lab's researchers. The best researcher is at +3.09 SD.
- **SAR**, the superhuman AI researcher, and **TED-AI**, top-expert-dominating AI, are the AI Futures Project's two milestones, at the levels its model sets. SAR is at +3.09 SD above the median researcher, the level of a lab's best researcher. TED-AI is at +7.72 SD. Each date here is when an AI-only lab's research matches a lab of researchers at that level.

## How the model works

**Experiments.** Experiments at scale are limited by compute. Behind each one the lab runs many small experiments and backs the candidate that looks best. AI labor raises the number of experiments a lab gets from its compute, with diminishing returns and a ceiling. It also multiplies the candidates, which helps less and less: the best of n candidates is about sqrt(2 ln n) SD better than a typical one.

**The chain.** Two links separate how good a candidate looks from what it is worth.

```
small-scale result  ->  result on the metric at scale  ->  real value
                 transfer                            validity
```

- **Transfer** is the share of a small-scale gain that holds at scale. It depends on who judged which candidate would transfer.
- **Validity** is the share of a gain on the metric that is real. It depends on who defined the metric and checked the result for gaming.

The share of a gain that survives both links is what a judge keeps. The links multiply in the exponent of an experiment's value:

```
value = exp(kept * (standing + gain) - standing)
kept  = transfer * validity, each measured against people's
```

`gain` is what has been added at small scale since October 2025: better ideas from the AI, and the best of more candidates. `standing` is what an experiment was already worth.

**Three kinds of AI judgment.** Each improves at its own rate, in SD per year of progress. All three start at -3.5 SD on November 1, 2026.

| Kind | What it does | Rate |
|---|---|---|
| Ideas | Proposes candidates on a well-defined problem. No ceiling | +3 SD |
| Transfer | Judges which small-scale gains hold at scale | +3, +1 or +0.5 SD |
| Metrics | Defines the next metric and debugs results that game the current one | +3, +1 or +0.5 SD |

**People.** A person who judges an experiment supplies both links at people's level, and keeps all of its gain. Two things limit this:

- **Time.** Researchers judge as many experiments as they have time for. The AI judges the rest with its own transfer and metric judgment and keeps less. AI takes over implementation, which frees researcher time. Managing the agents takes part of it back.
- **Reach.** People can vouch for a gain only up to what their best researcher could have proposed. The AI judges any part of a gain beyond that.

**The lab chooses.** It runs the amount of AI labor that gives it the most research. More agents mean more experiments and more candidates. They also mean more for people to judge and more deployed changes.

**The loop.** Real research makes software progress, and progress makes better AI. Research also gets harder: each year of software progress halves what a unit of research buys. Compute and people have grown fast enough to offset that, which is what a pace of 1 means. The loop runs away when the AI's judgment adds research faster than difficulty takes it away. That happens once the AI's own judgment keeps 78% of what people's keeps.

**Three pacing policies.** All start on January 1, 2027.

- **Comprehension audits.** A lab may deploy only what its own people understand. That takes researchers' hours for every deployed change: 14% of their time today, growing with the number of changes. It also has a reach. People cannot understand a gain past what they can vouch for, so an audited lab does not deploy that part.
- **Internal-use lag.** A lab works with the AI it had nine months ago.
- **Compute limit.** A lab may use a third of the compute it otherwise would for experiments, for running AI labor and for training.

Audits and the lag are also run together.

## What it builds on

The outer structure is the AI Futures Project's model: experiments limited by compute, AI labor with diminishing returns, judgment in SD of the researcher distribution, and research that gets harder. With the AI's two links set to people's values and no gain from selection, research here is the AI Futures rule exactly, and a check confirms it.

The two milestone levels are also theirs, read from their public code. A superhuman AI researcher (SAR) "can fully automate AI R&D", and a TED-AI "is at least as good as top human experts at virtually all cognitive tasks". Their model marks both as levels of research taste. The first is the 99.9th percentile of a normal distribution, +3.09 SD (`TOP_RESEARCHER_SD`). The second is a number of median-to-top gaps further on (`ted_ai_m2b`), which is a forecaster's judgment: 1.50 in the example trajectory of their update of November 10, 2026, giving +7.72 SD. This model applies both levels to an AI-only lab. A milestone arrives when an experiment left to the AI, with its own transfer and metric judgment, is worth what it would be with ideas at that level and people's judgment on both links. Weak links cost the AI a share of the value an experiment already had as well as a share of its ideas. The AI Futures Model has no such links, so an AI whose ideas reach +3.09 SD is a SAR there. Here it is a SAR only once its own transfer and metric judgment carry those ideas through, which is later.

Three inputs to the loop follow Ryan Greenblatt's public estimates.

- **Software share.** "I tend to think that ~2/3 of AI progress is algorithms while ~1/3 is from scaling up compute for training runs." The model uses 2/3.
- **Difficulty.** He estimates that software R&D slows by about 2 times for each year of software progress with inputs held fixed. That is one halving per year of software progress, the model's value of 1. This one is second-hand, as the next paragraph says.
- **Labor and compute.** "I tend to think the functional form for just AI R&D progress (like algorithmic progress) is like serial_labor_acceleration^0.55 * compute^0.45." He calls 0.7 and 0.3 "somewhat plausible" in either order. The model's square root is close to this and is not the same quantity: his labor input is how much faster staff work, and the model's is AI labor per researcher, which the fit to Anthropic's agent hours sets.

Both quotes are from the appendix of his post of April 2026, ["If Mythos actually made Anthropic employees 4x more productive, I would radically shorten my timelines"](https://www.lesswrong.com/posts/Jga7PHMzfZf4fbdyo/if-mythos-actually-made-anthropic-employees-4x-more). He describes that model as "basically a simplified version of the AI Futures Project model with somewhat different constants". The post offers the form for increases under about 30 times and sets diminishing returns aside. The difficulty estimate is from his [thread on X](https://x.com/RyanGreenblatt/status/2118447235289817503) about METR's report, which Zvi Mowshowitz reproduces in ["AI R&D Is Accelerating Towards Potential RSI in 2027"](https://thezvi.substack.com/p/ai-r-and-d-is-accelerating-towards) (November 9, 2026). Neither page could be snapshotted, so it is paraphrased here and not quoted. The thread points to an earlier [comment](https://www.lesswrong.com/posts/FG54euEAesRkSZuJN/ryan_greenblatt-s-shortform?commentId=rAFxcETtNtsuzw6aG) for the modeling behind it.

Ajeya Cotra's ["AI is dramatically accelerating AI research right now"](https://www.planned-obsolescence.org/p/ai-is-dramatically-accelerating-ai) (November 6, 2026) is a simplified version of the modeling in that thread. Its footnote 6 links the thread and cites the comment and the post as the basis of his numbers. Her footnote 8 gives the model's square root: "To make the math simple, I just assumed that labor and experiment compute contributed equally". She thanks him for help with the modeling, so the two are one estimate and not two.

The quotes from his post and from hers are verified against snapshots in the repository's source records `S-greenblatt-2026-04-mythos-4x-productivity` and `S-cotra-2026-11-ai-accelerating-ai`.

## Calibration

Three inputs are fitted to three measurements, all from Anthropic.

| Measurement | Value | Source | Input fitted | Fitted value |
|---|---|---|---|---|
| Pace on May 1, 2026 | 1.2 times | The AI Futures Project's estimate in its update of November 10, 2026 | Years of progress per doubling of AI labor | 0.11 |
| Pace on Nov 1, 2026 | 1.7 times | The same update's reading of METR's assessment of November 5, 2026, which put the pace at Anthropic at about 2 times with a range of 1.3 to 3 and attributed 80% of the rise to AI | Growth of judging time with candidates | 0.19 |
| AI labor per researcher in late August 2026 | 19 agent hours for each human work-hour | Anthropic, "How employment is changing at Anthropic", Figure 2, research organizations | AI labor on Oct 1, 2025 | 0.03 |

- **The fit has an independent check.** The model's AI labor doubles about monthly in mid-2026. Anthropic's series, which is not used to fit the doubling, rose from 0.2 agent hours per human hour in February 2026 to 19 in late August, a doubling every 31 days. The series was read from the chart by eye.
- **People's time is already short.** In the fitted model researchers judge 36% of experiments at scale in late August 2026 and 17% on November 1.
- **Managing agents takes researcher time.** Anthropic reports that 22% of model researchers' agent sessions in spring 2026 were meta-work: writing specs for agents, setting one agent to review another, watching pipelines. The model takes that as a share of researcher time, which is an assumption.

## Results with no pacing

The primary scenario is the third row.

| AI judgment gained per year of progress | SAR | TED-AI |
|---|---|---|
| Ideas, transfer and metrics all +3 SD | May 2027 | May 2027 |
| Ideas and transfer +3, metrics +1 | Dec 2027 | Jan 2028 |
| **Ideas and transfer +3, metrics +0.5 (primary)** | **Oct 2028** | **Dec 2028** |
| Ideas +3, transfer and metrics +1 | May 2028 | May 2028 |
| Ideas +3, transfer +1, metrics +0.5 | Feb 2029 | Apr 2029 |
| Ideas +3, transfer and metrics +0.5 | Nov 2029 | Jan 2030 |

- **Slow transfer and metric judgment delay the takeoff by up to three years and do not prevent it.** In the primary scenario the pace holds between 1.8 and 2.5 times through mid-2028 and rises steeply in the months after.
- **A weak link slows the loop and sets no ceiling.** An AI that keeps 10% of a gain turns ideas improving 3 SD a year into 0.3 SD a year of real judgment.
- **People judge very little of the work.** In the primary scenario researchers judge 9% of experiments at scale in January 2027 and 4% from mid-2027.
- **Measured progress runs ahead of real progress.** The pace the lab's own metrics show is 4.6 times in July 2027 against a real 1.9.
- **TED-AI arrives on the strength of ideas.** When it arrives in December 2028 the AI's metric judgment is at -0.8 SD. Its ideas are 13 SD above the median researcher's and its own judgment keeps 70% of what people's would.

The path in the primary scenario:

| Date | Pace | Pace on the lab's metrics | Experiments at scale | Share of experiments people judge | Share of a gain the AI keeps | AI ideas and transfer judgment | AI metric judgment |
|---|---|---|---|---|---|---|---|
| Jan 2027 | 1.8x | 2.5x | 10.1x | 9% | 3% | -2.6 SD | -3.3 SD |
| Jul 2027 | 1.9x | 4.6x | 15.3x | 4% | 11% | +0.1 SD | -2.9 SD |
| Jan 2028 | 2.3x | 1.7x | 4.0x | 32% | 21% | +3.6 SD | -2.3 SD |
| Jul 2028 | 2.5x | 5.4x | 15.8x | 4% | 32% | +7.1 SD | -1.7 SD |

The January 2028 row looks different because the lab has two ways of working. It can run every agent it has and leave most experiments to the AI, or run a few dozen agents per researcher and have people judge a third of the experiments. The two give nearly the same research. Around January 2028, when the AI's ideas are just past what people can vouch for, the second is slightly ahead and the lab takes it.

## What pacing does

![Pace of AI progress in the primary scenario under four pacing policies](results/pace.png)

The figure is the primary scenario. Each line is the pace under one policy and ends when TED-AI arrives. The two open circles are the measured paces the model is fitted to.

Delay to TED-AI:

| AI judgment gained per year of progress | Comprehension audits | 9-month lag | Audits and 9-month lag | Compute at a third of baseline |
|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD | +0 mo | +10 mo | +11 mo | +4 mo |
| Ideas and transfer +3, metrics +1 | +4 mo | +10 mo | +11 mo | +6 mo |
| **Ideas and transfer +3, metrics +0.5 (primary)** | **+13 mo** | **+12 mo** | **+16 mo** | **+6 mo** |
| Ideas +3, transfer and metrics +1 | +4 mo | +9 mo | +11 mo | +7 mo |
| Ideas +3, transfer +1, metrics +0.5 | +12 mo | +12 mo | +17 mo | +7 mo |
| Ideas +3, transfer and metrics +0.5 | +14 mo | +11 mo | +18 mo | +8 mo |

**Comprehension audits**

- **Under audits the loop does not run away.** In the primary scenario the pace peaks at 2.6 times at the start of 2028 and is 1.4 to 1.7 times from mid-2028 through 2029. With no pacing it reaches 14.6 times as TED-AI arrives.
- **TED-AI still arrives, 13 months later, as a capability the lab may not fully use.** The lab keeps making progress on gains its people can vouch for, and the AI keeps improving with that progress. In January 2030 the newest AI could do research at the TED-AI level. The audited lab deploys only the part of its ideas that people can vouch for.
- **The reach does the work.** If any change passes once people have spent the hours, audits delay TED-AI by 2 months. If the hours double, the delay goes from 13 months to 14.
- **Audits delay most where the AI's metric judgment is slow.** They delay TED-AI by 12 to 14 months with metrics at +0.5 SD, by 4 months at +1 SD and by less than a month where all judgment improves 3 SD a year. In that last scenario TED-AI arrives before the AI's ideas are far past people's.
- **An audited lab runs far fewer agents.** More agents mean more changes to understand. From 2028 to early 2029 the audited lab runs 12 to 34 agents per researcher, and its people judge a quarter to two fifths of its experiments.

**Lag and compute**

- **A 9-month lag delays TED-AI by 9 to 12 months in every scenario.** It sets back the AI the lab may use, and so the judgment that drives the loop.
- **Audits and the lag together delay it by 11 to 18 months.** That is less than the two delays added up. In the primary scenario the two together give 16 months, against 13 and 12 apart, and the pace ends at 1.3 times.
- **A compute limit delays it by 4 to 8 months, once.** Training waits about a year for its allowance to catch up with what it has already used, and research runs on a third of the compute from then on. A cut in research buys a fixed delay because difficulty is exponential: a lab with half the research ends up one year of software progress behind and stays there.
- **A third is a tight limit.** In the AI Futures Project's input series, experiments, training and running AI researchers take 62% of the leading company's compute in 2026. A third of that is 21%, which matches a rule that about 79% of compute go to other uses. A rule of 60% would leave research about two thirds of baseline and delay TED-AI by 2 to 3 months. That run is not in the results file.

## How fast research gets harder

Whether automated research runs away or peters out is a question about this input. The model's value is 1: each year of software progress halves what research buys. The three fitted inputs are refitted at each value below.

| Halvings of what research buys per year of software progress | Share of a gain the AI must keep for the loop to run away | TED-AI, primary scenario | Audits delay it |
|---|---|---|---|
| 0.5 | 39% | Apr 2028 | +9 mo |
| 1 | 78% | Dec 2028 | +13 mo |
| 1.5 | 117% | Jul 2029 | +14 mo |
| 2 | 156% | Dec 2029 | +13 mo |

- **Above about 1.96 the loop cannot run away on ideas alone.** The most the AI can keep of a gain here is 153% of what people keep.
- **TED-AI arrives at every value in the table.** At 2 it comes in December 2029, because ideas have no ceiling and the pace holds above 1 while they accumulate.
- **The measured pace of 2026 does not settle the question.** The model reaches 1.7 times in November 2026 at any difficulty up to 2.08, which spans both sides of that line.
- **That cap rests on two inputs.** It is 1.36 if AI labor in late August 2026 was half Anthropic's figure and 2.63 if it was twice. It is 2.69 if a quarter of researcher time went to judging in 2025 and 0.38 if 60% did. `results/tables.md` has the full table.
- **It also takes the 1.7 times as the AI's doing.** METR attributed 80% of the rise in pace to AI and called the estimate uncertain. Garicano and Imas (November 2026) read the same period as faster growth in spending with diminishing returns and a one-time gain from AI tools.

## Each input moved

The primary scenario, one input at a time. TED-AI is December 2028 in the central row. Across the 22 rows in `results/tables.md` it runs from December 2027 to July 2029.

- **Earliest.** Validity of 0.3 with the AI judging today (December 2027). An experiment ceiling of 60 times (March 2028). People able to vouch for any gain (May 2028).
- **Latest.** Validity of 0.01 with the AI judging today, an AI that never judges better than people, and ideas at +2.1 SD (all July 2029).
- **The delay from audits is 9 to 18 months in every row but two.** Those are the rows that remove the reach: people able to vouch for any gain (1 month) and audits that take hours only (2 months). With a reach of +1 SD ideas the delay is 18 months.
- **The delay from a 9-month lag is 11 to 16 months.**
- **Time spent managing agents matters little.** With none, TED-AI comes in November 2028, and with a third of researcher time, January 2029.
- **The level set for TED-AI matters little.** At the AI Futures code's default of +6.18 SD it also comes in December 2028. That run is not in the results file.

## Inputs

| Input | Value | Basis |
|---|---|---|
| Software share of progress | 2/3 | Greenblatt's estimate. The rest is more compute |
| Difficulty: halvings of what research buys per year of software progress | 1 | Greenblatt's estimate. The pace of 2026 allows up to 2.08. Tested at 0.5, 1.5 and 2 |
| Experiments from AI labor | Square root, ceiling of 15 times | The square root is Cotra's simplification, close to Greenblatt's 0.55. The limit on difficulty is run at 0.4 and 0.6. The ceiling is judgment, tested at 5 and 60 |
| Small experiments behind each one at scale, Oct 2025 | 20 | Judgment, from researchers' accounts that most experiments are discarded |
| Most candidates small-scale compute allows | 10,000 | Judgment. Tested at a million |
| Value of one SD of small-scale result | 0.3 log units | Judgment. Tested at 0.6 |
| Value of one SD of researcher judgment | 0.445 log units | The AI Futures Model's gap between the median and the top researcher, a factor of 3.97 over 3.09 SD |
| AI judgment on Nov 1, 2026 | -3.5 SD, all three kinds | The AI Futures Project's base case |
| Rate of ideas | +3 SD per year of progress | The AI Futures Project's base case. Tested at +2.1 |
| Rates of transfer and metric judgment | +3, +1 and +0.5 SD | +1 is the low end of the AI Futures Project's 80% interval and +0.5 is half of it. Neither is a measurement |
| Transfer: people, AI today, ceiling | 0.7, 0.2, 0.9 | Judgment. Only the ratios enter. AI today tested at 0.4 |
| Validity: people, AI today, ceiling | 0.8, 0.05, 0.95 | Judgment. Only the ratios enter. AI today tested at 0.3 and 0.01 |
| How a link rises from the AI today to people's level | The same ratio for each SD | As research value does in the AI Futures Model |
| People can vouch for gains up to | +3.09 SD ideas | Judgment: the best researcher. Tested at +1 SD and with no limit |
| Researcher time on results, metrics and plans, Oct 2025 | 40% | Judgment. One of eight researchers Epoch AI interviewed said "60% of my time would be automated". Tested at 60% |
| Researcher time managing agents once AI does the implementation | 22% | Anthropic's share of model researchers' agent sessions that were meta-work, used as a share of time. Tested at 0 and a third |
| Time to understand all deployed changes today | 14% | Judgment. Tested at 28% |
| Growth of deployed changes with AI labor | 0.4 | Judgment. Anthropic's commits per engineer and agent hours give about 0.35 to 0.4 over six months of 2026. Tested at 0 |
| Spread of value across deployed changes | Pareto index 1.8 | Judgment |
| Share of audit time that counts as judging | 50% | Judgment. Tested at 0 and 100% |
| What an audit passes | A gain only as far as people can vouch for it | Judgment: an audit that people can pass on a change they cannot evaluate does not test comprehension. Tested with hours only |

## What to hold loosely

- **AI labor keeps doubling, with no cap.** The model extrapolates a monthly doubling of agent hours per researcher that has been observed for seven months. It has 113 agent hours per human hour on November 1, 2026 and 724 on January 1, 2027. What that labor adds is capped, and a lab runs only as much of it as helps.
- **Ideas have no ceiling.** AI judgment on well-defined problems rises without limit, as in the AI Futures Model. TED-AI arrives on ideas alone because of it.
- **Judgment improves with progress, with no limit on how fast.** A lab would need its feedback on transfer and metrics to keep up.
- **How far people can vouch is fixed.** It stays at the best researcher's level however good the AI becomes at explaining its work. If AI help extends it, audits delay less.
- **Under audits TED-AI is a capability, and the model stops there.** It does not follow what a lab does with an AI it may not fully use, or whether the audit holds.
- **Research is one stream.** Pretraining and post-training are not separated.
- **Validity does not fall under pressure.** Selecting harder on a metric does not lower its validity here.
- **The lab sees real value.** It is taken to know what its gains are really worth and to choose on that.
- **One set of central values.** Nothing is sampled.

## Run it

```
pip install -r requirements.txt
python chain_model.py > results/tables.md
python figure.py
pytest
```

`calibrate()` in `chain_model.py` refits the three fitted inputs. It takes about two minutes.

| File | What it is |
|---|---|
| `chain_model.py` | The model and the code that writes the tables |
| `figure.py` | Draws `results/pace.png`. Needs matplotlib |
| `test_chain_model.py` | Nineteen checks: the calibration, the AI Futures case the model reduces to, and the directions its results must move in |
| `results/tables.md` | Every table, written by the model |
| `LICENSE` | MIT |
