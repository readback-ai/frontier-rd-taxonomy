# Probability of each milestone by date, by taste model and pacing scenario

Written by `montecarlo_taste.py`. Do not edit by hand.

96 of 9630 sampled trajectories (1.0%) had a pace of 1.5x to 2x on Nov 1, 2026 with AI research taste too low to contribute, and are kept. Parameters other than taste are drawn from AI Futures' August 2026 distribution for Daniel, seed 20261110. Median pace of the kept trajectories: 1.67x. Every taste model puts AI research taste at -3.5 SD on Sep 2026, in both classes of task where there are two. In the split models crisp tasks take 70% of research effort while judgment is equal across the classes, and the elasticity of substitution between the classes is 0.5. Pacing starts Jan 1, 2027. Delays are paired: each trajectory under a scenario against the same trajectory with no pacing. A milestone not reached by the end of 2039 counts as later than that. The link from comprehension to human judgment is on except where a table says otherwise.

## Summary

### Superhuman AI researcher, crisp and fuzzy tasks: median date and median delay

| Scenario | Crisp +3, fuzzy +1 SD: median date | Crisp +3, fuzzy +1 SD: median delay | Crisp +3, fuzzy +0.5 SD: median date | Crisp +3, fuzzy +0.5 SD: median delay |
|---|---|---|---|---|
| No pacing | Oct 2027 |  | Jan 2028 |  |
| Human sign-off, no comprehension standard | Oct 2027 | +0 mo | Mar 2028 | +0 mo |
| Comprehension audits, light | Nov 2027 | +0 mo | Mar 2028 | +1 mo |
| Comprehension audits, central | Nov 2027 | +1 mo | Apr 2028 | +1 mo |
| Comprehension audits, strict | Jan 2028 | +2 mo | Jun 2028 | +3 mo |
| Internal-use lag, 3 months | Feb 2028 | +4 mo | Aug 2028 | +4 mo |
| Internal-use lag, 9 months | Sep 2028 | +10 mo | Mar 2029 | +11 mo |
| R&D compute cut 3x | Apr 2028 | +5 mo | Aug 2028 | +7 mo |
| Comprehension audits (central) + 3-month lag | Mar 2028 | +5 mo | Aug 2028 | +5 mo |
| Comprehension audits (central) + 9-month lag | Sep 2028 | +10 mo | Apr 2029 | +11 mo |

### TED-AI, crisp and fuzzy tasks: median date and median delay

| Scenario | Crisp +3, fuzzy +1 SD: median date | Crisp +3, fuzzy +1 SD: median delay | Crisp +3, fuzzy +0.5 SD: median date | Crisp +3, fuzzy +0.5 SD: median delay |
|---|---|---|---|---|
| No pacing | May 2028 |  | May 2031 |  |
| Human sign-off, no comprehension standard | Jun 2028 | +0 mo | Nov 2031 | +0 mo |
| Comprehension audits, light | Aug 2028 | +1 mo | Feb 2032 | +3 mo |
| Comprehension audits, central | Sep 2028 | +2 mo | Jun 2032 | +5 mo |
| Comprehension audits, strict | Dec 2028 | +4 mo | Jan 2033 | +9 mo |
| Internal-use lag, 3 months | Oct 2028 | +5 mo | Nov 2031 | +4 mo |
| Internal-use lag, 9 months | Jun 2029 | +13 mo | May 2032 | +12 mo |
| R&D compute cut 3x | Jan 2029 | +7 mo | Jul 2032 | +10 mo |
| Comprehension audits (central) + 3-month lag | Feb 2029 | +7 mo | Jul 2032 | +10 mo |
| Comprehension audits (central) + 9-month lag | Sep 2029 | +15 mo | Jan 2033 | +17 mo |

## Crisp tasks improve +3 SD and fuzzy tasks +1 SD per year of 2025 progress (split_3_1)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Oct 2027 | Jul 2027 to Mar 2028 | 98% | 100% | 100% |  |  |
| Human sign-off, no comprehension standard | Oct 2027 | Jul 2027 to Mar 2028 | 98% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, light | Nov 2027 | Aug 2027 to Mar 2028 | 98% | 100% | 100% | +0 mo | +1 mo |
| Comprehension audits, central | Nov 2027 | Aug 2027 to Apr 2028 | 98% | 100% | 100% | +1 mo | +1 mo |
| Comprehension audits, strict | Jan 2028 | Oct 2027 to May 2028 | 98% | 100% | 100% | +2 mo | +3 mo |
| Internal-use lag, 3 months | Feb 2028 | Dec 2027 to Jul 2028 | 98% | 100% | 100% | +4 mo | +5 mo |
| Internal-use lag, 9 months | Sep 2028 | Jun 2028 to Dec 2028 | 79% | 100% | 100% | +10 mo | +12 mo |
| R&D compute cut 3x | Apr 2028 | Nov 2027 to Nov 2028 | 81% | 100% | 100% | +5 mo | +8 mo |
| Comprehension audits (central) + 3-month lag | Mar 2028 | Jan 2028 to Jul 2028 | 98% | 100% | 100% | +5 mo | +5 mo |
| Comprehension audits (central) + 9-month lag | Sep 2028 | Jul 2028 to Dec 2028 | 77% | 100% | 100% | +10 mo | +12 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | May 2028 | Sep 2027 to Jun 2029 | 65% | 85% | 93% |  |  |
| Human sign-off, no comprehension standard | Jun 2028 | Sep 2027 to Jun 2029 | 65% | 84% | 93% | +0 mo | +1 mo |
| Comprehension audits, light | Aug 2028 | Nov 2027 to Aug 2029 | 60% | 83% | 93% | +1 mo | +3 mo |
| Comprehension audits, central | Sep 2028 | Nov 2027 to Oct 2029 | 58% | 83% | 93% | +2 mo | +5 mo |
| Comprehension audits, strict | Dec 2028 | Jan 2028 to Jan 2030 | 54% | 83% | 92% | +4 mo | +7 mo |
| Internal-use lag, 3 months | Oct 2028 | Apr 2028 to Dec 2029 | 52% | 84% | 92% | +5 mo | +6 mo |
| Internal-use lag, 9 months | Jun 2029 | Nov 2028 to Aug 2030 | 28% | 81% | 92% | +13 mo | +15 mo |
| R&D compute cut 3x | Jan 2029 | Feb 2028 to Sep 2030 | 49% | 78% | 92% | +7 mo | +13 mo |
| Comprehension audits (central) + 3-month lag | Feb 2029 | May 2028 to Feb 2030 | 49% | 83% | 92% | +7 mo | +10 mo |
| Comprehension audits (central) + 9-month lag | Sep 2029 | Dec 2028 to Oct 2030 | 27% | 76% | 92% | +15 mo | +19 mo |

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

## Crisp tasks improve +3 SD and fuzzy tasks +0.5 SD per year of 2025 progress (split_3_0.5)

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
