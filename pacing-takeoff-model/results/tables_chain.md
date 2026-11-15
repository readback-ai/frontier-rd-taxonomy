# Chain model: milestone dates by scenario

Written by `chain_model.py`. Do not edit by hand.

Delays are against no pacing. Pacing starts Jan 1, 2027. Rates are SD of researcher judgment gained per year of progress. The loop runs away on better ideas alone once the AI's own judgment keeps 78% of the share of a gain that people's judgment keeps.

## No pacing

Researcher-level AI and TED-AI are the dates an AI-only lab's research matches a lab of researchers at AI Futures' two levels, +3.09 and +7.72 SD. The third date is when the AI's weakest kind of judgment passes the best researcher's. `over` means the run had ended by then.

| AI judgment gained per year of progress | Researcher-level AI | TED-AI | AI passes the best researcher on every kind of judgment | Pace in Jan 2028 | As measured |
|---|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | May 2027 | Jun 2027 | May 2027 | over | over |
| Ideas and transfer +3, metrics +1 | Jul 2027 | Aug 2027 | Aug 2027 | over | over |
| Ideas and transfer +3, metrics +0.5 | Aug 2027 | Oct 2027 | Nov 2027 | over | over |
| Ideas +3, transfer and metrics +1 | Nov 2027 | Dec 2027 | Dec 2027 | over | over |
| Ideas +3, transfer +1, metrics +0.5 | Jan 2028 | Mar 2028 | Mar 2028 | 4.4x | 6.7x |
| Ideas +3, transfer and metrics +0.5 | Apr 2028 | Aug 2028 | Sep 2028 | 2.8x | 3.5x |

## Dates by scenario

### Ideas, transfer and metrics all +3 SD a year

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | May 2027 |  | Jun 2027 |  |
| Comprehension audits, light | May 2027 | +0 mo | Jun 2027 | +0 mo |
| Comprehension audits, central | Jun 2027 | +0 mo | Jun 2027 | +0 mo |
| Comprehension audits, strict | Jun 2027 | +1 mo | Jun 2027 | +1 mo |
| Internal-use lag, 3 months | Sep 2027 | +4 mo | Nov 2027 | +6 mo |
| Internal-use lag, 9 months | Dec 2027 | +7 mo | May 2028 | +11 mo |
| R&D compute cut 3x | Jul 2027 | +1 mo | Jul 2027 | +2 mo |
| Comprehension audits (central) + 9-month lag | Jan 2028 | +7 mo | May 2028 | +12 mo |

### Ideas and transfer +3, metrics +1

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Jul 2027 |  | Aug 2027 |  |
| Comprehension audits, light | Aug 2027 | +0 mo | Sep 2027 | +1 mo |
| Comprehension audits, central | Aug 2027 | +1 mo | Sep 2027 | +1 mo |
| Comprehension audits, strict | Sep 2027 | +2 mo | Nov 2027 | +3 mo |
| Internal-use lag, 3 months | Nov 2027 | +4 mo | Feb 2028 | +6 mo |
| Internal-use lag, 9 months | Mar 2028 | +8 mo | Aug 2028 | +12 mo |
| R&D compute cut 3x | Sep 2027 | +1 mo | Oct 2027 | +2 mo |
| Comprehension audits (central) + 9-month lag | Apr 2028 | +8 mo | Aug 2028 | +13 mo |

### Ideas and transfer +3, metrics +0.5

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Aug 2027 |  | Oct 2027 |  |
| Comprehension audits, light | Sep 2027 | +1 mo | Dec 2027 | +3 mo |
| Comprehension audits, central | Oct 2027 | +2 mo | Feb 2028 | +4 mo |
| Comprehension audits, strict | Dec 2027 | +3 mo | Apr 2028 | +6 mo |
| Internal-use lag, 3 months | Jan 2028 | +4 mo | Apr 2028 | +6 mo |
| Internal-use lag, 9 months | May 2028 | +8 mo | Oct 2028 | +13 mo |
| R&D compute cut 3x | Oct 2027 | +1 mo | Dec 2027 | +2 mo |
| Comprehension audits (central) + 9-month lag | Jun 2028 | +9 mo | Dec 2028 | +14 mo |

### Ideas +3, transfer and metrics +1

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Nov 2027 |  | Dec 2027 |  |
| Comprehension audits, light | Dec 2027 | +1 mo | Feb 2028 | +2 mo |
| Comprehension audits, central | Jan 2028 | +3 mo | Apr 2028 | +4 mo |
| Comprehension audits, strict | Mar 2028 | +5 mo | Jun 2028 | +6 mo |
| Internal-use lag, 3 months | Feb 2028 | +4 mo | Jun 2028 | +6 mo |
| Internal-use lag, 9 months | Jun 2028 | +7 mo | Nov 2028 | +11 mo |
| R&D compute cut 3x | Jan 2028 | +2 mo | Feb 2028 | +2 mo |
| Comprehension audits (central) + 9-month lag | Jul 2028 | +8 mo | Jan 2029 | +13 mo |

### Ideas +3, transfer +1, metrics +0.5

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Jan 2028 |  | Mar 2028 |  |
| Comprehension audits, light | Mar 2028 | +2 mo | Jul 2028 | +5 mo |
| Comprehension audits, central | May 2028 | +4 mo | Oct 2028 | +7 mo |
| Comprehension audits, strict | Jul 2028 | +6 mo | Dec 2028 | +10 mo |
| Internal-use lag, 3 months | Apr 2028 | +4 mo | Sep 2028 | +6 mo |
| Internal-use lag, 9 months | Aug 2028 | +8 mo | Mar 2029 | +12 mo |
| R&D compute cut 3x | Feb 2028 | +2 mo | May 2028 | +2 mo |
| Comprehension audits (central) + 9-month lag | Oct 2028 | +9 mo | Jun 2029 | +16 mo |

### Ideas +3, transfer and metrics +0.5

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Apr 2028 |  | Aug 2028 |  |
| Comprehension audits, light | Sep 2028 | +5 mo | Jul 2029 | +11 mo |
| Comprehension audits, central | Dec 2028 | +8 mo | Oct 2029 | +14 mo |
| Comprehension audits, strict | Feb 2029 | +10 mo | Jan 2030 | +17 mo |
| Internal-use lag, 3 months | Jul 2028 | +3 mo | Feb 2029 | +6 mo |
| Internal-use lag, 9 months | Nov 2028 | +7 mo | Aug 2029 | +12 mo |
| R&D compute cut 3x | Jun 2028 | +2 mo | Oct 2028 | +2 mo |
| Comprehension audits (central) + 9-month lag | Feb 2029 | +10 mo | Apr 2030 | +19 mo |

## The path with no pacing: ideas +3, transfer +1, metrics +0.5

| Date | Pace | Pace as measured | Experiments at scale | Candidates behind each | Share of experiments people judge | Share of a gain the AI keeps | AI ideas | AI transfer judgment | AI metric judgment |
|---|---|---|---|---|---|---|---|---|---|
| Jan 2027 | 1.8x | 1.9x | 4.5x | 158 | 51% | 14% | -2.6 SD | -3.2 SD | -3.3 SD |
| Jul 2027 | 2.3x | 2.7x | 10.9x | 2,350 | 22% | 27% | +0.4 SD | -2.2 SD | -2.8 SD |
| Jan 2028 | 4.4x | 6.7x | 14.9x | 10,000 | 16% | 56% | +5.2 SD | -0.6 SD | -2.0 SD |

## Each input moved: ideas +3, transfer +1, metrics +0.5

| Case | Researcher-level AI | TED-AI | AI passes the best researcher on every kind of judgment | Central audits delay TED-AI | 9-month lag delays TED-AI |
|---|---|---|---|---|---|
| Central | Jan 2028 | Mar 2028 | Mar 2028 | +7 mo | +12 mo |
| Half of transfer and metric judgment comes with calendar time | Mar 2028 | Jul 2028 | Sep 2028 | +9 mo | +10 mo |
| All of transfer and metric judgment comes with calendar time | Aug 2028 | May 2029 | Jan 2040 | +8 mo | +6 mo |
| Experiments from unlimited AI labor: 5 times | Mar 2028 | Jun 2028 | Jul 2028 | +10 mo | +11 mo |
| Experiments from unlimited AI labor: 60 times | Oct 2027 | Nov 2027 | Nov 2027 | +4 mo | +14 mo |
| AI keeps 2% of a gain today (transfer 0.1, validity 0.1) | Mar 2028 | May 2028 | May 2028 | +9 mo | +12 mo |
| AI keeps 36% of a gain today (transfer 0.4, validity 0.5) | Nov 2027 | Jan 2028 | Jan 2028 | +5 mo | +12 mo |
| AI never judges better than people | Jan 2028 | Mar 2028 | May 2028 | +8 mo | +13 mo |
| People can vouch for any gain | Dec 2027 | Feb 2028 | Feb 2028 | +7 mo | +13 mo |
| People can vouch for gains up to +1 SD ideas | Feb 2028 | Apr 2028 | Apr 2028 | +7 mo | +12 mo |
| Judging time per experiment grows with candidates, elasticity 0.25 | Apr 2028 | Jun 2028 | Jun 2028 | +6 mo | +12 mo |
| 60% of researcher time was already on judging | Feb 2028 | Apr 2028 | May 2028 | +7 mo | +13 mo |
| Ideas improve +2.1 SD a year | May 2028 | Aug 2028 | Sep 2028 | +11 mo | +13 mo |
| Selection worth twice as much | Nov 2027 | Dec 2027 | Jan 2028 | +7 mo | +12 mo |
| Up to a million candidates behind each experiment | Dec 2027 | Feb 2028 | Mar 2028 | +7 mo | +12 mo |
| Compute grows at half the historical rate from 2029 | Jan 2028 | Mar 2028 | Mar 2028 | +7 mo | +12 mo |
| Audit time counts in full as judging | Jan 2028 | Mar 2028 | Mar 2028 | +5 mo | +12 mo |
| Audit time does not count as judging | Jan 2028 | Mar 2028 | Mar 2028 | +9 mo | +12 mo |
| Deployed changes do not grow with AI labor | Jan 2028 | Mar 2028 | Mar 2028 | +0 mo | +12 mo |

