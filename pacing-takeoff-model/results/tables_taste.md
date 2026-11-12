# Probability of each milestone by date, by taste model and pacing scenario

Written by `montecarlo_taste.py`. Do not edit by hand.

96 of 9630 sampled trajectories (1.0%) had a pace of 1.5x to 2x on Nov 1, 2026 with AI research taste too low to contribute, and are kept. Parameters other than taste are drawn from AI Futures' August 2026 distribution for Daniel, seed 20261110. Median pace of the kept trajectories: 1.67x. Every taste model puts AI research taste at -3.5 SD on Sep 2026, in both classes of task where there are two. In the split models crisp tasks take 70% of research effort while judgment is equal across the classes, and the elasticity of substitution between the classes is 0.5. Pacing starts Jan 1, 2027. Delays are paired: each trajectory under a scenario against the same trajectory with no pacing. A milestone not reached by the end of 2039 counts as later than that. The link from comprehension to human judgment is on except where a table says otherwise.

## Summary

### Superhuman AI researcher: median date and median delay

| Scenario | +3 SD: median date | +3 SD: median delay | +1 SD: median date | +1 SD: median delay | Crisp +3, fuzzy +1 SD: median date | Crisp +3, fuzzy +1 SD: median delay | Crisp +3, fuzzy +0.5 SD: median date | Crisp +3, fuzzy +0.5 SD: median delay |
|---|---|---|---|---|---|---|---|---|
| No pacing | Jul 2027 |  | Jun 2029 |  | Oct 2027 |  | Jan 2028 |  |
| Human sign-off, no comprehension standard | Jul 2027 | +0 mo | Aug 2029 | +1 mo | Oct 2027 | +0 mo | Mar 2028 | +0 mo |
| Comprehension audits, light | Jul 2027 | +0 mo | Apr 2030 | +4 mo | Nov 2027 | +0 mo | Mar 2028 | +1 mo |
| Comprehension audits, central | Jul 2027 | +0 mo | Aug 2030 | +8 mo | Nov 2027 | +1 mo | Apr 2028 | +1 mo |
| Comprehension audits, strict | Aug 2027 | +1 mo | Jan 2031 | +13 mo | Jan 2028 | +2 mo | Jun 2028 | +3 mo |
| Internal-use lag, 3 months | Oct 2027 | +3 mo | Oct 2029 | +4 mo | Feb 2028 | +4 mo | Aug 2028 | +4 mo |
| Internal-use lag, 9 months | Mar 2028 | +8 mo | May 2030 | +11 mo | Sep 2028 | +10 mo | Mar 2029 | +11 mo |
| R&D compute cut 3x | Nov 2027 | +4 mo | May 2030 | +12 mo | Apr 2028 | +5 mo | Aug 2028 | +7 mo |
| Comprehension audits (central) + 3-month lag | Nov 2027 | +4 mo | Oct 2030 | +11 mo | Mar 2028 | +5 mo | Aug 2028 | +5 mo |
| Comprehension audits (central) + 9-month lag | Mar 2028 | +8 mo | Mar 2031 | +18 mo | Sep 2028 | +10 mo | Apr 2029 | +11 mo |

### TED-AI: median date and median delay

| Scenario | +3 SD: median date | +3 SD: median delay | +1 SD: median date | +1 SD: median delay | Crisp +3, fuzzy +1 SD: median date | Crisp +3, fuzzy +1 SD: median delay | Crisp +3, fuzzy +0.5 SD: median date | Crisp +3, fuzzy +0.5 SD: median delay |
|---|---|---|---|---|---|---|---|---|
| No pacing | Sep 2027 |  | Aug 2032 |  | May 2028 |  | May 2031 |  |
| Human sign-off, no comprehension standard | Sep 2027 | +0 mo | Dec 2032 | +2 mo | Jun 2028 | +0 mo | Nov 2031 | +0 mo |
| Comprehension audits, light | Oct 2027 | +0 mo | Feb 2034 | +9 mo | Aug 2028 | +1 mo | Feb 2032 | +3 mo |
| Comprehension audits, central | Oct 2027 | +1 mo | Oct 2034 | +14 mo | Sep 2028 | +2 mo | Jun 2032 | +5 mo |
| Comprehension audits, strict | Nov 2027 | +2 mo | Jul 2035 | +21 mo | Dec 2028 | +4 mo | Jan 2033 | +9 mo |
| Internal-use lag, 3 months | Feb 2028 | +5 mo | Mar 2033 | +4 mo | Oct 2028 | +5 mo | Nov 2031 | +4 mo |
| Internal-use lag, 9 months | Sep 2028 | +11 mo | Nov 2033 | +13 mo | Jun 2029 | +13 mo | May 2032 | +12 mo |
| R&D compute cut 3x | Feb 2028 | +5 mo | Apr 2034 | +16 mo | Jan 2029 | +7 mo | Jul 2032 | +10 mo |
| Comprehension audits (central) + 3-month lag | Mar 2028 | +5 mo | Jan 2035 | +19 mo | Feb 2029 | +7 mo | Jul 2032 | +10 mo |
| Comprehension audits (central) + 9-month lag | Sep 2028 | +11 mo | Apr 2035 | +30 mo | Sep 2029 | +15 mo | Jan 2033 | +17 mo |

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

## Crisp tasks improve +3 SD and fuzzy tasks +1 SD per year of 2025 progress (split_1)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2028 | By start of 2029 | By start of 2031 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Oct 2027 | Jul 2027 to Mar 2028 | 64% | 98% | 100% |  |  |
| Human sign-off, no comprehension standard | Oct 2027 | Jul 2027 to Mar 2028 | 64% | 98% | 100% | +0 mo | +0 mo |
| Comprehension audits, light | Nov 2027 | Aug 2027 to Mar 2028 | 64% | 98% | 100% | +0 mo | +1 mo |
| Comprehension audits, central | Nov 2027 | Aug 2027 to Apr 2028 | 60% | 98% | 100% | +1 mo | +1 mo |
| Comprehension audits, strict | Jan 2028 | Oct 2027 to May 2028 | 49% | 98% | 100% | +2 mo | +3 mo |
| Internal-use lag, 3 months | Feb 2028 | Dec 2027 to Jul 2028 | 29% | 98% | 100% | +4 mo | +5 mo |
| Internal-use lag, 9 months | Sep 2028 | Jun 2028 to Dec 2028 | 0% | 79% | 100% | +10 mo | +12 mo |
| R&D compute cut 3x | Apr 2028 | Nov 2027 to Nov 2028 | 34% | 81% | 100% | +5 mo | +8 mo |
| Comprehension audits (central) + 3-month lag | Mar 2028 | Jan 2028 to Jul 2028 | 22% | 98% | 100% | +5 mo | +5 mo |
| Comprehension audits (central) + 9-month lag | Sep 2028 | Jul 2028 to Dec 2028 | 0% | 77% | 100% | +10 mo | +12 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2028 | By start of 2029 | By start of 2031 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | May 2028 | Sep 2027 to Jun 2029 | 39% | 65% | 85% |  |  |
| Human sign-off, no comprehension standard | Jun 2028 | Sep 2027 to Jun 2029 | 35% | 65% | 84% | +0 mo | +1 mo |
| Comprehension audits, light | Aug 2028 | Nov 2027 to Aug 2029 | 31% | 60% | 83% | +1 mo | +3 mo |
| Comprehension audits, central | Sep 2028 | Nov 2027 to Oct 2029 | 29% | 58% | 83% | +2 mo | +5 mo |
| Comprehension audits, strict | Dec 2028 | Jan 2028 to Jan 2030 | 23% | 54% | 83% | +4 mo | +7 mo |
| Internal-use lag, 3 months | Oct 2028 | Apr 2028 to Dec 2029 | 10% | 52% | 84% | +5 mo | +6 mo |
| Internal-use lag, 9 months | Jun 2029 | Nov 2028 to Aug 2030 | 0% | 28% | 81% | +13 mo | +15 mo |
| R&D compute cut 3x | Jan 2029 | Feb 2028 to Sep 2030 | 22% | 49% | 78% | +7 mo | +13 mo |
| Comprehension audits (central) + 3-month lag | Feb 2029 | May 2028 to Feb 2030 | 6% | 49% | 83% | +7 mo | +10 mo |
| Comprehension audits (central) + 9-month lag | Sep 2029 | Dec 2028 to Oct 2030 | 0% | 27% | 76% | +15 mo | +19 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Sep 2027 | Oct 2027 |
| No pacing: median date of TED-AI | May 2028 | May 2028 |
| Central audits: median delay to superhuman AI researcher | +1 mo | +1 mo |
| Central audits: median delay to TED-AI | +2 mo | +2 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +14 days and TED-AI by +9 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Nov 2027 | Jul 2028 | +0 mo | +1 mo | +5 mo |
| Nov 1, 2026 or later | 47 | Sep 2027 | Mar 2028 | +1 mo | +3 mo | +6 mo |

## Crisp tasks improve +3 SD and fuzzy tasks +0.5 SD per year of 2025 progress (split_0.5)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Jan 2028 | Oct 2027 to Jan 2029 | 73% | 96% | 100% |  |  |
| Human sign-off, no comprehension standard | Mar 2028 | Nov 2027 to Jan 2029 | 73% | 96% | 100% | +0 mo | +0 mo |
| Comprehension audits, light | Mar 2028 | Dec 2027 to Jan 2029 | 73% | 96% | 100% | +1 mo | +2 mo |
| Comprehension audits, central | Apr 2028 | Dec 2027 to Jan 2029 | 72% | 96% | 100% | +1 mo | +2 mo |
| Comprehension audits, strict | Jun 2028 | Jan 2028 to Mar 2029 | 69% | 95% | 100% | +3 mo | +4 mo |
| Internal-use lag, 3 months | Aug 2028 | Mar 2028 to Apr 2029 | 67% | 96% | 100% | +4 mo | +5 mo |
| Internal-use lag, 9 months | Mar 2029 | Oct 2028 to Nov 2029 | 42% | 93% | 100% | +11 mo | +13 mo |
| R&D compute cut 3x | Aug 2028 | Mar 2028 to Dec 2029 | 57% | 86% | 98% | +7 mo | +11 mo |
| Comprehension audits (central) + 3-month lag | Aug 2028 | Apr 2028 to Apr 2029 | 67% | 96% | 100% | +5 mo | +7 mo |
| Comprehension audits (central) + 9-month lag | Apr 2029 | Nov 2028 to Nov 2029 | 36% | 92% | 100% | +11 mo | +14 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | May 2031 | Mar 2028 to Nov 2036 | 42% | 48% | 67% |  |  |
| Human sign-off, no comprehension standard | Nov 2031 | May 2028 to Jul 2037 | 39% | 43% | 65% | +0 mo | +3 mo |
| Comprehension audits, light | Feb 2032 | Jul 2028 to Oct 2037 | 35% | 43% | 62% | +3 mo | +9 mo |
| Comprehension audits, central | Jun 2032 | Sep 2028 to Feb 2038 | 32% | 43% | 61% | +5 mo | +13 mo |
| Comprehension audits, strict | Jan 2033 | Dec 2028 to Sep 2038 | 26% | 42% | 61% | +9 mo | +21 mo |
| Internal-use lag, 3 months | Nov 2031 | Sep 2028 to Feb 2037 | 30% | 46% | 66% | +4 mo | +6 mo |
| Internal-use lag, 9 months | May 2032 | Jul 2029 to Oct 2037 | 14% | 43% | 64% | +12 mo | +16 mo |
| R&D compute cut 3x | Jul 2032 | Oct 2028 to Feb 2039 | 30% | 43% | 60% | +10 mo | +24 mo |
| Comprehension audits (central) + 3-month lag | Jul 2032 | Feb 2029 to May 2038 | 24% | 42% | 61% | +10 mo | +18 mo |
| Comprehension audits (central) + 9-month lag | Jan 2033 | Oct 2029 to Oct 2038 | 8% | 38% | 61% | +17 mo | +25 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Dec 2027 | Jan 2028 |
| No pacing: median date of TED-AI | Apr 2031 | May 2031 |
| Central audits: median delay to superhuman AI researcher | +2 mo | +1 mo |
| Central audits: median delay to TED-AI | +6 mo | +5 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +29 days and TED-AI by +32 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Aug 2028 | Jan 2032 | +1 mo | +7 mo | +3 mo |
| Nov 1, 2026 or later | 47 | Dec 2027 | Oct 2028 | +1 mo | +5 mo | +6 mo |
