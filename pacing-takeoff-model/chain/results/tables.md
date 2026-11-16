# Chain model: milestone dates by scenario

Written by `chain_model.py`. Do not edit by hand.

Delays are against no pacing. Pacing starts Jan 1, 2027. Rates are SD of researcher judgment gained per year of progress. The loop runs away on better ideas alone once the AI's own judgment keeps 78% of the share of a gain that people's judgment keeps.

Researcher-level AI and TED-AI are the dates an AI-only lab's research matches a lab of researchers at AI Futures' two levels, +3.09 and +7.72 SD. `over` means the run had ended by then.

## No pacing

| AI judgment gained per year of progress | Researcher-level AI | TED-AI | Pace in Jan 2028 | As measured |
|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | May 2027 | May 2027 | over | over |
| Ideas and transfer +3, metrics +1 | Dec 2027 | Jan 2028 | 58.8x | 14.8x |
| Ideas and transfer +3, metrics +0.5 | Aug 2028 | Dec 2028 | 2.3x | 1.7x |
| Ideas +3, transfer and metrics +1 | May 2028 | May 2028 | 2.0x | 2.9x |
| Ideas +3, transfer +1, metrics +0.5 | Jan 2029 | Apr 2029 | 1.7x | 2.7x |
| Ideas +3, transfer and metrics +0.5 | Sep 2029 | Jan 2030 | 1.6x | 2.1x |

## Delay to TED-AI

| AI judgment gained per year | TED-AI, no pacing | Comprehension audits | 9-month lag | Audits and 9-month lag | Compute at a third of baseline |
|---|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | May 2027 | +1 mo | +11 mo | +12 mo | +4 mo |
| Ideas and transfer +3, metrics +1 | Jan 2028 | +4 mo | +10 mo | +11 mo | +6 mo |
| Ideas and transfer +3, metrics +0.5 | Dec 2028 | +12 mo | +11 mo | +15 mo | +6 mo |
| Ideas +3, transfer and metrics +1 | May 2028 | +4 mo | +9 mo | +11 mo | +7 mo |
| Ideas +3, transfer +1, metrics +0.5 | Apr 2029 | +11 mo | +11 mo | +16 mo | +7 mo |
| Ideas +3, transfer and metrics +0.5 | Jan 2030 | +13 mo | +10 mo | +16 mo | +7 mo |

## The path with no pacing: ideas and transfer +3, metrics +0.5

| Date | Pace | Pace as measured | Experiments at scale | Candidates behind each | Share of experiments people judge | Share of a gain the AI keeps | AI ideas | AI transfer judgment | AI metric judgment |
|---|---|---|---|---|---|---|---|---|---|
| Jan 2027 | 1.8x | 2.5x | 10.1x | 1,391 | 9% | 3% | -2.6 SD | -2.6 SD | -3.3 SD |
| Jul 2027 | 1.9x | 4.6x | 15.3x | 10,000 | 4% | 11% | +0.1 SD | +0.1 SD | -2.9 SD |
| Jan 2028 | 2.3x | 1.7x | 4.0x | 125 | 32% | 21% | +3.6 SD | +3.6 SD | -2.3 SD |
| Jul 2028 | 2.5x | 5.4x | 15.8x | 10,000 | 4% | 32% | +7.1 SD | +7.1 SD | -1.7 SD |

## Each input moved: ideas and transfer +3, metrics +0.5

| Case | Researcher-level AI | TED-AI | Audits delay TED-AI | 9-month lag delays TED-AI |
|---|---|---|---|---|
| Central | Aug 2028 | Dec 2028 | +12 mo | +11 mo |
| Experiments from unlimited AI labor: 5 times | Nov 2028 | Mar 2029 | +10 mo | +11 mo |
| Experiments from unlimited AI labor: 60 times | Jan 2028 | Mar 2028 | +13 mo | +12 mo |
| Validity with the AI judging today: 0.3 | Sep 2027 | Dec 2027 | +8 mo | +12 mo |
| Validity with the AI judging today: 0.01 | Mar 2029 | Jul 2029 | +11 mo | +10 mo |
| Transfer with the AI judging today: 0.4 | Aug 2028 | Dec 2028 | +12 mo | +11 mo |
| AI never judges better than people | Feb 2029 | Jun 2029 | +14 mo | +10 mo |
| People can vouch for any gain | Mar 2028 | Apr 2028 | +1 mo | +15 mo |
| Audits take hours only: any change passes once understood | Aug 2028 | Dec 2028 | +2 mo | +11 mo |
| People can vouch for gains up to +1 SD ideas | Nov 2028 | Feb 2029 | +16 mo | +11 mo |
| Judging time per experiment grows with candidates, elasticity 0.25 | Sep 2028 | Jan 2029 | +12 mo | +11 mo |
| 60% of researcher time was already on judging | Oct 2028 | Jan 2029 | +12 mo | +11 mo |
| No researcher time goes to managing agents | Jul 2028 | Nov 2028 | +11 mo | +11 mo |
| A third of researcher time goes to managing agents | Sep 2028 | Jan 2029 | +12 mo | +11 mo |
| Ideas improve +2.1 SD a year | Mar 2029 | Jun 2029 | +11 mo | +11 mo |
| Selection worth twice as much | Jul 2028 | Oct 2028 | +14 mo | +11 mo |
| Up to a million candidates behind each experiment | Sep 2028 | Dec 2028 | +11 mo | +11 mo |
| Compute grows at half the historical rate from 2029 | Aug 2028 | Dec 2028 | +14 mo | +12 mo |
| Understanding all deployed changes takes twice the time | Aug 2028 | Dec 2028 | +13 mo | +11 mo |
| Audit time counts in full as judging | Aug 2028 | Dec 2028 | +11 mo | +11 mo |
| Audit time does not count as judging | Aug 2028 | Dec 2028 | +13 mo | +11 mo |
| Deployed changes do not grow with AI labor | Aug 2028 | Dec 2028 | +10 mo | +11 mo |

## By how fast research gets harder

The three fitted inputs are refitted at each difficulty. The most the AI's judgment can keep of a gain is 153% of what people's keeps.

| Halvings of what research buys per year of software progress | Share of a gain the AI must keep for the loop to run away | TED-AI, all judgment +3 SD | TED-AI, ideas and transfer +3 and metrics +0.5 | Audits delay it |
|---|---|---|---|---|
| 0.5 | 39% | Apr 2027 | Apr 2028 | +8 mo |
| 1 | 78% | May 2027 | Dec 2028 | +12 mo |
| 1.5 | 117% | Jun 2027 | Jun 2029 | +12 mo |
| 2 | 156% | Aug 2027 | Nov 2029 | +11 mo |

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

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | May 2027 |  | May 2027 |  |
| Comprehension audits | May 2027 | +0 mo | Jun 2027 | +1 mo |
| Internal-use lag, 3 months | Sep 2027 | +4 mo | Nov 2027 | +5 mo |
| Internal-use lag, 9 months | Jan 2028 | +8 mo | Apr 2028 | +11 mo |
| R&D compute at a third of baseline | Sep 2027 | +4 mo | Sep 2027 | +4 mo |
| Comprehension audits + 9-month lag | Jan 2028 | +8 mo | May 2028 | +12 mo |

### Ideas and transfer +3, metrics +1

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Dec 2027 |  | Jan 2028 |  |
| Comprehension audits | Feb 2028 | +2 mo | Apr 2028 | +4 mo |
| Internal-use lag, 3 months | Mar 2028 | +4 mo | Jun 2028 | +5 mo |
| Internal-use lag, 9 months | Jul 2028 | +7 mo | Nov 2028 | +10 mo |
| R&D compute at a third of baseline | Jun 2028 | +6 mo | Jul 2028 | +6 mo |
| Comprehension audits + 9-month lag | Aug 2028 | +8 mo | Dec 2028 | +11 mo |

### Ideas and transfer +3, metrics +0.5

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Aug 2028 |  | Dec 2028 |  |
| Comprehension audits | Dec 2028 | +4 mo | Dec 2029 | +12 mo |
| Internal-use lag, 3 months | Nov 2028 | +3 mo | May 2029 | +5 mo |
| Internal-use lag, 9 months | Mar 2029 | +7 mo | Nov 2029 | +11 mo |
| R&D compute at a third of baseline | Feb 2029 | +6 mo | Jun 2029 | +6 mo |
| Comprehension audits + 9-month lag | Apr 2029 | +8 mo | Mar 2030 | +15 mo |

### Ideas +3, transfer and metrics +1

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | May 2028 |  | May 2028 |  |
| Comprehension audits | Aug 2028 | +3 mo | Sep 2028 | +4 mo |
| Internal-use lag, 3 months | Jul 2028 | +3 mo | Oct 2028 | +5 mo |
| Internal-use lag, 9 months | Oct 2028 | +6 mo | Feb 2029 | +9 mo |
| R&D compute at a third of baseline | Nov 2028 | +7 mo | Dec 2028 | +7 mo |
| Comprehension audits + 9-month lag | Dec 2028 | +7 mo | Apr 2029 | +11 mo |

### Ideas +3, transfer +1, metrics +0.5

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Jan 2029 |  | Apr 2029 |  |
| Comprehension audits | Jun 2029 | +5 mo | Feb 2030 | +11 mo |
| Internal-use lag, 3 months | Apr 2029 | +3 mo | Sep 2029 | +5 mo |
| Internal-use lag, 9 months | Jul 2029 | +6 mo | Mar 2030 | +11 mo |
| R&D compute at a third of baseline | Aug 2029 | +7 mo | Nov 2029 | +7 mo |
| Comprehension audits + 9-month lag | Sep 2029 | +8 mo | Jul 2030 | +16 mo |

### Ideas +3, transfer and metrics +0.5

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Sep 2029 |  | Jan 2030 |  |
| Comprehension audits | Apr 2030 | +7 mo | Jan 2031 | +13 mo |
| Internal-use lag, 3 months | Nov 2029 | +2 mo | May 2030 | +5 mo |
| Internal-use lag, 9 months | Feb 2030 | +5 mo | Oct 2030 | +10 mo |
| R&D compute at a third of baseline | Apr 2030 | +7 mo | Aug 2030 | +7 mo |
| Comprehension audits + 9-month lag | May 2030 | +8 mo | Apr 2031 | +16 mo |

