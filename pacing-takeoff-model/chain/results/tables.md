# Chain model: milestone dates by scenario

Written by `chain_model.py`. Do not edit by hand.

Delays are against no pacing. Pacing starts Jan 1, 2027. Rates are SD of researcher judgment gained per year of progress. The loop runs away on better ideas alone once the AI's own judgment keeps 78% of the share of a gain that people's judgment keeps.

Researcher-level AI and TED-AI are the dates an AI-only lab's research matches a lab of researchers at AI Futures' two levels, +3.09 and +7.72 SD. `over` means the run had ended by then.

## No pacing

| AI judgment gained per year of progress | Researcher-level AI | TED-AI | Pace in Jan 2028 | As measured |
|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | May 2027 | May 2027 | over | over |
| Ideas and transfer +3, metrics +1 | Dec 2027 | Jan 2028 | 58.8x | 14.8x |
| Ideas and transfer +3, metrics +0.5 | Aug 2028 | Dec 2028 | 2.3x | 5.0x |
| Ideas +3, transfer and metrics +1 | May 2028 | May 2028 | 2.0x | 2.9x |
| Ideas +3, transfer +1, metrics +0.5 | Jan 2029 | Apr 2029 | 1.7x | 2.7x |
| Ideas +3, transfer and metrics +0.5 | Sep 2029 | Jan 2030 | 1.6x | 2.1x |

## Delay to TED-AI

| AI judgment gained per year | TED-AI, no pacing | Central audits | Strict audits | 9-month lag | Compute at a third of baseline |
|---|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | May 2027 | +2 mo | +3 mo | +11 mo | +4 mo |
| Ideas and transfer +3, metrics +1 | Jan 2028 | +11 mo | +14 mo | +10 mo | +6 mo |
| Ideas and transfer +3, metrics +0.5 | Dec 2028 | +35 mo | +39 mo | +11 mo | +6 mo |
| Ideas +3, transfer and metrics +1 | May 2028 | +15 mo | +18 mo | +9 mo | +7 mo |
| Ideas +3, transfer +1, metrics +0.5 | Apr 2029 | +34 mo | +38 mo | +11 mo | +7 mo |
| Ideas +3, transfer and metrics +0.5 | Jan 2030 | +45 mo | +49 mo | +10 mo | +7 mo |

## The path with no pacing: ideas +3, transfer +1, metrics +0.5

| Date | Pace | Pace as measured | Experiments at scale | Candidates behind each | Share of experiments people judge | Share of a gain the AI keeps | AI ideas | AI transfer judgment | AI metric judgment |
|---|---|---|---|---|---|---|---|---|---|
| Jan 2027 | 1.8x | 2.3x | 10.1x | 1,389 | 9% | 2% | -2.6 SD | -3.2 SD | -3.3 SD |
| Jul 2027 | 1.7x | 2.2x | 15.2x | 10,000 | 4% | 4% | +0.1 SD | -2.3 SD | -2.9 SD |
| Jan 2028 | 1.7x | 2.7x | 15.7x | 10,000 | 4% | 8% | +2.6 SD | -1.5 SD | -2.5 SD |
| Jul 2028 | 1.7x | 3.7x | 15.8x | 10,000 | 4% | 15% | +5.1 SD | -0.6 SD | -2.1 SD |
| Jan 2029 | 2.8x | 7.9x | 15.8x | 10,000 | 4% | 32% | +8.0 SD | +0.3 SD | -1.6 SD |

## Each input moved: ideas +3, transfer +1, metrics +0.5

| Case | Researcher-level AI | TED-AI | Central audits delay TED-AI | 9-month lag delays TED-AI |
|---|---|---|---|---|
| Central | Jan 2029 | Apr 2029 | +34 mo | +11 mo |
| Experiments from unlimited AI labor: 5 times | Jul 2029 | Oct 2029 | +36 mo | +11 mo |
| Experiments from unlimited AI labor: 60 times | Apr 2028 | Jun 2028 | +31 mo | +12 mo |
| Validity with the AI judging today: 0.3 | Apr 2028 | Jun 2028 | +20 mo | +11 mo |
| Validity with the AI judging today: 0.01 | Jul 2029 | Oct 2029 | +42 mo | +10 mo |
| Transfer with the AI judging today: 0.4 | Feb 2029 | Apr 2029 | +35 mo | +11 mo |
| AI never judges better than people | Mar 2029 | Jul 2029 | +40 mo | +11 mo |
| People can vouch for any gain | Sep 2028 | Oct 2028 | +31 mo | +14 mo |
| People can vouch for gains up to +1 SD ideas | Mar 2029 | May 2029 | +34 mo | +11 mo |
| Judging time per experiment grows with candidates, elasticity 0.25 | Feb 2029 | May 2029 | +34 mo | +11 mo |
| 60% of researcher time was already on judging | Feb 2029 | May 2029 | +34 mo | +11 mo |
| No researcher time goes to managing agents | Dec 2028 | Mar 2029 | +33 mo | +11 mo |
| A third of researcher time goes to managing agents | Feb 2029 | Apr 2029 | +35 mo | +11 mo |
| Ideas improve +2.1 SD a year | Jun 2029 | Sep 2029 | +43 mo | +12 mo |
| Selection worth twice as much | Dec 2028 | Feb 2029 | +33 mo | +11 mo |
| Up to a million candidates behind each experiment | Feb 2029 | May 2029 | +33 mo | +11 mo |
| Compute grows at half the historical rate from 2029 | Jan 2029 | Apr 2029 | +45 mo | +13 mo |
| Audit time counts in full as judging | Jan 2029 | Apr 2029 | +33 mo | +11 mo |
| Audit time does not count as judging | Jan 2029 | Apr 2029 | +36 mo | +11 mo |
| Deployed changes do not grow with AI labor | Jan 2029 | Apr 2029 | +0 mo | +11 mo |

## By how fast research gets harder

The three fitted inputs are refitted at each difficulty. The most the AI's judgment can keep of a gain is 153% of what people's keeps.

| Halvings of what research buys per year of software progress | Share of a gain the AI must keep for the loop to run away | TED-AI, all judgment +3 SD | TED-AI, transfer +1 and metrics +0.5 | Central audits delay it |
|---|---|---|---|---|
| 0.5 | 39% | Apr 2027 | Aug 2028 | +39 mo |
| 1 | 78% | May 2027 | Apr 2029 | +34 mo |
| 1.5 | 117% | Jun 2027 | Sep 2029 | +29 mo |
| 2 | 156% | Aug 2027 | Jan 2030 | +25 mo |

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
| Comprehension audits, light | May 2027 | +0 mo | Jun 2027 | +1 mo |
| Comprehension audits, central | Jun 2027 | +1 mo | Jul 2027 | +2 mo |
| Comprehension audits, strict | Jul 2027 | +2 mo | Aug 2027 | +3 mo |
| Internal-use lag, 3 months | Sep 2027 | +4 mo | Nov 2027 | +5 mo |
| Internal-use lag, 9 months | Jan 2028 | +8 mo | Apr 2028 | +11 mo |
| R&D compute at a third of baseline | Sep 2027 | +4 mo | Sep 2027 | +4 mo |
| Comprehension audits (central) + 9-month lag | Jan 2028 | +8 mo | May 2028 | +12 mo |

### Ideas and transfer +3, metrics +1

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Dec 2027 |  | Jan 2028 |  |
| Comprehension audits, light | Jul 2028 | +7 mo | Sep 2028 | +9 mo |
| Comprehension audits, central | Sep 2028 | +9 mo | Dec 2028 | +11 mo |
| Comprehension audits, strict | Dec 2028 | +12 mo | Mar 2029 | +14 mo |
| Internal-use lag, 3 months | Mar 2028 | +4 mo | Jun 2028 | +5 mo |
| Internal-use lag, 9 months | Jul 2028 | +7 mo | Nov 2028 | +10 mo |
| R&D compute at a third of baseline | Jun 2028 | +6 mo | Jul 2028 | +6 mo |
| Comprehension audits (central) + 9-month lag | Oct 2028 | +10 mo | May 2029 | +17 mo |

### Ideas and transfer +3, metrics +0.5

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Aug 2028 |  | Dec 2028 |  |
| Comprehension audits, light | May 2030 | +21 mo | Aug 2031 | +32 mo |
| Comprehension audits, central | Sep 2030 | +24 mo | Nov 2031 | +35 mo |
| Comprehension audits, strict | Dec 2030 | +28 mo | Mar 2032 | +39 mo |
| Internal-use lag, 3 months | Nov 2028 | +3 mo | May 2029 | +5 mo |
| Internal-use lag, 9 months | Mar 2029 | +7 mo | Nov 2029 | +11 mo |
| R&D compute at a third of baseline | Feb 2029 | +6 mo | Jun 2029 | +6 mo |
| Comprehension audits (central) + 9-month lag | Jun 2030 | +22 mo | Jan 2032 | +37 mo |

### Ideas +3, transfer and metrics +1

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | May 2028 |  | May 2028 |  |
| Comprehension audits, light | Mar 2029 | +11 mo | May 2029 | +12 mo |
| Comprehension audits, central | Jun 2029 | +13 mo | Aug 2029 | +15 mo |
| Comprehension audits, strict | Sep 2029 | +16 mo | Nov 2029 | +18 mo |
| Internal-use lag, 3 months | Jul 2028 | +3 mo | Oct 2028 | +5 mo |
| Internal-use lag, 9 months | Oct 2028 | +6 mo | Feb 2029 | +9 mo |
| R&D compute at a third of baseline | Nov 2028 | +7 mo | Dec 2028 | +7 mo |
| Comprehension audits (central) + 9-month lag | May 2029 | +12 mo | Dec 2029 | +19 mo |

### Ideas +3, transfer +1, metrics +0.5

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Jan 2029 |  | Apr 2029 |  |
| Comprehension audits, light | Nov 2030 | +22 mo | Oct 2031 | +31 mo |
| Comprehension audits, central | Mar 2031 | +25 mo | Feb 2032 | +34 mo |
| Comprehension audits, strict | Jun 2031 | +29 mo | May 2032 | +38 mo |
| Internal-use lag, 3 months | Apr 2029 | +3 mo | Sep 2029 | +5 mo |
| Internal-use lag, 9 months | Jul 2029 | +6 mo | Mar 2030 | +11 mo |
| R&D compute at a third of baseline | Aug 2029 | +7 mo | Nov 2029 | +7 mo |
| Comprehension audits (central) + 9-month lag | Jan 2031 | +23 mo | Apr 2032 | +37 mo |

### Ideas +3, transfer and metrics +0.5

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Sep 2029 |  | Jan 2030 |  |
| Comprehension audits, light | Jun 2032 | +32 mo | Jun 2033 | +42 mo |
| Comprehension audits, central | Sep 2032 | +36 mo | Oct 2033 | +45 mo |
| Comprehension audits, strict | Dec 2032 | +39 mo | Jan 2034 | +49 mo |
| Internal-use lag, 3 months | Nov 2029 | +2 mo | May 2030 | +5 mo |
| Internal-use lag, 9 months | Feb 2030 | +5 mo | Oct 2030 | +10 mo |
| R&D compute at a third of baseline | Apr 2030 | +7 mo | Aug 2030 | +7 mo |
| Comprehension audits (central) + 9-month lag | Jun 2032 | +33 mo | Nov 2033 | +47 mo |

