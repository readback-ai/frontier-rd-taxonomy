# Chain model: milestone dates by scenario

Written by `chain_model.py`. Do not edit by hand.

Delays are against no pacing. Pacing starts Jan 1, 2027. Rates are SD of researcher judgment. Ideas gain theirs per year of progress. Transfer and metric judgment gain theirs per year of progress in the first set of tables. In the second, metric judgment gains its rate per calendar year. In the third, both do. The loop runs away on better ideas alone once the AI's own judgment keeps 78% of the share of a gain that people's judgment keeps.

Researcher-level AI and TED-AI are the dates an AI-only lab's research matches a lab of researchers at AI Futures' two levels, +3.09 and +7.72 SD. The third date is when the AI's weakest kind of judgment passes the best researcher's. `over` means the run had ended by then.

## Transfer and metric judgment come with progress

### No pacing

| AI judgment gained per year of progress | Researcher-level AI | TED-AI | AI passes the best researcher on every kind of judgment | Pace in Jan 2028 | As measured |
|---|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | Jun 2027 | Jun 2027 | Jun 2027 | over | over |
| Ideas and transfer +3, metrics +1 | Oct 2027 | Nov 2027 | Nov 2027 | over | over |
| Ideas and transfer +3, metrics +0.5 | Mar 2028 | Jun 2028 | Jul 2028 | 3.3x | 7.1x |
| Ideas +3, transfer and metrics +1 | Feb 2028 | Mar 2028 | Mar 2028 | 3.1x | 4.5x |
| Ideas +3, transfer +1, metrics +0.5 | Aug 2028 | Nov 2028 | Nov 2028 | 2.2x | 4.0x |
| Ideas +3, transfer and metrics +0.5 | Mar 2029 | Jul 2029 | Aug 2029 | 2.1x | 2.9x |

### Delay to TED-AI

| AI judgment gained per year | TED-AI, no pacing | Central audits | Strict audits | 9-month lag | 3-fold compute cut |
|---|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | Jun 2027 | +0 mo | +1 mo | +11 mo | +1 mo |
| Ideas and transfer +3, metrics +1 | Nov 2027 | +4 mo | +6 mo | +11 mo | +1 mo |
| Ideas and transfer +3, metrics +0.5 | Jun 2028 | +16 mo | +19 mo | +12 mo | +1 mo |
| Ideas +3, transfer and metrics +1 | Mar 2028 | +6 mo | +8 mo | +10 mo | +2 mo |
| Ideas +3, transfer +1, metrics +0.5 | Nov 2028 | +16 mo | +19 mo | +12 mo | +2 mo |
| Ideas +3, transfer and metrics +0.5 | Jul 2029 | +23 mo | +26 mo | +10 mo | +2 mo |

### The path with no pacing: ideas +3, transfer +1, metrics +0.5

| Date | Pace | Pace as measured | Experiments at scale | Candidates behind each | Share of experiments people judge | Share of a gain the AI keeps | AI ideas | AI transfer judgment | AI metric judgment |
|---|---|---|---|---|---|---|---|---|---|
| Jan 2027 | 1.8x | 1.9x | 4.5x | 157 | 51% | 2% | -2.6 SD | -3.2 SD | -3.4 SD |
| Jul 2027 | 2.1x | 2.5x | 10.7x | 2,046 | 23% | 5% | +0.3 SD | -2.2 SD | -2.9 SD |
| Jan 2028 | 2.2x | 4.0x | 14.5x | 10,000 | 17% | 11% | +3.9 SD | -1.0 SD | -2.3 SD |
| Jul 2028 | 2.4x | 6.4x | 15.2x | 10,000 | 16% | 26% | +7.1 SD | +0.0 SD | -1.7 SD |

### Each input moved: ideas +3, transfer +1, metrics +0.5

| Case | Researcher-level AI | TED-AI | AI passes the best researcher on every kind of judgment | Central audits delay TED-AI | 9-month lag delays TED-AI |
|---|---|---|---|---|---|
| Central | Aug 2028 | Nov 2028 | Nov 2028 | +16 mo | +12 mo |
| Experiments from unlimited AI labor: 5 times | Oct 2028 | Jan 2029 | Jan 2029 | +18 mo | +12 mo |
| Experiments from unlimited AI labor: 60 times | Apr 2028 | Jun 2028 | Jun 2028 | +12 mo | +14 mo |
| Validity with the AI judging today: 0.3 | Feb 2028 | Apr 2028 | Apr 2028 | +8 mo | +11 mo |
| Validity with the AI judging today: 0.01 | Jan 2029 | Mar 2029 | Apr 2029 | +21 mo | +11 mo |
| Transfer with the AI judging today: 0.4 | Sep 2028 | Nov 2028 | Dec 2028 | +16 mo | +12 mo |
| AI never judges better than people | Oct 2028 | Feb 2029 | Mar 2029 | +19 mo | +11 mo |
| People can vouch for any gain | Mar 2028 | Apr 2028 | Apr 2028 | +11 mo | +16 mo |
| People can vouch for gains up to +1 SD ideas | Dec 2028 | Feb 2029 | Mar 2029 | +15 mo | +11 mo |
| Judging time per experiment grows with candidates, elasticity 0.25 | Mar 2029 | May 2029 | May 2029 | +14 mo | +12 mo |
| 60% of researcher time was already on judging | Nov 2028 | Jan 2029 | Jan 2029 | +15 mo | +13 mo |
| Ideas improve +2.1 SD a year | Jan 2029 | Apr 2029 | May 2029 | +21 mo | +12 mo |
| Selection worth twice as much | Jul 2028 | Sep 2028 | Sep 2028 | +15 mo | +12 mo |
| Up to a million candidates behind each experiment | Aug 2028 | Oct 2028 | Nov 2028 | +15 mo | +13 mo |
| Compute grows at half the historical rate from 2029 | Aug 2028 | Nov 2028 | Nov 2028 | +19 mo | +13 mo |
| Audit time counts in full as judging | Aug 2028 | Nov 2028 | Nov 2028 | +12 mo | +12 mo |
| Audit time does not count as judging | Aug 2028 | Nov 2028 | Nov 2028 | +19 mo | +12 mo |
| Deployed changes do not grow with AI labor | Aug 2028 | Nov 2028 | Nov 2028 | +0 mo | +12 mo |

## Transfer judgment comes with progress and metric judgment with calendar time

### No pacing

| AI judgment gained per year of progress | Researcher-level AI | TED-AI | AI passes the best researcher on every kind of judgment | Pace in Jan 2028 | As measured |
|---|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | Sep 2027 | Nov 2027 | Jan 2029 | over | over |
| Ideas and transfer +3, metrics +1 | Jul 2028 | Feb 2029 | Jun 2033 | 2.9x | 6.7x |
| Ideas and transfer +3, metrics +0.5 | May 2029 | Jul 2030 | Jan 2040 | 2.6x | 6.4x |
| Ideas +3, transfer and metrics +1 | Sep 2028 | Feb 2029 | Jun 2033 | 2.2x | 4.0x |
| Ideas +3, transfer +1, metrics +0.5 | Jun 2029 | Aug 2030 | Jan 2040 | 2.1x | 3.9x |
| Ideas +3, transfer and metrics +0.5 | Apr 2030 | Dec 2030 | Jan 2040 | 2.1x | 2.9x |

### Delay to TED-AI

| AI judgment gained per year | TED-AI, no pacing | Central audits | Strict audits | 9-month lag | 3-fold compute cut |
|---|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | Nov 2027 | +1 mo | +1 mo | +8 mo | +1 mo |
| Ideas and transfer +3, metrics +1 | Feb 2029 | +5 mo | +6 mo | +4 mo | +0 mo |
| Ideas and transfer +3, metrics +0.5 | Jul 2030 | +10 mo | +11 mo | +3 mo | +0 mo |
| Ideas +3, transfer and metrics +1 | Feb 2029 | +5 mo | +6 mo | +5 mo | +1 mo |
| Ideas +3, transfer +1, metrics +0.5 | Aug 2030 | +10 mo | +11 mo | +4 mo | +0 mo |
| Ideas +3, transfer and metrics +0.5 | Dec 2030 | +15 mo | +16 mo | +6 mo | +1 mo |

### The path with no pacing: ideas +3, transfer +1, metrics +0.5

| Date | Pace | Pace as measured | Experiments at scale | Candidates behind each | Share of experiments people judge | Share of a gain the AI keeps | AI ideas | AI transfer judgment | AI metric judgment |
|---|---|---|---|---|---|---|---|---|---|
| Jan 2027 | 1.8x | 1.9x | 4.5x | 157 | 51% | 2% | -2.6 SD | -3.2 SD | -3.4 SD |
| Jul 2027 | 2.1x | 2.5x | 10.7x | 2,035 | 23% | 4% | +0.3 SD | -2.2 SD | -3.2 SD |
| Jan 2028 | 2.1x | 3.9x | 14.5x | 10,000 | 17% | 7% | +3.8 SD | -1.1 SD | -2.9 SD |
| Jul 2028 | 1.8x | 5.1x | 15.1x | 10,000 | 16% | 12% | +6.7 SD | -0.1 SD | -2.7 SD |
| Jan 2029 | 2.7x | 7.3x | 15.3x | 10,000 | 16% | 19% | +10.1 SD | +1.0 SD | -2.4 SD |
| Jan 2030 | 2.4x | 4.8x | 15.3x | 10,000 | 16% | 28% | +17.1 SD | +3.4 SD | -1.9 SD |
| Jan 2032 | 19.8x | 31.0x | 15.3x | 10,000 | 16% | 62% | +52.2 SD | +15.1 SD | -0.9 SD |

### Each input moved: ideas +3, transfer +1, metrics +0.5

| Case | Researcher-level AI | TED-AI | AI passes the best researcher on every kind of judgment | Central audits delay TED-AI | 9-month lag delays TED-AI |
|---|---|---|---|---|---|
| Central | Jun 2029 | Aug 2030 | Jan 2040 | +10 mo | +4 mo |
| Experiments from unlimited AI labor: 5 times | Jul 2029 | Aug 2030 | Jan 2040 | +10 mo | +4 mo |
| Experiments from unlimited AI labor: 60 times | Apr 2029 | Jun 2030 | Jan 2040 | +9 mo | +4 mo |
| Validity with the AI judging today: 0.3 | Apr 2028 | Jul 2028 | Jan 2040 | +10 mo | +12 mo |
| Validity with the AI judging today: 0.01 | Aug 2030 | Aug 2031 | Jan 2040 | +7 mo | +2 mo |
| Transfer with the AI judging today: 0.4 | Jul 2029 | Aug 2030 | Jan 2040 | +10 mo | +4 mo |
| AI never judges better than people | Dec 2029 | Mar 2031 | Jan 2040 | +9 mo | +3 mo |
| People can vouch for any gain | Apr 2028 | Apr 2028 | Jan 2040 | +17 mo | +24 mo |
| People can vouch for gains up to +1 SD ideas | Sep 2029 | Oct 2030 | Jan 2040 | +9 mo | +4 mo |
| Judging time per experiment grows with candidates, elasticity 0.25 | Oct 2029 | Oct 2030 | Jan 2040 | +8 mo | +4 mo |
| 60% of researcher time was already on judging | Aug 2029 | Aug 2030 | Jan 2040 | +10 mo | +4 mo |
| Ideas improve +2.1 SD a year | Mar 2030 | May 2031 | Jan 2040 | +11 mo | +3 mo |
| Selection worth twice as much | Jun 2029 | Jul 2030 | Jan 2040 | +10 mo | +4 mo |
| Up to a million candidates behind each experiment | Jun 2029 | Jul 2030 | Jan 2040 | +10 mo | +4 mo |
| Compute grows at half the historical rate from 2029 | Jul 2029 | Sep 2030 | Jan 2040 | +11 mo | +4 mo |
| Audit time counts in full as judging | Jun 2029 | Aug 2030 | Jan 2040 | +9 mo | +4 mo |
| Audit time does not count as judging | Jun 2029 | Aug 2030 | Jan 2040 | +11 mo | +4 mo |
| Deployed changes do not grow with AI labor | Jun 2029 | Aug 2030 | Jan 2040 | +0 mo | +4 mo |

## Transfer and metric judgment come with calendar time

### No pacing

| AI judgment gained per year of progress | Researcher-level AI | TED-AI | AI passes the best researcher on every kind of judgment | Pace in Jan 2028 | As measured |
|---|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | Nov 2027 | Dec 2027 | Jan 2029 | 31.8x | 22.0x |
| Ideas and transfer +3, metrics +1 | Aug 2028 | Feb 2029 | Jun 2033 | 2.3x | 6.1x |
| Ideas and transfer +3, metrics +0.5 | Jun 2029 | Jul 2030 | Jan 2040 | 2.2x | 6.0x |
| Ideas +3, transfer and metrics +1 | Mar 2029 | Sep 2029 | Jun 2033 | 2.1x | 2.8x |
| Ideas +3, transfer +1, metrics +0.5 | Feb 2030 | Nov 2030 | Jan 2040 | 2.1x | 2.8x |
| Ideas +3, transfer and metrics +0.5 | Nov 2030 | Nov 2031 | Jan 2040 | 2.1x | 2.6x |

### Delay to TED-AI

| AI judgment gained per year | TED-AI, no pacing | Central audits | Strict audits | 9-month lag | 3-fold compute cut |
|---|---|---|---|---|---|
| Ideas, transfer and metrics all +3 SD a year | Dec 2027 | +1 mo | +1 mo | +7 mo | +0 mo |
| Ideas and transfer +3, metrics +1 | Feb 2029 | +5 mo | +5 mo | +4 mo | +0 mo |
| Ideas and transfer +3, metrics +0.5 | Jul 2030 | +10 mo | +11 mo | +3 mo | +0 mo |
| Ideas +3, transfer and metrics +1 | Sep 2029 | +3 mo | +4 mo | +3 mo | +0 mo |
| Ideas +3, transfer +1, metrics +0.5 | Nov 2030 | +7 mo | +8 mo | +3 mo | +0 mo |
| Ideas +3, transfer and metrics +0.5 | Nov 2031 | +7 mo | +8 mo | +2 mo | +0 mo |

### The path with no pacing: ideas +3, transfer +1, metrics +0.5

| Date | Pace | Pace as measured | Experiments at scale | Candidates behind each | Share of experiments people judge | Share of a gain the AI keeps | AI ideas | AI transfer judgment | AI metric judgment |
|---|---|---|---|---|---|---|---|---|---|
| Jan 2027 | 1.8x | 1.9x | 4.5x | 157 | 51% | 2% | -2.6 SD | -3.3 SD | -3.4 SD |
| Jul 2027 | 2.1x | 2.4x | 10.6x | 2,026 | 23% | 3% | +0.3 SD | -2.8 SD | -3.2 SD |
| Jan 2028 | 2.1x | 2.8x | 14.5x | 10,000 | 17% | 4% | +3.8 SD | -2.3 SD | -2.9 SD |
| Jul 2028 | 1.6x | 2.7x | 15.1x | 10,000 | 16% | 6% | +6.5 SD | -1.8 SD | -2.7 SD |
| Jan 2029 | 1.5x | 2.9x | 15.2x | 10,000 | 16% | 9% | +8.8 SD | -1.3 SD | -2.4 SD |
| Jan 2030 | 1.8x | 4.7x | 15.3x | 10,000 | 16% | 19% | +13.5 SD | -0.3 SD | -1.9 SD |
| Jan 2032 | 20.0x | 31.5x | 15.3x | 10,000 | 16% | 62% | +52.0 SD | +1.7 SD | -0.9 SD |

### Each input moved: ideas +3, transfer +1, metrics +0.5

| Case | Researcher-level AI | TED-AI | AI passes the best researcher on every kind of judgment | Central audits delay TED-AI | 9-month lag delays TED-AI |
|---|---|---|---|---|---|
| Central | Feb 2030 | Nov 2030 | Jan 2040 | +7 mo | +3 mo |
| Experiments from unlimited AI labor: 5 times | Mar 2030 | Nov 2030 | Jan 2040 | +8 mo | +3 mo |
| Experiments from unlimited AI labor: 60 times | Jan 2030 | Oct 2030 | Jan 2040 | +6 mo | +3 mo |
| Validity with the AI judging today: 0.3 | Dec 2028 | Sep 2029 | Jan 2040 | +7 mo | +4 mo |
| Validity with the AI judging today: 0.01 | Nov 2030 | Aug 2031 | Jan 2040 | +7 mo | +3 mo |
| Transfer with the AI judging today: 0.4 | Jan 2030 | Jan 2031 | Jan 2040 | +7 mo | +3 mo |
| AI never judges better than people | Feb 2030 | Mar 2031 | Jan 2040 | +9 mo | +3 mo |
| People can vouch for any gain | Sep 2028 | Sep 2028 | Jan 2040 | +24 mo | +23 mo |
| People can vouch for gains up to +1 SD ideas | Mar 2030 | Dec 2030 | Jan 2040 | +7 mo | +4 mo |
| Judging time per experiment grows with candidates, elasticity 0.25 | Apr 2030 | Dec 2030 | Jan 2040 | +7 mo | +4 mo |
| 60% of researcher time was already on judging | Mar 2030 | Nov 2030 | Jan 2040 | +7 mo | +3 mo |
| Ideas improve +2.1 SD a year | Aug 2030 | Jun 2031 | Jan 2040 | +10 mo | +4 mo |
| Selection worth twice as much | Feb 2030 | Nov 2030 | Jan 2040 | +7 mo | +3 mo |
| Up to a million candidates behind each experiment | Feb 2030 | Nov 2030 | Jan 2040 | +7 mo | +3 mo |
| Compute grows at half the historical rate from 2029 | Mar 2030 | Dec 2030 | Jan 2040 | +8 mo | +4 mo |
| Audit time counts in full as judging | Feb 2030 | Nov 2030 | Jan 2040 | +6 mo | +3 mo |
| Audit time does not count as judging | Feb 2030 | Nov 2030 | Jan 2040 | +8 mo | +3 mo |
| Deployed changes do not grow with AI labor | Feb 2030 | Nov 2030 | Jan 2040 | +0 mo | +3 mo |

## Every scenario, with transfer and metric judgment coming with progress

### Ideas, transfer and metrics all +3 SD a year

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Jun 2027 |  | Jun 2027 |  |
| Comprehension audits, light | Jun 2027 | +0 mo | Jun 2027 | +0 mo |
| Comprehension audits, central | Jun 2027 | +0 mo | Jun 2027 | +0 mo |
| Comprehension audits, strict | Jul 2027 | +1 mo | Jul 2027 | +1 mo |
| Internal-use lag, 3 months | Oct 2027 | +4 mo | Nov 2027 | +5 mo |
| Internal-use lag, 9 months | Jan 2028 | +7 mo | May 2028 | +11 mo |
| R&D compute cut 3x | Jul 2027 | +1 mo | Jul 2027 | +1 mo |
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
| R&D compute cut 3x | Nov 2027 | +1 mo | Dec 2027 | +1 mo |
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
| R&D compute cut 3x | Apr 2028 | +1 mo | Aug 2028 | +1 mo |
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
| R&D compute cut 3x | Mar 2028 | +1 mo | Apr 2028 | +2 mo |
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
| R&D compute cut 3x | Oct 2028 | +1 mo | Dec 2028 | +2 mo |
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
| R&D compute cut 3x | May 2029 | +2 mo | Sep 2029 | +2 mo |
| Comprehension audits (central) + 9-month lag | Sep 2030 | +17 mo | Oct 2031 | +27 mo |

