# Probability of each milestone by date, by taste model and pacing scenario

Written by `montecarlo_taste.py`. Do not edit by hand.

96 of 9630 sampled trajectories (1.0%) had a pace of 1.5x to 2x on Nov 1, 2026 with AI research taste too low to contribute, and are kept. Parameters other than taste are drawn from AI Futures' August 2026 distribution for Daniel, seed 20261110. Median pace of the kept trajectories: 1.67x. Both taste models put AI research taste at -3.5 SD on Sep 2026. Pacing starts Jan 1, 2027. Delays are paired: each trajectory under a scenario against the same trajectory with no pacing. A milestone not reached by the end of 2039 counts as later than that. The link from comprehension to human judgment is on except where a table says otherwise.

## Summary

| Scenario | +3 SD: median superhuman AI researcher | +3 SD: median delay | +3 SD: median TED-AI | +3 SD: median delay | +1 SD: median superhuman AI researcher | +1 SD: median delay | +1 SD: median TED-AI | +1 SD: median delay |
|---|---|---|---|---|---|---|---|---|
| No pacing | Jul 2027 |  | Sep 2027 |  | Jun 2029 |  | Aug 2032 |  |
| Human sign-off, no comprehension standard | Jul 2027 | +0 mo | Sep 2027 | +0 mo | Aug 2029 | +1 mo | Dec 2032 | +2 mo |
| Comprehension audits, light | Jul 2027 | +0 mo | Oct 2027 | +0 mo | Apr 2030 | +4 mo | Feb 2034 | +9 mo |
| Comprehension audits, central | Jul 2027 | +0 mo | Oct 2027 | +1 mo | Aug 2030 | +8 mo | Oct 2034 | +14 mo |
| Comprehension audits, strict | Aug 2027 | +1 mo | Nov 2027 | +2 mo | Jan 2031 | +13 mo | Jul 2035 | +21 mo |
| Internal-use lag, 3 months | Oct 2027 | +3 mo | Feb 2028 | +5 mo | Oct 2029 | +4 mo | Mar 2033 | +4 mo |
| Internal-use lag, 9 months | Mar 2028 | +8 mo | Sep 2028 | +11 mo | May 2030 | +11 mo | Nov 2033 | +13 mo |
| R&D compute cut 3x | Nov 2027 | +4 mo | Feb 2028 | +5 mo | May 2030 | +12 mo | Apr 2034 | +16 mo |
| Comprehension audits (central) + 3-month lag | Nov 2027 | +4 mo | Mar 2028 | +5 mo | Oct 2030 | +11 mo | Jan 2035 | +19 mo |
| Comprehension audits (central) + 9-month lag | Mar 2028 | +8 mo | Sep 2028 | +11 mo | Mar 2031 | +18 mo | Apr 2035 | +30 mo |

## Taste improves +3 SD per year of 2025 progress (baseline)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2028 | By start of 2029 | By start of 2030 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Jul 2027 | May 2027 to Sep 2027 | 94% | 100% | 100% |  |  |
| Human sign-off, no comprehension standard | Jul 2027 | May 2027 to Sep 2027 | 94% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, light | Jul 2027 | Jun 2027 to Sep 2027 | 93% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, central | Jul 2027 | Jun 2027 to Oct 2027 | 92% | 100% | 100% | +0 mo | +1 mo |
| Comprehension audits, strict | Aug 2027 | Jul 2027 to Oct 2027 | 92% | 100% | 100% | +1 mo | +1 mo |
| Internal-use lag, 3 months | Oct 2027 | Sep 2027 to Dec 2027 | 81% | 100% | 100% | +3 mo | +4 mo |
| Internal-use lag, 9 months | Mar 2028 | Feb 2028 to Apr 2028 | 9% | 100% | 100% | +8 mo | +9 mo |
| R&D compute cut 3x | Nov 2027 | Sep 2027 to Mar 2028 | 59% | 99% | 100% | +4 mo | +6 mo |
| Comprehension audits (central) + 3-month lag | Nov 2027 | Sep 2027 to Dec 2027 | 79% | 100% | 100% | +4 mo | +4 mo |
| Comprehension audits (central) + 9-month lag | Mar 2028 | Feb 2028 to Apr 2028 | 9% | 99% | 100% | +8 mo | +9 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2028 | By start of 2029 | By start of 2030 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Sep 2027 | Jun 2027 to Dec 2027 | 75% | 95% | 98% |  |  |
| Human sign-off, no comprehension standard | Sep 2027 | Jun 2027 to Dec 2027 | 75% | 95% | 98% | +0 mo | +0 mo |
| Comprehension audits, light | Oct 2027 | Jul 2027 to Jan 2028 | 74% | 95% | 98% | +0 mo | +1 mo |
| Comprehension audits, central | Oct 2027 | Jul 2027 to Feb 2028 | 66% | 94% | 98% | +1 mo | +2 mo |
| Comprehension audits, strict | Nov 2027 | Aug 2027 to Mar 2028 | 60% | 93% | 98% | +2 mo | +3 mo |
| Internal-use lag, 3 months | Feb 2028 | Nov 2027 to May 2028 | 38% | 93% | 98% | +5 mo | +6 mo |
| Internal-use lag, 9 months | Sep 2028 | May 2028 to Jan 2029 | 1% | 73% | 95% | +11 mo | +13 mo |
| R&D compute cut 3x | Feb 2028 | Oct 2027 to Jul 2028 | 42% | 89% | 96% | +5 mo | +7 mo |
| Comprehension audits (central) + 3-month lag | Mar 2028 | Dec 2027 to Jul 2028 | 34% | 89% | 98% | +5 mo | +6 mo |
| Comprehension audits (central) + 9-month lag | Sep 2028 | May 2028 to Feb 2029 | 1% | 69% | 93% | +11 mo | +14 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Jul 2027 | Jul 2027 |
| No pacing: median date of TED-AI | Sep 2027 | Sep 2027 |
| Central audits: median delay to superhuman AI researcher | +1 mo | +0 mo |
| Central audits: median delay to TED-AI | +1 mo | +1 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +1 days and TED-AI by +1 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Jul 2027 | Sep 2027 | +0 mo | +1 mo | +4 mo |
| Nov 1, 2026 or later | 47 | Jul 2027 | Aug 2027 | +1 mo | +1 mo | +5 mo |

## Taste improves +1 SD per year of 2025 progress (slow)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Jun 2029 | Aug 2028 to Jul 2031 | 36% | 72% | 97% |  |  |
| Human sign-off, no comprehension standard | Aug 2029 | Nov 2028 to Aug 2031 | 31% | 70% | 97% | +1 mo | +2 mo |
| Comprehension audits, light | Apr 2030 | May 2029 to Apr 2032 | 20% | 62% | 97% | +4 mo | +9 mo |
| Comprehension audits, central | Aug 2030 | Jul 2029 to Aug 2032 | 12% | 55% | 97% | +8 mo | +13 mo |
| Comprehension audits, strict | Jan 2031 | Nov 2029 to Nov 2032 | 8% | 49% | 94% | +13 mo | +18 mo |
| Internal-use lag, 3 months | Oct 2029 | Feb 2029 to Oct 2031 | 23% | 67% | 97% | +4 mo | +6 mo |
| Internal-use lag, 9 months | May 2030 | Nov 2029 to Apr 2032 | 3% | 61% | 97% | +11 mo | +15 mo |
| R&D compute cut 3x | May 2030 | May 2029 to Feb 2033 | 19% | 55% | 85% | +12 mo | +19 mo |
| Comprehension audits (central) + 3-month lag | Oct 2030 | Oct 2029 to Oct 2032 | 5% | 52% | 97% | +11 mo | +16 mo |
| Comprehension audits (central) + 9-month lag | Mar 2031 | Apr 2030 to Dec 2032 | 0% | 47% | 97% | +18 mo | +22 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Aug 2032 | Jul 2029 to Dec 2038 | 19% | 41% | 59% |  |  |
| Human sign-off, no comprehension standard | Dec 2032 | Nov 2029 to Dec 2038 | 14% | 33% | 59% | +2 mo | +6 mo |
| Comprehension audits, light | Feb 2034 | Oct 2030 to after 2039 | 8% | 29% | 55% | +9 mo | +26 mo |
| Comprehension audits, central | Oct 2034 | May 2031 to after 2039 | 6% | 24% | 53% | +14 mo | +34 mo |
| Comprehension audits, strict | Jul 2035 | Dec 2031 to after 2039 | 2% | 20% | 48% | +21 mo | +46 mo |
| Internal-use lag, 3 months | Mar 2033 | Jan 2030 to Feb 2039 | 9% | 35% | 58% | +4 mo | +7 mo |
| Internal-use lag, 9 months | Nov 2033 | Nov 2030 to Jul 2039 | 0% | 26% | 57% | +13 mo | +17 mo |
| R&D compute cut 3x | Apr 2034 | May 2030 to after 2039 | 8% | 29% | 54% | +16 mo | +25 mo |
| Comprehension audits (central) + 3-month lag | Jan 2035 | Jul 2031 to after 2039 | 1% | 21% | 49% | +19 mo | +37 mo |
| Comprehension audits (central) + 9-month lag | Apr 2035 | Feb 2032 to after 2039 | 0% | 14% | 47% | +30 mo | +45 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | May 2029 | Jun 2029 |
| No pacing: median date of TED-AI | Jul 2032 | Aug 2032 |
| Central audits: median delay to superhuman AI researcher | +9 mo | +8 mo |
| Central audits: median delay to TED-AI | +15 mo | +14 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +17 days and TED-AI by +7 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Jun 2030 | Sep 2033 | +4 mo | +7 mo | +4 mo |
| Nov 1, 2026 or later | 47 | Jan 2029 | Dec 2030 | +8 mo | +20 mo | +5 mo |
