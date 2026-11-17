# Chain model: milestone dates by scenario

Written by `chain_model.py`. Do not edit by hand.

Delays are against no pacing. Pacing starts Jan 1, 2027. Rates are SD of researcher judgment gained per year of progress. The loop runs away on better ideas alone once the AI's own judgment keeps 78% of the share of a gain that people's judgment keeps.

SAR, the superhuman AI researcher, and TED-AI are the AI Futures Project's milestones. They are the dates an AI-only lab's research matches a lab of researchers at the project's two levels, +3.09 and +7.72 SD above the median researcher. `over` means the run had ended by then.

## No pacing

| AI judgment gained per year of progress | SAR | TED-AI | Pace in Jan 2028 | As measured |
|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | Jun 2027 | Jun 2027 | over | over |
| Ideas and transfer +3, metrics +1 | Feb 2028 | Feb 2028 | 4.1x | 6.0x |
| Ideas and transfer +3, metrics +0.5 | Jan 2029 | Feb 2029 | 2.2x | 0.8x |
| Ideas +3, transfer and metrics +1 | Jun 2028 | Jun 2028 | 1.8x | 2.6x |
| Ideas +3, transfer +1, metrics +0.5 | Apr 2029 | Jun 2029 | 1.6x | 2.5x |
| Ideas +3, transfer and metrics +0.5 | Jan 2030 | Feb 2030 | 1.5x | 2.0x |

## Delay to TED-AI

| AI judgment gained per year | TED-AI, no pacing | Comprehension audits | 9-month lag | Audits and 9-month lag | Compute capped at 9.6% |
|---|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | Jun 2027 | +0 mo | +11 mo | +11 mo | +7 mo |
| Ideas and transfer +3, metrics +1 | Feb 2028 | +3 mo | +10 mo | +11 mo | +11 mo |
| Ideas and transfer +3, metrics +0.5 | Feb 2029 | +12 mo | +12 mo | +16 mo | +10 mo |
| Ideas +3, transfer and metrics +1 | Jun 2028 | +4 mo | +10 mo | +11 mo | +12 mo |
| Ideas +3, transfer +1, metrics +0.5 | Jun 2029 | +12 mo | +12 mo | +17 mo | +11 mo |
| Ideas +3, transfer and metrics +0.5 | Feb 2030 | +13 mo | +11 mo | +17 mo | +12 mo |

## The path with no pacing: ideas and transfer +3, metrics +0.5

| Date | Pace | Pace as measured | Experiments at scale | Candidates behind each | Share of experiments people judge | Share of a gain the AI keeps | AI ideas | AI transfer judgment | AI metric judgment |
|---|---|---|---|---|---|---|---|---|---|
| Jan 2027 | 1.5x | 2.1x | 8.3x | 674 | 6% | 3% | -2.7 SD | -2.7 SD | -3.4 SD |
| Jul 2027 | 1.7x | 4.0x | 14.3x | 10,000 | 1% | 9% | -0.3 SD | -0.3 SD | -3.0 SD |
| Jan 2028 | 2.2x | 0.8x | 2.7x | 71 | 37% | 18% | +2.6 SD | +2.6 SD | -2.5 SD |
| Jul 2028 | 2.1x | 2.3x | 1.9x | 43 | 59% | 28% | +6.0 SD | +6.0 SD | -1.9 SD |
| Jan 2029 | 4.1x | 6.6x | 15.5x | 10,000 | 1% | 47% | +9.9 SD | +9.9 SD | -1.3 SD |

## Each input moved: ideas and transfer +3, metrics +0.5

| Case | SAR | TED-AI | Audits delay TED-AI | 9-month lag delays TED-AI |
|---|---|---|---|---|
| Central | Jan 2029 | Feb 2029 | +12 mo | +12 mo |
| Experiments from unlimited AI labor: 5 times | Mar 2029 | Jun 2029 | +11 mo | +11 mo |
| Experiments from unlimited AI labor: 60 times | Mar 2028 | Apr 2028 | +14 mo | +14 mo |
| Validity with the AI judging today: 0.3 | Nov 2027 | Dec 2027 | +8 mo | +13 mo |
| Validity with the AI judging today: 0.01 | Aug 2029 | Sep 2029 | +12 mo | +11 mo |
| Transfer with the AI judging today: 0.4 | Jan 2029 | Feb 2029 | +12 mo | +12 mo |
| AI never judges better than people | Jun 2029 | Aug 2029 | +15 mo | +12 mo |
| People can vouch for any gain | Jun 2028 | Jul 2028 | +1 mo | +16 mo |
| Audits take hours only: any change passes once understood | Jan 2029 | Feb 2029 | +1 mo | +12 mo |
| People can vouch for gains up to +1 SD ideas | Feb 2029 | Apr 2029 | +17 mo | +12 mo |
| Judging time per experiment grows with candidates, elasticity 0.25 | Nov 2028 | Jan 2029 | +13 mo | +12 mo |
| 60% of researcher time was already on judging | Feb 2029 | Mar 2029 | +12 mo | +12 mo |
| No researcher time goes to managing agents | Dec 2028 | Jan 2029 | +12 mo | +12 mo |
| A third of researcher time goes to managing agents | Jan 2029 | Mar 2029 | +13 mo | +12 mo |
| Ideas improve +2.1 SD a year | Jul 2029 | Sep 2029 | +11 mo | +12 mo |
| Selection worth twice as much | Nov 2028 | Dec 2028 | +14 mo | +12 mo |
| Up to a million candidates behind each experiment | Jan 2029 | Feb 2029 | +12 mo | +12 mo |
| Compute grows at half the historical rate from 2029 | Jan 2029 | Feb 2029 | +16 mo | +14 mo |
| Understanding all deployed changes takes twice the time | Jan 2029 | Feb 2029 | +13 mo | +12 mo |
| Audit time counts in full as judging | Jan 2029 | Feb 2029 | +12 mo | +12 mo |
| Audit time does not count as judging | Jan 2029 | Feb 2029 | +13 mo | +12 mo |
| Deployed changes do not grow with AI labor | Jan 2029 | Feb 2029 | +11 mo | +12 mo |

## By how fast research gets harder

The three fitted inputs are refitted at each difficulty. The most the AI's judgment can keep of a gain is 153% of what people's keeps.

| Halvings of what research buys per year of software progress | Share of a gain the AI must keep for the loop to run away | TED-AI, all judgment +3 SD | TED-AI, ideas and transfer +3 and metrics +0.5 | Audits delay it |
|---|---|---|---|---|
| 0.5 | 39% | May 2027 | Jun 2028 | +9 mo |
| 1 | 78% | Jun 2027 | Feb 2029 | +12 mo |
| 1.5 | 117% | Jul 2027 | Sep 2029 | +13 mo |
| 2 | 156% | Aug 2027 | Jan 2030 | +12 mo |

Above some difficulty the model cannot reach the pace measured in November 2026. The table below gives the highest difficulty that still fits, computed by `max_difficulty`, and how it moves with the inputs it rests on.

| Inputs | Highest difficulty that fits the pace of Nov 2026 | Share of a gain the AI must keep for the loop to run away at that difficulty |
|---|---|---|
| Central | 2.62 | 204% |
| AI labor per researcher in late August 2026: 38, twice Anthropic's figure | 3.0 or more | 234% or more |
| AI labor per researcher in late August 2026: 9.5, half of it | 1.74 | 136% |
| AI labor per researcher in late August 2026: 3.8, OpenAI's trend | 0.31 | 24% |
| No researcher time goes to managing agents | 2.91 | 227% |
| 25% of researcher time was on judging in Oct 2025 | 3.0 or more | 234% or more |
| 60% of researcher time was on judging in Oct 2025 | 1.62 | 126% |
| Experiments rise with AI labor to the power 0.4 | 2.16 | 168% |
| Experiments rise with AI labor to the power 0.6 | 2.96 | 231% |
| Experiments from unlimited AI labor: 60 times | 3.0 or more | 234% or more |

## Every scenario

### Ideas, transfer and metrics all +3 SD a year

| Scenario | SAR | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Jun 2027 |  | Jun 2027 |  |
| Comprehension audits | Jun 2027 | +0 mo | Jun 2027 | +0 mo |
| Internal-use lag, 3 months | Sep 2027 | +3 mo | Nov 2027 | +5 mo |
| Internal-use lag, 9 months | Nov 2027 | +6 mo | May 2028 | +11 mo |
| R&D compute capped at 9.6% of all compute | Dec 2027 | +7 mo | Jan 2028 | +7 mo |
| Comprehension audits + 9-month lag | Nov 2027 | +6 mo | May 2028 | +11 mo |

### Ideas and transfer +3, metrics +1

| Scenario | SAR | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Feb 2028 |  | Feb 2028 |  |
| Comprehension audits | Apr 2028 | +2 mo | May 2028 | +3 mo |
| Internal-use lag, 3 months | Jun 2028 | +4 mo | Jul 2028 | +5 mo |
| Internal-use lag, 9 months | Oct 2028 | +8 mo | Dec 2028 | +10 mo |
| R&D compute capped at 9.6% of all compute | Dec 2028 | +11 mo | Jan 2029 | +11 mo |
| Comprehension audits + 9-month lag | Oct 2028 | +9 mo | Jan 2029 | +11 mo |

### Ideas and transfer +3, metrics +0.5

| Scenario | SAR | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Jan 2029 |  | Feb 2029 |  |
| Comprehension audits | Jul 2029 | +7 mo | Mar 2030 | +12 mo |
| Internal-use lag, 3 months | Apr 2029 | +4 mo | Aug 2029 | +6 mo |
| Internal-use lag, 9 months | Sep 2029 | +8 mo | Feb 2030 | +12 mo |
| R&D compute capped at 9.6% of all compute | Oct 2029 | +9 mo | Dec 2029 | +10 mo |
| Comprehension audits + 9-month lag | Oct 2029 | +10 mo | Jun 2030 | +16 mo |

### Ideas +3, transfer and metrics +1

| Scenario | SAR | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Jun 2028 |  | Jun 2028 |  |
| Comprehension audits | Sep 2028 | +3 mo | Oct 2028 | +4 mo |
| Internal-use lag, 3 months | Oct 2028 | +4 mo | Nov 2028 | +5 mo |
| Internal-use lag, 9 months | Jan 2029 | +7 mo | Apr 2029 | +10 mo |
| R&D compute capped at 9.6% of all compute | Jun 2029 | +12 mo | Jun 2029 | +12 mo |
| Comprehension audits + 9-month lag | Feb 2029 | +8 mo | May 2029 | +11 mo |

### Ideas +3, transfer +1, metrics +0.5

| Scenario | SAR | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Apr 2029 |  | Jun 2029 |  |
| Comprehension audits | Nov 2029 | +7 mo | May 2030 | +12 mo |
| Internal-use lag, 3 months | Aug 2029 | +4 mo | Nov 2029 | +6 mo |
| Internal-use lag, 9 months | Jan 2030 | +8 mo | Jun 2030 | +12 mo |
| R&D compute capped at 9.6% of all compute | Apr 2030 | +11 mo | May 2030 | +11 mo |
| Comprehension audits + 9-month lag | Mar 2030 | +11 mo | Nov 2030 | +17 mo |

### Ideas +3, transfer and metrics +0.5

| Scenario | SAR | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Jan 2030 |  | Feb 2030 |  |
| Comprehension audits | Nov 2030 | +9 mo | Apr 2031 | +13 mo |
| Internal-use lag, 3 months | May 2030 | +4 mo | Aug 2030 | +5 mo |
| Internal-use lag, 9 months | Sep 2030 | +8 mo | Jan 2031 | +11 mo |
| R&D compute capped at 9.6% of all compute | Jan 2031 | +11 mo | Feb 2031 | +12 mo |
| Comprehension audits + 9-month lag | Jan 2031 | +12 mo | Aug 2031 | +17 mo |

