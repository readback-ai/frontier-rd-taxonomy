# Chain model: milestone dates by scenario

Written by `chain_model.py`. Do not edit by hand.

Delays are against no pacing. Pacing starts Jan 1, 2027. Rates are SD of researcher judgment gained per year of progress. The loop runs away on better ideas alone once the AI's own judgment keeps 78% of the share of a gain that people's judgment keeps.

SAR, the superhuman AI researcher, and TED-AI are the AI Futures Project's milestones. They are the dates an AI-only lab's research matches a lab of researchers at the project's two levels, +3.09 and +7.72 SD above the median researcher. `over` means the run had ended by then.

## No pacing

| AI judgment gained per year of progress | SAR | TED-AI | Pace in Jan 2028 | As measured |
|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | May 2027 | May 2027 | over | over |
| Ideas and transfer +3, metrics +1 | Dec 2027 | Jan 2028 | 58.8x | 14.8x |
| Ideas and transfer +3, metrics +0.5 | Oct 2028 | Dec 2028 | 2.3x | 1.7x |
| Ideas +3, transfer and metrics +1 | May 2028 | May 2028 | 2.0x | 2.9x |
| Ideas +3, transfer +1, metrics +0.5 | Feb 2029 | Apr 2029 | 1.7x | 2.7x |
| Ideas +3, transfer and metrics +0.5 | Nov 2029 | Jan 2030 | 1.6x | 2.1x |

## Delay to TED-AI

| AI judgment gained per year | TED-AI, no pacing | Comprehension audits | 9-month lag | Audits and 9-month lag | Compute at a third of baseline |
|---|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | May 2027 | +0 mo | +10 mo | +11 mo | +4 mo |
| Ideas and transfer +3, metrics +1 | Jan 2028 | +4 mo | +10 mo | +11 mo | +6 mo |
| Ideas and transfer +3, metrics +0.5 | Dec 2028 | +13 mo | +12 mo | +16 mo | +6 mo |
| Ideas +3, transfer and metrics +1 | May 2028 | +4 mo | +9 mo | +11 mo | +7 mo |
| Ideas +3, transfer +1, metrics +0.5 | Apr 2029 | +12 mo | +12 mo | +17 mo | +7 mo |
| Ideas +3, transfer and metrics +0.5 | Jan 2030 | +14 mo | +11 mo | +18 mo | +8 mo |

## The path with no pacing: ideas and transfer +3, metrics +0.5

| Date | Pace | Pace as measured | Experiments at scale | Candidates behind each | Share of experiments people judge | Share of a gain the AI keeps | AI ideas | AI transfer judgment | AI metric judgment |
|---|---|---|---|---|---|---|---|---|---|
| Jan 2027 | 1.8x | 2.5x | 10.1x | 1,391 | 9% | 3% | -2.6 SD | -2.6 SD | -3.3 SD |
| Jul 2027 | 1.9x | 4.6x | 15.3x | 10,000 | 4% | 11% | +0.1 SD | +0.1 SD | -2.9 SD |
| Jan 2028 | 2.3x | 1.7x | 4.0x | 125 | 32% | 21% | +3.6 SD | +3.6 SD | -2.3 SD |
| Jul 2028 | 2.5x | 5.4x | 15.8x | 10,000 | 4% | 32% | +7.1 SD | +7.1 SD | -1.7 SD |

## Each input moved: ideas and transfer +3, metrics +0.5

| Case | SAR | TED-AI | Audits delay TED-AI | 9-month lag delays TED-AI |
|---|---|---|---|---|
| Central | Oct 2028 | Dec 2028 | +13 mo | +12 mo |
| Experiments from unlimited AI labor: 5 times | Jan 2029 | Apr 2029 | +12 mo | +11 mo |
| Experiments from unlimited AI labor: 60 times | Feb 2028 | Mar 2028 | +14 mo | +13 mo |
| Validity with the AI judging today: 0.3 | Oct 2027 | Dec 2027 | +9 mo | +13 mo |
| Validity with the AI judging today: 0.01 | Jun 2029 | Jul 2029 | +12 mo | +11 mo |
| Transfer with the AI judging today: 0.4 | Nov 2028 | Dec 2028 | +13 mo | +12 mo |
| AI never judges better than people | May 2029 | Jul 2029 | +15 mo | +11 mo |
| People can vouch for any gain | Apr 2028 | May 2028 | +1 mo | +16 mo |
| Audits take hours only: any change passes once understood | Oct 2028 | Dec 2028 | +2 mo | +12 mo |
| People can vouch for gains up to +1 SD ideas | Jan 2029 | Mar 2029 | +18 mo | +12 mo |
| Judging time per experiment grows with candidates, elasticity 0.25 | Dec 2028 | Jan 2029 | +13 mo | +12 mo |
| 60% of researcher time was already on judging | Dec 2028 | Feb 2029 | +13 mo | +12 mo |
| No researcher time goes to managing agents | Sep 2028 | Nov 2028 | +13 mo | +12 mo |
| A third of researcher time goes to managing agents | Nov 2028 | Jan 2029 | +13 mo | +12 mo |
| Ideas improve +2.1 SD a year | May 2029 | Jul 2029 | +12 mo | +12 mo |
| Selection worth twice as much | Sep 2028 | Oct 2028 | +15 mo | +12 mo |
| Up to a million candidates behind each experiment | Nov 2028 | Jan 2029 | +13 mo | +12 mo |
| Compute grows at half the historical rate from 2029 | Oct 2028 | Dec 2028 | +16 mo | +13 mo |
| Understanding all deployed changes takes twice the time | Oct 2028 | Dec 2028 | +14 mo | +12 mo |
| Audit time counts in full as judging | Oct 2028 | Dec 2028 | +12 mo | +12 mo |
| Audit time does not count as judging | Oct 2028 | Dec 2028 | +14 mo | +12 mo |
| Deployed changes do not grow with AI labor | Oct 2028 | Dec 2028 | +12 mo | +12 mo |

## By how fast research gets harder

The three fitted inputs are refitted at each difficulty. The most the AI's judgment can keep of a gain is 153% of what people's keeps.

| Halvings of what research buys per year of software progress | Share of a gain the AI must keep for the loop to run away | TED-AI, all judgment +3 SD | TED-AI, ideas and transfer +3 and metrics +0.5 | Audits delay it |
|---|---|---|---|---|
| 0.5 | 39% | Apr 2027 | Apr 2028 | +9 mo |
| 1 | 78% | May 2027 | Dec 2028 | +13 mo |
| 1.5 | 117% | Jun 2027 | Jul 2029 | +14 mo |
| 2 | 156% | Jul 2027 | Dec 2029 | +13 mo |

Above some difficulty the model cannot reach the pace measured in November 2026. The table below gives the highest difficulty that still fits, computed by `max_difficulty`, and how it moves with the inputs it rests on.

| Inputs | Highest difficulty that fits the pace of Nov 2026 | Share of a gain the AI must keep for the loop to run away at that difficulty |
|---|---|---|
| Central | 2.08 | 162% |
| AI labor per researcher in late August 2026: 38, twice Anthropic's figure | 2.63 | 205% |
| AI labor per researcher in late August 2026: 9.5, half of it | 1.36 | 106% |
| AI labor per researcher in late August 2026: 3.8, OpenAI's trend | none above 0.3 | |
| No researcher time goes to managing agents | 2.47 | 192% |
| 25% of researcher time was on judging in Oct 2025 | 2.69 | 210% |
| 60% of researcher time was on judging in Oct 2025 | 0.38 | 30% |
| Experiments rise with AI labor to the power 0.4 | 1.75 | 136% |
| Experiments rise with AI labor to the power 0.6 | 2.29 | 178% |
| Experiments from unlimited AI labor: 60 times | 2.52 | 196% |

## Every scenario

### Ideas, transfer and metrics all +3 SD a year

| Scenario | SAR | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | May 2027 |  | May 2027 |  |
| Comprehension audits | May 2027 | +0 mo | Jun 2027 | +0 mo |
| Internal-use lag, 3 months | Aug 2027 | +3 mo | Oct 2027 | +5 mo |
| Internal-use lag, 9 months | Oct 2027 | +5 mo | Apr 2028 | +10 mo |
| R&D compute at a third of baseline | Aug 2027 | +4 mo | Sep 2027 | +4 mo |
| Comprehension audits + 9-month lag | Oct 2027 | +5 mo | Apr 2028 | +11 mo |

### Ideas and transfer +3, metrics +1

| Scenario | SAR | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Dec 2027 |  | Jan 2028 |  |
| Comprehension audits | Mar 2028 | +3 mo | Apr 2028 | +4 mo |
| Internal-use lag, 3 months | Apr 2028 | +4 mo | Jun 2028 | +5 mo |
| Internal-use lag, 9 months | Aug 2028 | +8 mo | Nov 2028 | +10 mo |
| R&D compute at a third of baseline | Jun 2028 | +6 mo | Jul 2028 | +6 mo |
| Comprehension audits + 9-month lag | Sep 2028 | +9 mo | Dec 2028 | +11 mo |

### Ideas and transfer +3, metrics +0.5

| Scenario | SAR | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Oct 2028 |  | Dec 2028 |  |
| Comprehension audits | Jun 2029 | +7 mo | Jan 2030 | +13 mo |
| Internal-use lag, 3 months | Feb 2029 | +4 mo | Jun 2029 | +6 mo |
| Internal-use lag, 9 months | Jul 2029 | +8 mo | Dec 2029 | +12 mo |
| R&D compute at a third of baseline | Apr 2029 | +6 mo | Jun 2029 | +6 mo |
| Comprehension audits + 9-month lag | Sep 2029 | +10 mo | May 2030 | +16 mo |

### Ideas +3, transfer and metrics +1

| Scenario | SAR | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | May 2028 |  | May 2028 |  |
| Comprehension audits | Aug 2028 | +4 mo | Sep 2028 | +4 mo |
| Internal-use lag, 3 months | Aug 2028 | +4 mo | Oct 2028 | +5 mo |
| Internal-use lag, 9 months | Dec 2028 | +7 mo | Feb 2029 | +9 mo |
| R&D compute at a third of baseline | Dec 2028 | +7 mo | Dec 2028 | +7 mo |
| Comprehension audits + 9-month lag | Jan 2029 | +8 mo | Apr 2029 | +11 mo |

### Ideas +3, transfer +1, metrics +0.5

| Scenario | SAR | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Feb 2029 |  | Apr 2029 |  |
| Comprehension audits | Oct 2029 | +7 mo | Apr 2030 | +12 mo |
| Internal-use lag, 3 months | Jun 2029 | +4 mo | Sep 2029 | +6 mo |
| Internal-use lag, 9 months | Nov 2029 | +8 mo | Apr 2030 | +12 mo |
| R&D compute at a third of baseline | Sep 2029 | +7 mo | Nov 2029 | +7 mo |
| Comprehension audits + 9-month lag | Feb 2030 | +11 mo | Sep 2030 | +17 mo |

### Ideas +3, transfer and metrics +0.5

| Scenario | SAR | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Nov 2029 |  | Jan 2030 |  |
| Comprehension audits | Sep 2030 | +10 mo | Mar 2031 | +14 mo |
| Internal-use lag, 3 months | Mar 2030 | +3 mo | Jun 2030 | +5 mo |
| Internal-use lag, 9 months | Jul 2030 | +7 mo | Nov 2030 | +11 mo |
| R&D compute at a third of baseline | Jul 2030 | +7 mo | Aug 2030 | +8 mo |
| Comprehension audits + 9-month lag | Nov 2030 | +12 mo | Jun 2031 | +18 mo |

