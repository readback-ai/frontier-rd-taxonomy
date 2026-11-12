# Probability of each milestone by date, by taste model and pacing scenario

Written by `montecarlo_taste.py`. Do not edit by hand.

96 of 9630 sampled trajectories (1.0%) had a pace of 1.5x to 2x on Nov 1, 2026 with AI research taste too low to contribute, and are kept. Parameters other than taste are drawn from AI Futures' August 2026 distribution for Daniel, seed 20261110. Median pace of the kept trajectories: 1.67x. Every taste model puts AI research taste at -3.5 SD on Sep 2026, in both classes of task where there are two. In the split models crisp tasks take 65% of research effort while judgment is equal across the classes, and the elasticity of substitution between the classes is 0.25. Pacing starts Jan 1, 2027. Delays are paired: each trajectory under a scenario against the same trajectory with no pacing. A milestone not reached by the end of 2039 counts as later than that. The link from comprehension to human judgment is on except where a table says otherwise.

## Summary

### Superhuman AI researcher, one taste: median date and median delay

| Scenario | +3 SD: median date | +3 SD: median delay | +1 SD: median date | +1 SD: median delay |
|---|---|---|---|---|
| No pacing | Jul 2027 |  | Jun 2029 |  |
| Human sign-off, no comprehension standard | Jul 2027 | +0 mo | Aug 2029 | +1 mo |
| Comprehension audits, light | Jul 2027 | +0 mo | Apr 2030 | +4 mo |
| Comprehension audits, central | Jul 2027 | +0 mo | Aug 2030 | +8 mo |
| Comprehension audits, strict | Aug 2027 | +1 mo | Jan 2031 | +13 mo |
| Internal-use lag, 3 months | Oct 2027 | +3 mo | Oct 2029 | +4 mo |
| Internal-use lag, 9 months | Mar 2028 | +8 mo | May 2030 | +11 mo |
| R&D compute cut 3x | Nov 2027 | +4 mo | May 2030 | +12 mo |
| Comprehension audits (central) + 3-month lag | Nov 2027 | +4 mo | Oct 2030 | +11 mo |
| Comprehension audits (central) + 9-month lag | Mar 2028 | +8 mo | Mar 2031 | +18 mo |

### Superhuman AI researcher, crisp and fuzzy tasks: median date and median delay

| Scenario | Crisp +3, fuzzy +1 SD: median date | Crisp +3, fuzzy +1 SD: median delay | Crisp +3, fuzzy +0.5 SD: median date | Crisp +3, fuzzy +0.5 SD: median delay | Crisp +2.1, fuzzy +1 SD: median date | Crisp +2.1, fuzzy +1 SD: median delay | Crisp +2.1, fuzzy +0.5 SD: median date | Crisp +2.1, fuzzy +0.5 SD: median delay |
|---|---|---|---|---|---|---|---|---|
| No pacing | Dec 2027 |  | Feb 2029 |  | Mar 2028 |  | Aug 2029 |  |
| Human sign-off, no comprehension standard | Dec 2027 | +0 mo | Jun 2029 | +0 mo | Apr 2028 | +0 mo | Feb 2030 | +1 mo |
| Comprehension audits, light | Jan 2028 | +1 mo | Dec 2029 | +2 mo | Jun 2028 | +1 mo | Sep 2030 | +3 mo |
| Comprehension audits, central | Feb 2028 | +1 mo | Mar 2030 | +3 mo | Jul 2028 | +2 mo | Dec 2030 | +5 mo |
| Comprehension audits, strict | Mar 2028 | +3 mo | Jul 2030 | +7 mo | Sep 2028 | +4 mo | May 2031 | +11 mo |
| Internal-use lag, 3 months | Apr 2028 | +4 mo | Jun 2029 | +4 mo | Jul 2028 | +4 mo | Nov 2029 | +3 mo |
| Internal-use lag, 9 months | Nov 2028 | +10 mo | Feb 2030 | +10 mo | Feb 2029 | +11 mo | Sep 2030 | +10 mo |
| R&D compute cut 3x | Jun 2028 | +6 mo | Jan 2030 | +10 mo | Oct 2028 | +7 mo | Oct 2030 | +13 mo |
| Comprehension audits (central) + 3-month lag | May 2028 | +5 mo | Apr 2030 | +7 mo | Oct 2028 | +6 mo | Feb 2031 | +8 mo |
| Comprehension audits (central) + 9-month lag | Dec 2028 | +11 mo | Jul 2030 | +12 mo | Mar 2029 | +12 mo | Jul 2031 | +15 mo |

### TED-AI, one taste: median date and median delay

| Scenario | +3 SD: median date | +3 SD: median delay | +1 SD: median date | +1 SD: median delay |
|---|---|---|---|---|
| No pacing | Sep 2027 |  | Aug 2032 |  |
| Human sign-off, no comprehension standard | Sep 2027 | +0 mo | Dec 2032 | +2 mo |
| Comprehension audits, light | Oct 2027 | +0 mo | Feb 2034 | +9 mo |
| Comprehension audits, central | Oct 2027 | +1 mo | Oct 2034 | +14 mo |
| Comprehension audits, strict | Nov 2027 | +2 mo | Jul 2035 | +21 mo |
| Internal-use lag, 3 months | Feb 2028 | +5 mo | Mar 2033 | +4 mo |
| Internal-use lag, 9 months | Sep 2028 | +11 mo | Nov 2033 | +13 mo |
| R&D compute cut 3x | Feb 2028 | +5 mo | Apr 2034 | +16 mo |
| Comprehension audits (central) + 3-month lag | Mar 2028 | +5 mo | Jan 2035 | +19 mo |
| Comprehension audits (central) + 9-month lag | Sep 2028 | +11 mo | Apr 2035 | +30 mo |

### TED-AI, crisp and fuzzy tasks: median date and median delay

| Scenario | Crisp +3, fuzzy +1 SD: median date | Crisp +3, fuzzy +1 SD: median delay | Crisp +3, fuzzy +0.5 SD: median date | Crisp +3, fuzzy +0.5 SD: median delay | Crisp +2.1, fuzzy +1 SD: median date | Crisp +2.1, fuzzy +1 SD: median delay | Crisp +2.1, fuzzy +0.5 SD: median date | Crisp +2.1, fuzzy +0.5 SD: median delay |
|---|---|---|---|---|---|---|---|---|
| No pacing | Dec 2028 |  | May 2038 |  | May 2029 |  | Jun 2038 |  |
| Human sign-off, no comprehension standard | Jan 2029 | +0 mo | Apr 2039 | +3 mo | Jun 2029 | +0 mo | Apr 2039 | +4 mo |
| Comprehension audits, light | May 2029 | +2 mo | after 2039 | +12 mo | Jan 2030 | +3 mo | after 2039 | +16 mo |
| Comprehension audits, central | Aug 2029 | +3 mo | after 2039 | +18 mo | Mar 2030 | +5 mo | after 2039 | +22 mo |
| Comprehension audits, strict | Dec 2029 | +6 mo | after 2039 | +26 mo | Jun 2030 | +8 mo | after 2039 | +32 mo |
| Internal-use lag, 3 months | Jun 2029 | +5 mo | Jul 2038 | +5 mo | Oct 2029 | +5 mo | Sep 2038 | +5 mo |
| Internal-use lag, 9 months | Feb 2030 | +14 mo | Dec 2038 | +13 mo | Aug 2030 | +14 mo | Jan 2039 | +14 mo |
| R&D compute cut 3x | Aug 2029 | +9 mo | after 2039 | +11 mo | Apr 2030 | +11 mo | after 2039 | +12 mo |
| Comprehension audits (central) + 3-month lag | Feb 2030 | +9 mo | after 2039 | +22 mo | Aug 2030 | +10 mo | after 2039 | +26 mo |
| Comprehension audits (central) + 9-month lag | Aug 2030 | +17 mo | after 2039 | +25 mo | Apr 2031 | +18 mo | after 2039 | +33 mo |

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

## Crisp tasks improve +3 SD and fuzzy tasks +1 SD per year of 2025 progress (split_3_1)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Dec 2027 | Aug 2027 to Jul 2028 | 88% | 100% | 100% |  |  |
| Human sign-off, no comprehension standard | Dec 2027 | Sep 2027 to Jul 2028 | 88% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, light | Jan 2028 | Oct 2027 to Aug 2028 | 88% | 100% | 100% | +1 mo | +1 mo |
| Comprehension audits, central | Feb 2028 | Oct 2027 to Aug 2028 | 85% | 100% | 100% | +1 mo | +2 mo |
| Comprehension audits, strict | Mar 2028 | Dec 2027 to Oct 2028 | 79% | 100% | 100% | +3 mo | +4 mo |
| Internal-use lag, 3 months | Apr 2028 | Feb 2028 to Nov 2028 | 82% | 100% | 100% | +4 mo | +5 mo |
| Internal-use lag, 9 months | Nov 2028 | Sep 2028 to Apr 2029 | 59% | 100% | 100% | +10 mo | +12 mo |
| R&D compute cut 3x | Jun 2028 | Jan 2028 to May 2029 | 66% | 97% | 100% | +6 mo | +9 mo |
| Comprehension audits (central) + 3-month lag | May 2028 | Mar 2028 to Nov 2028 | 78% | 100% | 100% | +5 mo | +6 mo |
| Comprehension audits (central) + 9-month lag | Dec 2028 | Sep 2028 to Apr 2029 | 58% | 100% | 100% | +11 mo | +13 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Dec 2028 | Dec 2027 to Dec 2030 | 53% | 75% | 91% |  |  |
| Human sign-off, no comprehension standard | Jan 2029 | Dec 2027 to Dec 2030 | 50% | 75% | 91% | +0 mo | +1 mo |
| Comprehension audits, light | May 2029 | Feb 2028 to Jun 2031 | 44% | 70% | 89% | +2 mo | +5 mo |
| Comprehension audits, central | Aug 2029 | Feb 2028 to Aug 2031 | 43% | 70% | 86% | +3 mo | +7 mo |
| Comprehension audits, strict | Dec 2029 | May 2028 to Nov 2031 | 40% | 67% | 86% | +6 mo | +11 mo |
| Internal-use lag, 3 months | Jun 2029 | Jun 2028 to Mar 2031 | 45% | 73% | 90% | +5 mo | +6 mo |
| Internal-use lag, 9 months | Feb 2030 | Feb 2029 to Nov 2031 | 20% | 59% | 90% | +14 mo | +16 mo |
| R&D compute cut 3x | Aug 2029 | May 2028 to Apr 2032 | 43% | 61% | 86% | +9 mo | +16 mo |
| Comprehension audits (central) + 3-month lag | Feb 2030 | Aug 2028 to Jan 2032 | 34% | 67% | 86% | +9 mo | +13 mo |
| Comprehension audits (central) + 9-month lag | Aug 2030 | Mar 2029 to Sep 2032 | 15% | 55% | 86% | +17 mo | +22 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Nov 2027 | Dec 2027 |
| No pacing: median date of TED-AI | Dec 2028 | Dec 2028 |
| Central audits: median delay to superhuman AI researcher | +2 mo | +1 mo |
| Central audits: median delay to TED-AI | +4 mo | +3 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +18 days and TED-AI by +10 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Mar 2028 | Feb 2029 | +1 mo | +2 mo | +5 mo |
| Nov 1, 2026 or later | 47 | Nov 2027 | Apr 2028 | +1 mo | +4 mo | +6 mo |

## Crisp tasks improve +3 SD and fuzzy tasks +0.5 SD per year of 2025 progress (split_3_0.5)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Feb 2029 | Apr 2028 to Jul 2031 | 47% | 71% | 90% |  |  |
| Human sign-off, no comprehension standard | Jun 2029 | Apr 2028 to Aug 2031 | 39% | 70% | 90% | +0 mo | +2 mo |
| Comprehension audits, light | Dec 2029 | Jul 2028 to Jan 2032 | 36% | 68% | 89% | +2 mo | +8 mo |
| Comprehension audits, central | Mar 2030 | Jul 2028 to Feb 2032 | 33% | 64% | 88% | +3 mo | +9 mo |
| Comprehension audits, strict | Jul 2030 | Nov 2028 to Jun 2032 | 28% | 59% | 84% | +7 mo | +15 mo |
| Internal-use lag, 3 months | Jun 2029 | Sep 2028 to Sep 2031 | 36% | 71% | 90% | +4 mo | +5 mo |
| Internal-use lag, 9 months | Feb 2030 | May 2029 to Apr 2032 | 15% | 62% | 89% | +10 mo | +13 mo |
| R&D compute cut 3x | Jan 2030 | Nov 2028 to May 2033 | 32% | 59% | 82% | +10 mo | +20 mo |
| Comprehension audits (central) + 3-month lag | Apr 2030 | Dec 2028 to Mar 2032 | 27% | 62% | 86% | +7 mo | +13 mo |
| Comprehension audits (central) + 9-month lag | Jul 2030 | Aug 2029 to Jul 2032 | 8% | 56% | 85% | +12 mo | +19 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | May 2038 | Aug 2029 to after 2039 | 17% | 38% | 44% |  |  |
| Human sign-off, no comprehension standard | Apr 2039 | Jan 2030 to after 2039 | 15% | 33% | 44% | +3 mo | +7 mo |
| Comprehension audits, light | after 2039 | Feb 2031 to after 2039 | 11% | 24% | 41% | +12 mo | +23 mo |
| Comprehension audits, central | after 2039 | Sep 2031 to after 2039 | 9% | 23% | 41% | +18 mo | +31 mo |
| Comprehension audits, strict | after 2039 | May 2032 to after 2039 | 4% | 22% | 41% | +26 mo | +41 mo |
| Internal-use lag, 3 months | Jul 2038 | Jan 2030 to after 2039 | 14% | 34% | 44% | +5 mo | +7 mo |
| Internal-use lag, 9 months | Dec 2038 | Nov 2030 to after 2039 | 2% | 26% | 44% | +13 mo | +17 mo |
| R&D compute cut 3x | after 2039 | Jun 2030 to after 2039 | 10% | 31% | 43% | +11 mo | +15 mo |
| Comprehension audits (central) + 3-month lag | after 2039 | Nov 2031 to after 2039 | 5% | 22% | 41% | +22 mo | +35 mo |
| Comprehension audits (central) + 9-month lag | after 2039 | Jul 2032 to after 2039 | 2% | 20% | 40% | +25 mo | +42 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Oct 2028 | Feb 2029 |
| No pacing: median date of TED-AI | May 2038 | May 2038 |
| Central audits: median delay to superhuman AI researcher | +5 mo | +3 mo |
| Central audits: median delay to TED-AI | +21 mo | +18 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +53 days and TED-AI by +43 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Feb 2030 | after 2039 | +3 mo | +25 mo | +4 mo |
| Nov 1, 2026 or later | 47 | Jun 2028 | Nov 2030 | +4 mo | +15 mo | +5 mo |

## Crisp tasks improve +2.1 SD and fuzzy tasks +1 SD per year of 2025 progress (split_2.1_1)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Mar 2028 | Nov 2027 to Jan 2029 | 74% | 99% | 100% |  |  |
| Human sign-off, no comprehension standard | Apr 2028 | Nov 2027 to Feb 2029 | 73% | 99% | 100% | +0 mo | +0 mo |
| Comprehension audits, light | Jun 2028 | Dec 2027 to Mar 2029 | 71% | 99% | 100% | +1 mo | +3 mo |
| Comprehension audits, central | Jul 2028 | Jan 2028 to Apr 2029 | 69% | 99% | 100% | +2 mo | +4 mo |
| Comprehension audits, strict | Sep 2028 | Apr 2028 to Jun 2029 | 62% | 99% | 100% | +4 mo | +6 mo |
| Internal-use lag, 3 months | Jul 2028 | Apr 2028 to Apr 2029 | 65% | 99% | 100% | +4 mo | +5 mo |
| Internal-use lag, 9 months | Feb 2029 | Dec 2028 to Oct 2029 | 34% | 98% | 100% | +11 mo | +13 mo |
| R&D compute cut 3x | Oct 2028 | Apr 2028 to Nov 2029 | 58% | 93% | 100% | +7 mo | +10 mo |
| Comprehension audits (central) + 3-month lag | Oct 2028 | May 2028 to Jun 2029 | 59% | 99% | 100% | +6 mo | +7 mo |
| Comprehension audits (central) + 9-month lag | Mar 2029 | Jan 2029 to Nov 2029 | 25% | 98% | 100% | +12 mo | +14 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | May 2029 | Feb 2028 to Aug 2031 | 45% | 69% | 86% |  |  |
| Human sign-off, no comprehension standard | Jun 2029 | Feb 2028 to Sep 2031 | 43% | 68% | 85% | +0 mo | +2 mo |
| Comprehension audits, light | Jan 2030 | Jun 2028 to Jun 2032 | 33% | 64% | 83% | +3 mo | +8 mo |
| Comprehension audits, central | Mar 2030 | Sep 2028 to Aug 2032 | 32% | 60% | 83% | +5 mo | +11 mo |
| Comprehension audits, strict | Jun 2030 | Dec 2028 to Nov 2032 | 26% | 57% | 83% | +8 mo | +16 mo |
| Internal-use lag, 3 months | Oct 2029 | Sep 2028 to Dec 2031 | 35% | 62% | 85% | +5 mo | +7 mo |
| Internal-use lag, 9 months | Aug 2030 | Jun 2029 to Jul 2032 | 8% | 54% | 84% | +14 mo | +17 mo |
| R&D compute cut 3x | Apr 2030 | Sep 2028 to Apr 2033 | 33% | 56% | 82% | +11 mo | +18 mo |
| Comprehension audits (central) + 3-month lag | Aug 2030 | Feb 2029 to Nov 2032 | 24% | 55% | 83% | +10 mo | +15 mo |
| Comprehension audits (central) + 9-month lag | Apr 2031 | Oct 2029 to Jul 2033 | 4% | 48% | 83% | +18 mo | +24 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Feb 2028 | Mar 2028 |
| No pacing: median date of TED-AI | Apr 2029 | May 2029 |
| Central audits: median delay to superhuman AI researcher | +3 mo | +2 mo |
| Central audits: median delay to TED-AI | +6 mo | +5 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +19 days and TED-AI by +10 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Aug 2028 | Dec 2029 | +1 mo | +3 mo | +5 mo |
| Nov 1, 2026 or later | 47 | Jan 2028 | Sep 2028 | +2 mo | +7 mo | +6 mo |

## Crisp tasks improve +2.1 SD and fuzzy tasks +0.5 SD per year of 2025 progress (split_2.1_0.5)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Aug 2029 | Jul 2028 to Aug 2032 | 42% | 65% | 86% |  |  |
| Human sign-off, no comprehension standard | Feb 2030 | Sep 2028 to Sep 2032 | 36% | 62% | 85% | +1 mo | +2 mo |
| Comprehension audits, light | Sep 2030 | Dec 2028 to Nov 2032 | 27% | 55% | 85% | +3 mo | +9 mo |
| Comprehension audits, central | Dec 2030 | Jan 2029 to Nov 2032 | 23% | 53% | 84% | +5 mo | +12 mo |
| Comprehension audits, strict | May 2031 | Jun 2029 to Jun 2033 | 16% | 46% | 83% | +11 mo | +19 mo |
| Internal-use lag, 3 months | Nov 2029 | Jan 2029 to Oct 2032 | 24% | 60% | 86% | +3 mo | +5 mo |
| Internal-use lag, 9 months | Sep 2030 | Sep 2029 to Dec 2032 | 6% | 56% | 86% | +10 mo | +14 mo |
| R&D compute cut 3x | Oct 2030 | Mar 2029 to Jul 2034 | 19% | 52% | 79% | +13 mo | +21 mo |
| Comprehension audits (central) + 3-month lag | Feb 2031 | May 2029 to Dec 2032 | 12% | 50% | 84% | +8 mo | +15 mo |
| Comprehension audits (central) + 9-month lag | Jul 2031 | Dec 2029 to May 2033 | 3% | 43% | 84% | +15 mo | +21 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Jun 2038 | Dec 2029 to after 2039 | 11% | 34% | 43% |  |  |
| Human sign-off, no comprehension standard | Apr 2039 | Jun 2030 to after 2039 | 7% | 32% | 43% | +4 mo | +10 mo |
| Comprehension audits, light | after 2039 | Jul 2031 to after 2039 | 4% | 23% | 40% | +16 mo | +28 mo |
| Comprehension audits, central | after 2039 | Dec 2031 to after 2039 | 4% | 19% | 39% | +22 mo | +38 mo |
| Comprehension audits, strict | after 2039 | Sep 2032 to after 2039 | 2% | 11% | 38% | +32 mo | +50 mo |
| Internal-use lag, 3 months | Sep 2038 | May 2030 to after 2039 | 6% | 32% | 43% | +5 mo | +7 mo |
| Internal-use lag, 9 months | Jan 2039 | Jun 2031 to after 2039 | 2% | 23% | 43% | +14 mo | +18 mo |
| R&D compute cut 3x | after 2039 | Dec 2030 to after 2039 | 5% | 26% | 42% | +12 mo | +18 mo |
| Comprehension audits (central) + 3-month lag | after 2039 | Apr 2032 to after 2039 | 2% | 16% | 39% | +26 mo | +40 mo |
| Comprehension audits (central) + 9-month lag | after 2039 | Sep 2032 to after 2039 | 0% | 9% | 38% | +33 mo | +45 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Apr 2029 | Aug 2029 |
| No pacing: median date of TED-AI | Jun 2038 | Jun 2038 |
| Central audits: median delay to superhuman AI researcher | +9 mo | +5 mo |
| Central audits: median delay to TED-AI | +23 mo | +22 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +62 days and TED-AI by +46 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Mar 2031 | after 2039 | +5 mo | +29 mo | +4 mo |
| Nov 1, 2026 or later | 47 | Nov 2028 | Apr 2031 | +6 mo | +22 mo | +6 mo |
