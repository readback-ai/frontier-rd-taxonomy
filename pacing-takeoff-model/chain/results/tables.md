# Chain model: milestone dates by scenario

Written by `chain_model.py`. Do not edit by hand.

Delays are against no pacing. Pacing starts Jan 1, 2027. Rates are SD of researcher judgment gained per year of progress. The loop runs away on better ideas alone once the AI's own judgment keeps 78% of the share of a gain that people's judgment keeps.

Researcher-level AI and TED-AI are the dates an AI-only lab's research matches a lab of researchers at AI Futures' two levels, +3.09 and +7.72 SD. `over` means the run had ended by then.

## No pacing

| AI judgment gained per year of progress | Researcher-level AI | TED-AI | Pace in Jan 2028 | As measured |
|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | Jun 2027 | Jun 2027 | over | over |
| Ideas and transfer +3, metrics +1 | Oct 2027 | Nov 2027 | over | over |
| Ideas and transfer +3, metrics +0.5 | Mar 2028 | Jun 2028 | 3.3x | 7.1x |
| Ideas +3, transfer and metrics +1 | Feb 2028 | Mar 2028 | 3.1x | 4.5x |
| Ideas +3, transfer +1, metrics +0.5 | Aug 2028 | Nov 2028 | 2.2x | 4.0x |
| Ideas +3, transfer and metrics +0.5 | Mar 2029 | Jul 2029 | 2.1x | 2.9x |

## Delay to TED-AI

| AI judgment gained per year | TED-AI, no pacing | Central audits | Strict audits | 9-month lag | Compute at a third of baseline |
|---|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | Jun 2027 | +0 mo | +1 mo | +11 mo | +5 mo |
| Ideas and transfer +3, metrics +1 | Nov 2027 | +4 mo | +6 mo | +11 mo | +5 mo |
| Ideas and transfer +3, metrics +0.5 | Jun 2028 | +16 mo | +19 mo | +12 mo | +5 mo |
| Ideas +3, transfer and metrics +1 | Mar 2028 | +6 mo | +8 mo | +10 mo | +6 mo |
| Ideas +3, transfer +1, metrics +0.5 | Nov 2028 | +16 mo | +19 mo | +12 mo | +6 mo |
| Ideas +3, transfer and metrics +0.5 | Jul 2029 | +23 mo | +26 mo | +10 mo | +6 mo |

## The path with no pacing: ideas +3, transfer +1, metrics +0.5

| Date | Pace | Pace as measured | Experiments at scale | Candidates behind each | Share of experiments people judge | Share of a gain the AI keeps | AI ideas | AI transfer judgment | AI metric judgment |
|---|---|---|---|---|---|---|---|---|---|
| Jan 2027 | 1.8x | 1.9x | 4.5x | 157 | 51% | 2% | -2.6 SD | -3.2 SD | -3.4 SD |
| Jul 2027 | 2.1x | 2.5x | 10.7x | 2,046 | 23% | 5% | +0.3 SD | -2.2 SD | -2.9 SD |
| Jan 2028 | 2.2x | 4.0x | 14.5x | 10,000 | 17% | 11% | +3.9 SD | -1.0 SD | -2.3 SD |
| Jul 2028 | 2.4x | 6.4x | 15.2x | 10,000 | 16% | 26% | +7.1 SD | +0.0 SD | -1.7 SD |

## Each input moved: ideas +3, transfer +1, metrics +0.5

| Case | Researcher-level AI | TED-AI | Central audits delay TED-AI | 9-month lag delays TED-AI |
|---|---|---|---|---|
| Central | Aug 2028 | Nov 2028 | +16 mo | +12 mo |
| Experiments from unlimited AI labor: 5 times | Oct 2028 | Jan 2029 | +18 mo | +12 mo |
| Experiments from unlimited AI labor: 60 times | Apr 2028 | Jun 2028 | +12 mo | +14 mo |
| Validity with the AI judging today: 0.3 | Feb 2028 | Apr 2028 | +8 mo | +11 mo |
| Validity with the AI judging today: 0.01 | Jan 2029 | Mar 2029 | +21 mo | +11 mo |
| Transfer with the AI judging today: 0.4 | Sep 2028 | Nov 2028 | +16 mo | +12 mo |
| AI never judges better than people | Oct 2028 | Feb 2029 | +19 mo | +11 mo |
| People can vouch for any gain | Mar 2028 | Apr 2028 | +11 mo | +16 mo |
| People can vouch for gains up to +1 SD ideas | Dec 2028 | Feb 2029 | +15 mo | +11 mo |
| Judging time per experiment grows with candidates, elasticity 0.25 | Mar 2029 | May 2029 | +14 mo | +12 mo |
| 60% of researcher time was already on judging | Nov 2028 | Jan 2029 | +15 mo | +13 mo |
| Ideas improve +2.1 SD a year | Jan 2029 | Apr 2029 | +21 mo | +12 mo |
| Selection worth twice as much | Jul 2028 | Sep 2028 | +15 mo | +12 mo |
| Up to a million candidates behind each experiment | Aug 2028 | Oct 2028 | +15 mo | +13 mo |
| Compute grows at half the historical rate from 2029 | Aug 2028 | Nov 2028 | +18 mo | +13 mo |
| Audit time counts in full as judging | Aug 2028 | Nov 2028 | +12 mo | +12 mo |
| Audit time does not count as judging | Aug 2028 | Nov 2028 | +19 mo | +12 mo |
| Deployed changes do not grow with AI labor | Aug 2028 | Nov 2028 | +0 mo | +12 mo |

## By how fast research gets harder

The three fitted inputs are refitted at each difficulty. The most the AI's judgment can keep of a gain is 153% of what people's keeps.

| Halvings of what research buys per year of software progress | Share of a gain the AI must keep for the loop to run away | TED-AI, all judgment +3 SD | TED-AI, transfer +1 and metrics +0.5 | Central audits delay it |
|---|---|---|---|---|
| 0.25 | 19% | May 2027 | Mar 2028 | +15 mo |
| 0.5 | 39% | May 2027 | Jun 2028 | +16 mo |
| 0.75 | 58% | May 2027 | Aug 2028 | +16 mo |
| 1 | 78% | Jun 2027 | Nov 2028 | +16 mo |

Above a difficulty of about 1 the model cannot reach the pace measured in November 2026. The table below gives the highest difficulty that still fits, computed by `max_difficulty`, and how it moves with the inputs it rests on.

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

## Every scenario

### Ideas, transfer and metrics all +3 SD a year

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Jun 2027 |  | Jun 2027 |  |
| Comprehension audits, light | Jun 2027 | +0 mo | Jun 2027 | +0 mo |
| Comprehension audits, central | Jun 2027 | +0 mo | Jun 2027 | +0 mo |
| Comprehension audits, strict | Jul 2027 | +1 mo | Jul 2027 | +1 mo |
| Internal-use lag, 3 months | Oct 2027 | +4 mo | Nov 2027 | +5 mo |
| Internal-use lag, 9 months | Jan 2028 | +7 mo | May 2028 | +11 mo |
| R&D compute at a third of baseline | Oct 2027 | +4 mo | Oct 2027 | +5 mo |
| Comprehension audits (central) + 9-month lag | Jan 2028 | +8 mo | May 2028 | +12 mo |

### Ideas and transfer +3, metrics +1

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Oct 2027 |  | Nov 2027 |  |
| Comprehension audits, light | Dec 2027 | +2 mo | Jan 2028 | +2 mo |
| Comprehension audits, central | Jan 2028 | +3 mo | Feb 2028 | +4 mo |
| Comprehension audits, strict | Mar 2028 | +5 mo | Apr 2028 | +6 mo |
| Internal-use lag, 3 months | Feb 2028 | +4 mo | Apr 2028 | +6 mo |
| Internal-use lag, 9 months | Jun 2028 | +8 mo | Sep 2028 | +11 mo |
| R&D compute at a third of baseline | Mar 2028 | +5 mo | Apr 2028 | +5 mo |
| Comprehension audits (central) + 9-month lag | Jul 2028 | +10 mo | Nov 2028 | +13 mo |

### Ideas and transfer +3, metrics +0.5

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Mar 2028 |  | Jun 2028 |  |
| Comprehension audits, light | Nov 2028 | +8 mo | Aug 2029 | +13 mo |
| Comprehension audits, central | Jan 2029 | +10 mo | Nov 2029 | +16 mo |
| Comprehension audits, strict | Apr 2029 | +13 mo | Feb 2030 | +19 mo |
| Internal-use lag, 3 months | Jul 2028 | +4 mo | Dec 2028 | +6 mo |
| Internal-use lag, 9 months | Dec 2028 | +9 mo | Jul 2029 | +12 mo |
| R&D compute at a third of baseline | Aug 2028 | +5 mo | Dec 2028 | +5 mo |
| Comprehension audits (central) + 9-month lag | Apr 2029 | +12 mo | Apr 2030 | +21 mo |

### Ideas +3, transfer and metrics +1

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Feb 2028 |  | Mar 2028 |  |
| Comprehension audits, light | May 2028 | +3 mo | Jun 2028 | +4 mo |
| Comprehension audits, central | Jul 2028 | +5 mo | Aug 2028 | +6 mo |
| Comprehension audits, strict | Sep 2028 | +8 mo | Nov 2028 | +8 mo |
| Internal-use lag, 3 months | May 2028 | +3 mo | Aug 2028 | +5 mo |
| Internal-use lag, 9 months | Sep 2028 | +7 mo | Dec 2028 | +10 mo |
| R&D compute at a third of baseline | Aug 2028 | +6 mo | Aug 2028 | +6 mo |
| Comprehension audits (central) + 9-month lag | Nov 2028 | +9 mo | Mar 2029 | +13 mo |

### Ideas +3, transfer +1, metrics +0.5

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Aug 2028 |  | Nov 2028 |  |
| Comprehension audits, light | May 2029 | +9 mo | Nov 2029 | +13 mo |
| Comprehension audits, central | Aug 2029 | +12 mo | Feb 2030 | +16 mo |
| Comprehension audits, strict | Nov 2029 | +15 mo | May 2030 | +19 mo |
| Internal-use lag, 3 months | Dec 2028 | +3 mo | Apr 2029 | +6 mo |
| Internal-use lag, 9 months | Mar 2029 | +7 mo | Nov 2029 | +12 mo |
| R&D compute at a third of baseline | Feb 2029 | +6 mo | Apr 2029 | +6 mo |
| Comprehension audits (central) + 9-month lag | Sep 2029 | +13 mo | Aug 2030 | +22 mo |

### Ideas +3, transfer and metrics +0.5

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Mar 2029 |  | Jul 2029 |  |
| Comprehension audits, light | Jun 2030 | +15 mo | Feb 2031 | +19 mo |
| Comprehension audits, central | Sep 2030 | +18 mo | Jun 2031 | +23 mo |
| Comprehension audits, strict | Dec 2030 | +21 mo | Sep 2031 | +26 mo |
| Internal-use lag, 3 months | Jun 2029 | +2 mo | Dec 2029 | +5 mo |
| Internal-use lag, 9 months | Sep 2029 | +6 mo | May 2030 | +10 mo |
| R&D compute at a third of baseline | Sep 2029 | +6 mo | Feb 2030 | +6 mo |
| Comprehension audits (central) + 9-month lag | Sep 2030 | +17 mo | Oct 2031 | +27 mo |

