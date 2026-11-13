# Probability of each milestone by date, by taste model and pacing scenario

Written by `montecarlo_taste.py`. Do not edit by hand.

96 of 9630 sampled trajectories (1.0%) had a pace of 1.5x to 2x on Nov 1, 2026 with AI research taste too low to contribute, and are kept. Parameters other than taste are drawn from AI Futures' August 2026 distribution for Daniel, seed 20261110. Median pace of the kept trajectories: 1.67x. Every taste model puts AI research taste at -3.5 SD on Sep 2026, in both classes of task where there are two. In the split models crisp tasks take 65% of research effort while judgment is equal across the classes, and the elasticity of substitution between the classes is 0.25. Pacing starts Jan 1, 2027. Delays are paired: each trajectory under a scenario against the same trajectory with no pacing. A milestone not reached by the end of 2039 counts as later than that. The link from comprehension to human judgment is on except where a table says otherwise. 14% of work needs a person on Nov 1, 2026, and that share falls with the share of researchers whose judgment is still better than the AI's.

## Summary

### Superhuman AI researcher, one taste: median date and median delay

| Scenario | +3 SD: median date | +3 SD: median delay | +1 SD: median date | +1 SD: median delay |
|---|---|---|---|---|
| No pacing | Jul 2027 |  | Aug 2030 |  |
| Human sign-off, no comprehension standard | Jul 2027 | +0 mo | Aug 2030 | +0 mo |
| Comprehension audits, light | Aug 2027 | +0 mo | Nov 2030 | +2 mo |
| Comprehension audits, central | Aug 2027 | +0 mo | Jan 2031 | +4 mo |
| Comprehension audits, strict | Sep 2027 | +1 mo | Apr 2031 | +8 mo |
| Internal-use lag, 3 months | Nov 2027 | +3 mo | Jan 2031 | +4 mo |
| Internal-use lag, 9 months | Mar 2028 | +7 mo | Sep 2031 | +11 mo |
| R&D compute cut 3x | Dec 2027 | +4 mo | Nov 2031 | +15 mo |
| Comprehension audits (central) + 3-month lag | Nov 2027 | +3 mo | Apr 2031 | +8 mo |
| Comprehension audits (central) + 9-month lag | Mar 2028 | +7 mo | Oct 2031 | +14 mo |

### Superhuman AI researcher, crisp and fuzzy tasks: median date and median delay

| Scenario | Crisp +3, fuzzy +1 SD: median date | Crisp +3, fuzzy +1 SD: median delay | Crisp +3, fuzzy +0.5 SD: median date | Crisp +3, fuzzy +0.5 SD: median delay | Crisp +2.1, fuzzy +1 SD: median date | Crisp +2.1, fuzzy +1 SD: median delay | Crisp +2.1, fuzzy +0.5 SD: median date | Crisp +2.1, fuzzy +0.5 SD: median delay |
|---|---|---|---|---|---|---|---|---|
| No pacing | May 2028 |  | Oct 2030 |  | Oct 2028 |  | Jul 2031 |  |
| Human sign-off, no comprehension standard | May 2028 | +0 mo | Oct 2030 | +0 mo | Oct 2028 | +0 mo | Jul 2031 | +0 mo |
| Comprehension audits, light | May 2028 | +0 mo | Nov 2030 | +0 mo | Nov 2028 | +0 mo | Aug 2031 | +1 mo |
| Comprehension audits, central | May 2028 | +0 mo | Nov 2030 | +1 mo | Nov 2028 | +1 mo | Aug 2031 | +1 mo |
| Comprehension audits, strict | Jul 2028 | +2 mo | Apr 2031 | +3 mo | Jan 2029 | +2 mo | Dec 2031 | +4 mo |
| Internal-use lag, 3 months | Aug 2028 | +3 mo | Dec 2030 | +2 mo | Feb 2029 | +3 mo | Sep 2031 | +2 mo |
| Internal-use lag, 9 months | Jan 2029 | +8 mo | Jul 2031 | +7 mo | Jul 2029 | +9 mo | Feb 2032 | +7 mo |
| R&D compute cut 3x | Nov 2028 | +7 mo | Sep 2031 | +14 mo | Jul 2029 | +8 mo | Oct 2032 | +16 mo |
| Comprehension audits (central) + 3-month lag | Aug 2028 | +3 mo | Mar 2031 | +3 mo | Feb 2029 | +4 mo | Oct 2031 | +3 mo |
| Comprehension audits (central) + 9-month lag | Feb 2029 | +8 mo | Jul 2031 | +8 mo | Aug 2029 | +9 mo | Apr 2032 | +8 mo |

### TED-AI, one taste: median date and median delay

| Scenario | +3 SD: median date | +3 SD: median delay | +1 SD: median date | +1 SD: median delay |
|---|---|---|---|---|
| No pacing | Oct 2027 |  | Apr 2033 |  |
| Human sign-off, no comprehension standard | Oct 2027 | +0 mo | May 2033 | +1 mo |
| Comprehension audits, light | Oct 2027 | +0 mo | Mar 2034 | +4 mo |
| Comprehension audits, central | Nov 2027 | +1 mo | Sep 2034 | +9 mo |
| Comprehension audits, strict | Nov 2027 | +1 mo | Apr 2035 | +14 mo |
| Internal-use lag, 3 months | Feb 2028 | +5 mo | Aug 2033 | +5 mo |
| Internal-use lag, 9 months | Sep 2028 | +11 mo | Jun 2034 | +15 mo |
| R&D compute cut 3x | Mar 2028 | +5 mo | Jan 2035 | +16 mo |
| Comprehension audits (central) + 3-month lag | Mar 2028 | +5 mo | Jan 2035 | +14 mo |
| Comprehension audits (central) + 9-month lag | Oct 2028 | +11 mo | Jul 2035 | +25 mo |

### TED-AI, crisp and fuzzy tasks: median date and median delay

| Scenario | Crisp +3, fuzzy +1 SD: median date | Crisp +3, fuzzy +1 SD: median delay | Crisp +3, fuzzy +0.5 SD: median date | Crisp +3, fuzzy +0.5 SD: median delay | Crisp +2.1, fuzzy +1 SD: median date | Crisp +2.1, fuzzy +1 SD: median delay | Crisp +2.1, fuzzy +0.5 SD: median date | Crisp +2.1, fuzzy +0.5 SD: median delay |
|---|---|---|---|---|---|---|---|---|
| No pacing | Jul 2029 |  | after 2039 |  | Feb 2030 |  | after 2039 |  |
| Human sign-off, no comprehension standard | Jul 2029 | +0 mo | after 2039 | +0 mo | Feb 2030 | +0 mo | after 2039 | +0 mo |
| Comprehension audits, light | Nov 2029 | +1 mo | after 2039 | +1 mo | Apr 2030 | +1 mo | after 2039 | +2 mo |
| Comprehension audits, central | Dec 2029 | +2 mo | after 2039 | +3 mo | Jun 2030 | +2 mo | after 2039 | +3 mo |
| Comprehension audits, strict | Feb 2030 | +3 mo | after 2039 | +8 mo | Sep 2030 | +5 mo | after 2039 | +9 mo |
| Internal-use lag, 3 months | Jan 2030 | +5 mo | after 2039 | +3 mo | Jul 2030 | +5 mo | after 2039 | +4 mo |
| Internal-use lag, 9 months | Dec 2030 | +13 mo | after 2039 | +10 mo | Jun 2031 | +13 mo | after 2039 | +11 mo |
| R&D compute cut 3x | Aug 2030 | +10 mo | after 2039 | +13 mo | Apr 2031 | +12 mo | after 2039 | +16 mo |
| Comprehension audits (central) + 3-month lag | Apr 2030 | +7 mo | after 2039 | +6 mo | Nov 2030 | +7 mo | after 2039 | +7 mo |
| Comprehension audits (central) + 9-month lag | Feb 2031 | +14 mo | after 2039 | +13 mo | Aug 2031 | +15 mo | after 2039 | +13 mo |

## Taste improves +3 SD per year of 2025 progress (baseline)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2028 | By start of 2029 | By start of 2030 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Jul 2027 | Jun 2027 to Sep 2027 | 94% | 100% | 100% |  |  |
| Human sign-off, no comprehension standard | Jul 2027 | Jun 2027 to Sep 2027 | 94% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, light | Aug 2027 | Jun 2027 to Sep 2027 | 93% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, central | Aug 2027 | Jun 2027 to Oct 2027 | 92% | 100% | 100% | +0 mo | +1 mo |
| Comprehension audits, strict | Sep 2027 | Jul 2027 to Oct 2027 | 89% | 100% | 100% | +1 mo | +1 mo |
| Internal-use lag, 3 months | Nov 2027 | Oct 2027 to Dec 2027 | 78% | 100% | 100% | +3 mo | +4 mo |
| Internal-use lag, 9 months | Mar 2028 | Feb 2028 to Apr 2028 | 9% | 100% | 100% | +7 mo | +8 mo |
| R&D compute cut 3x | Dec 2027 | Sep 2027 to Apr 2028 | 54% | 99% | 100% | +4 mo | +6 mo |
| Comprehension audits (central) + 3-month lag | Nov 2027 | Oct 2027 to Dec 2027 | 77% | 100% | 100% | +3 mo | +4 mo |
| Comprehension audits (central) + 9-month lag | Mar 2028 | Feb 2028 to Apr 2028 | 8% | 99% | 100% | +7 mo | +8 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2028 | By start of 2029 | By start of 2030 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Oct 2027 | Jul 2027 to Jan 2028 | 74% | 95% | 98% |  |  |
| Human sign-off, no comprehension standard | Oct 2027 | Jul 2027 to Jan 2028 | 73% | 95% | 98% | +0 mo | +0 mo |
| Comprehension audits, light | Oct 2027 | Jul 2027 to Jan 2028 | 70% | 95% | 98% | +0 mo | +1 mo |
| Comprehension audits, central | Nov 2027 | Jul 2027 to Feb 2028 | 65% | 94% | 98% | +1 mo | +1 mo |
| Comprehension audits, strict | Nov 2027 | Aug 2027 to Mar 2028 | 60% | 92% | 98% | +1 mo | +3 mo |
| Internal-use lag, 3 months | Feb 2028 | Dec 2027 to Jun 2028 | 34% | 93% | 98% | +5 mo | +6 mo |
| Internal-use lag, 9 months | Sep 2028 | Jun 2028 to Jan 2029 | 1% | 72% | 95% | +11 mo | +13 mo |
| R&D compute cut 3x | Mar 2028 | Oct 2027 to Jul 2028 | 40% | 88% | 95% | +5 mo | +7 mo |
| Comprehension audits (central) + 3-month lag | Mar 2028 | Dec 2027 to Jul 2028 | 27% | 89% | 98% | +5 mo | +6 mo |
| Comprehension audits (central) + 9-month lag | Oct 2028 | Jun 2028 to Feb 2029 | 1% | 69% | 93% | +11 mo | +14 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Jul 2027 | Jul 2027 |
| No pacing: median date of TED-AI | Oct 2027 | Oct 2027 |
| Central audits: median delay to superhuman AI researcher | +1 mo | +0 mo |
| Central audits: median delay to TED-AI | +1 mo | +1 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +0 days and TED-AI by -0 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Jul 2027 | Oct 2027 | +0 mo | +0 mo | +4 mo |
| Nov 1, 2026 or later | 47 | Jul 2027 | Oct 2027 | +0 mo | +1 mo | +5 mo |

## Taste improves +1 SD per year of 2025 progress (slow)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Aug 2030 | Sep 2029 to May 2032 | 8% | 57% | 97% |  |  |
| Human sign-off, no comprehension standard | Aug 2030 | Sep 2029 to Jun 2032 | 8% | 57% | 97% | +0 mo | +0 mo |
| Comprehension audits, light | Nov 2030 | Oct 2029 to Aug 2032 | 5% | 53% | 97% | +2 mo | +3 mo |
| Comprehension audits, central | Jan 2031 | Jan 2030 to Aug 2032 | 5% | 50% | 97% | +4 mo | +6 mo |
| Comprehension audits, strict | Apr 2031 | May 2030 to Nov 2032 | 1% | 43% | 96% | +8 mo | +11 mo |
| Internal-use lag, 3 months | Jan 2031 | Feb 2030 to Sep 2032 | 0% | 50% | 97% | +4 mo | +5 mo |
| Internal-use lag, 9 months | Sep 2031 | Oct 2030 to Jan 2033 | 0% | 33% | 97% | +11 mo | +13 mo |
| R&D compute cut 3x | Nov 2031 | Jun 2030 to Jan 2034 | 1% | 35% | 85% | +15 mo | +20 mo |
| Comprehension audits (central) + 3-month lag | Apr 2031 | Apr 2030 to Nov 2032 | 0% | 47% | 97% | +8 mo | +9 mo |
| Comprehension audits (central) + 9-month lag | Oct 2031 | Nov 2030 to Feb 2033 | 0% | 28% | 96% | +14 mo | +16 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Apr 2033 | Jun 2030 to Dec 2038 | 6% | 33% | 59% |  |  |
| Human sign-off, no comprehension standard | May 2033 | Sep 2030 to Dec 2038 | 5% | 29% | 58% | +1 mo | +3 mo |
| Comprehension audits, light | Mar 2034 | Dec 2030 to after 2039 | 2% | 26% | 54% | +4 mo | +14 mo |
| Comprehension audits, central | Sep 2034 | May 2031 to after 2039 | 0% | 19% | 54% | +9 mo | +20 mo |
| Comprehension audits, strict | Apr 2035 | Dec 2031 to after 2039 | 0% | 17% | 50% | +14 mo | +30 mo |
| Internal-use lag, 3 months | Aug 2033 | Feb 2031 to Mar 2039 | 0% | 22% | 57% | +5 mo | +7 mo |
| Internal-use lag, 9 months | Jun 2034 | Nov 2031 to Aug 2039 | 0% | 9% | 54% | +15 mo | +18 mo |
| R&D compute cut 3x | Jan 2035 | Jun 2031 to after 2039 | 0% | 19% | 50% | +16 mo | +26 mo |
| Comprehension audits (central) + 3-month lag | Jan 2035 | Sep 2031 to after 2039 | 0% | 17% | 50% | +14 mo | +24 mo |
| Comprehension audits (central) + 9-month lag | Jul 2035 | Jun 2032 to after 2039 | 0% | 7% | 46% | +25 mo | +35 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Aug 2030 | Aug 2030 |
| No pacing: median date of TED-AI | Apr 2033 | Apr 2033 |
| Central audits: median delay to superhuman AI researcher | +5 mo | +4 mo |
| Central audits: median delay to TED-AI | +9 mo | +9 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +1 days and TED-AI by -1 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Jun 2031 | Jun 2034 | +3 mo | +6 mo | +5 mo |
| Nov 1, 2026 or later | 47 | Feb 2030 | Feb 2032 | +5 mo | +12 mo | +6 mo |

## Crisp tasks improve +3 SD and fuzzy tasks +1 SD per year of 2025 progress (split_3_1)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | May 2028 | Jan 2028 to Oct 2028 | 82% | 100% | 100% |  |  |
| Human sign-off, no comprehension standard | May 2028 | Feb 2028 to Oct 2028 | 82% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, light | May 2028 | Feb 2028 to Nov 2028 | 81% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, central | May 2028 | Feb 2028 to Nov 2028 | 80% | 100% | 100% | +0 mo | +1 mo |
| Comprehension audits, strict | Jul 2028 | Mar 2028 to Dec 2028 | 77% | 100% | 100% | +2 mo | +2 mo |
| Internal-use lag, 3 months | Aug 2028 | May 2028 to Jan 2029 | 74% | 100% | 100% | +3 mo | +4 mo |
| Internal-use lag, 9 months | Jan 2029 | Oct 2028 to Jun 2029 | 39% | 100% | 100% | +8 mo | +10 mo |
| R&D compute cut 3x | Nov 2028 | Jul 2028 to Aug 2029 | 55% | 96% | 100% | +7 mo | +10 mo |
| Comprehension audits (central) + 3-month lag | Aug 2028 | May 2028 to Feb 2029 | 73% | 100% | 100% | +3 mo | +4 mo |
| Comprehension audits (central) + 9-month lag | Feb 2029 | Nov 2028 to Jun 2029 | 38% | 100% | 100% | +8 mo | +10 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Jul 2029 | Jun 2028 to Feb 2031 | 42% | 74% | 91% |  |  |
| Human sign-off, no comprehension standard | Jul 2029 | Jun 2028 to Feb 2031 | 41% | 74% | 91% | +0 mo | +0 mo |
| Comprehension audits, light | Nov 2029 | Jul 2028 to Jun 2031 | 41% | 70% | 89% | +1 mo | +2 mo |
| Comprehension audits, central | Dec 2029 | Jul 2028 to Jul 2031 | 38% | 67% | 86% | +2 mo | +4 mo |
| Comprehension audits, strict | Feb 2030 | Sep 2028 to Aug 2031 | 33% | 66% | 86% | +3 mo | +8 mo |
| Internal-use lag, 3 months | Jan 2030 | Nov 2028 to May 2031 | 29% | 70% | 90% | +5 mo | +6 mo |
| Internal-use lag, 9 months | Dec 2030 | Jul 2029 to Jan 2032 | 3% | 51% | 89% | +13 mo | +16 mo |
| R&D compute cut 3x | Aug 2030 | Dec 2028 to Jul 2032 | 26% | 57% | 86% | +10 mo | +16 mo |
| Comprehension audits (central) + 3-month lag | Apr 2030 | Dec 2028 to Jan 2032 | 27% | 66% | 86% | +7 mo | +10 mo |
| Comprehension audits (central) + 9-month lag | Feb 2031 | Jul 2029 to Sep 2032 | 3% | 48% | 86% | +14 mo | +20 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | May 2028 | May 2028 |
| No pacing: median date of TED-AI | Jul 2029 | Jul 2029 |
| Central audits: median delay to superhuman AI researcher | +1 mo | +0 mo |
| Central audits: median delay to TED-AI | +2 mo | +2 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +9 days and TED-AI by +2 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Jul 2028 | Dec 2029 | +0 mo | +1 mo | +4 mo |
| Nov 1, 2026 or later | 47 | Mar 2028 | Dec 2028 | +0 mo | +2 mo | +6 mo |

## Crisp tasks improve +3 SD and fuzzy tasks +0.5 SD per year of 2025 progress (split_3_0.5)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Oct 2030 | Apr 2029 to Feb 2033 | 23% | 54% | 83% |  |  |
| Human sign-off, no comprehension standard | Oct 2030 | Apr 2029 to Feb 2033 | 23% | 54% | 83% | +0 mo | +0 mo |
| Comprehension audits, light | Nov 2030 | Apr 2029 to Feb 2033 | 23% | 53% | 83% | +0 mo | +1 mo |
| Comprehension audits, central | Nov 2030 | May 2029 to Mar 2033 | 23% | 52% | 82% | +1 mo | +2 mo |
| Comprehension audits, strict | Apr 2031 | Sep 2029 to May 2033 | 19% | 48% | 82% | +3 mo | +6 mo |
| Internal-use lag, 3 months | Dec 2030 | Jul 2029 to Apr 2033 | 19% | 52% | 83% | +2 mo | +3 mo |
| Internal-use lag, 9 months | Jul 2031 | Jan 2030 to Jul 2033 | 5% | 44% | 82% | +7 mo | +9 mo |
| R&D compute cut 3x | Sep 2031 | Jan 2030 to Nov 2034 | 10% | 39% | 77% | +14 mo | +20 mo |
| Comprehension audits (central) + 3-month lag | Mar 2031 | Aug 2029 to May 2033 | 18% | 48% | 82% | +3 mo | +4 mo |
| Comprehension audits (central) + 9-month lag | Jul 2031 | Jan 2030 to Jul 2033 | 5% | 43% | 81% | +8 mo | +10 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | after 2039 | Feb 2032 to after 2039 | 2% | 22% | 39% |  |  |
| Human sign-off, no comprehension standard | after 2039 | Feb 2032 to after 2039 | 2% | 21% | 39% | +0 mo | +0 mo |
| Comprehension audits, light | after 2039 | Jul 2032 to after 2039 | 1% | 21% | 39% | +1 mo | +3 mo |
| Comprehension audits, central | after 2039 | Aug 2032 to after 2039 | 1% | 21% | 39% | +3 mo | +7 mo |
| Comprehension audits, strict | after 2039 | Jan 2033 to after 2039 | 1% | 20% | 35% | +8 mo | +16 mo |
| Internal-use lag, 3 months | after 2039 | Apr 2032 to after 2039 | 1% | 21% | 39% | +3 mo | +5 mo |
| Internal-use lag, 9 months | after 2039 | Jul 2033 to after 2039 | 0% | 14% | 36% | +10 mo | +15 mo |
| R&D compute cut 3x | after 2039 | Apr 2033 to after 2039 | 1% | 14% | 36% | +13 mo | +18 mo |
| Comprehension audits (central) + 3-month lag | after 2039 | Jan 2033 to after 2039 | 1% | 20% | 36% | +6 mo | +11 mo |
| Comprehension audits (central) + 9-month lag | after 2039 | Feb 2034 to after 2039 | 0% | 14% | 34% | +13 mo | +19 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Sep 2030 | Oct 2030 |
| No pacing: median date of TED-AI | after 2039 | after 2039 |
| Central audits: median delay to superhuman AI researcher | +2 mo | +1 mo |
| Central audits: median delay to TED-AI | +5 mo | +3 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +20 days and TED-AI by +11 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Aug 2031 | after 2039 | +1 mo | +3 mo | +2 mo |
| Nov 1, 2026 or later | 47 | Feb 2030 | Jan 2034 | +1 mo | +4 mo | +4 mo |

## Crisp tasks improve +2.1 SD and fuzzy tasks +1 SD per year of 2025 progress (split_2.1_1)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Oct 2028 | Jun 2028 to May 2029 | 57% | 99% | 100% |  |  |
| Human sign-off, no comprehension standard | Oct 2028 | Jun 2028 to May 2029 | 57% | 99% | 100% | +0 mo | +0 mo |
| Comprehension audits, light | Nov 2028 | Jun 2028 to Jun 2029 | 57% | 99% | 100% | +0 mo | +0 mo |
| Comprehension audits, central | Nov 2028 | Jun 2028 to Jun 2029 | 57% | 99% | 100% | +1 mo | +1 mo |
| Comprehension audits, strict | Jan 2029 | Aug 2028 to Jul 2029 | 49% | 99% | 100% | +2 mo | +3 mo |
| Internal-use lag, 3 months | Feb 2029 | Sep 2028 to Aug 2029 | 42% | 99% | 100% | +3 mo | +4 mo |
| Internal-use lag, 9 months | Jul 2029 | Mar 2029 to Jan 2030 | 8% | 98% | 100% | +9 mo | +10 mo |
| R&D compute cut 3x | Jul 2029 | Dec 2028 to May 2030 | 29% | 86% | 100% | +8 mo | +12 mo |
| Comprehension audits (central) + 3-month lag | Feb 2029 | Oct 2028 to Aug 2029 | 42% | 99% | 100% | +4 mo | +4 mo |
| Comprehension audits (central) + 9-month lag | Aug 2029 | Apr 2029 to Jan 2030 | 5% | 98% | 100% | +9 mo | +10 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Feb 2030 | Nov 2028 to Dec 2031 | 30% | 65% | 86% |  |  |
| Human sign-off, no comprehension standard | Feb 2030 | Nov 2028 to Jan 2032 | 29% | 64% | 85% | +0 mo | +0 mo |
| Comprehension audits, light | Apr 2030 | Dec 2028 to Jul 2032 | 26% | 61% | 83% | +1 mo | +3 mo |
| Comprehension audits, central | Jun 2030 | Feb 2029 to Aug 2032 | 24% | 59% | 83% | +2 mo | +5 mo |
| Comprehension audits, strict | Sep 2030 | Apr 2029 to Jan 2033 | 17% | 55% | 83% | +5 mo | +9 mo |
| Internal-use lag, 3 months | Jul 2030 | May 2029 to Apr 2032 | 10% | 58% | 84% | +5 mo | +6 mo |
| Internal-use lag, 9 months | Jun 2031 | Feb 2030 to Jan 2033 | 0% | 46% | 84% | +13 mo | +17 mo |
| R&D compute cut 3x | Apr 2031 | Jul 2029 to Sep 2033 | 14% | 48% | 80% | +12 mo | +18 mo |
| Comprehension audits (central) + 3-month lag | Nov 2030 | Jun 2029 to Nov 2032 | 8% | 51% | 83% | +7 mo | +11 mo |
| Comprehension audits (central) + 9-month lag | Aug 2031 | Mar 2030 to Jul 2033 | 0% | 43% | 83% | +15 mo | +21 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Oct 2028 | Oct 2028 |
| No pacing: median date of TED-AI | Feb 2030 | Feb 2030 |
| Central audits: median delay to superhuman AI researcher | +2 mo | +1 mo |
| Central audits: median delay to TED-AI | +3 mo | +2 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +8 days and TED-AI by -0 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Mar 2029 | Jun 2030 | +1 mo | +2 mo | +4 mo |
| Nov 1, 2026 or later | 47 | Aug 2028 | Jul 2029 | +1 mo | +3 mo | +5 mo |

## Crisp tasks improve +2.1 SD and fuzzy tasks +0.5 SD per year of 2025 progress (split_2.1_0.5)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Jul 2031 | Feb 2030 to Sep 2033 | 3% | 40% | 81% |  |  |
| Human sign-off, no comprehension standard | Jul 2031 | Feb 2030 to Sep 2033 | 3% | 40% | 81% | +0 mo | +0 mo |
| Comprehension audits, light | Aug 2031 | Feb 2030 to Nov 2033 | 3% | 40% | 81% | +1 mo | +1 mo |
| Comprehension audits, central | Aug 2031 | Mar 2030 to Jan 2034 | 3% | 39% | 80% | +1 mo | +2 mo |
| Comprehension audits, strict | Dec 2031 | May 2030 to May 2034 | 3% | 30% | 80% | +4 mo | +6 mo |
| Internal-use lag, 3 months | Sep 2031 | Mar 2030 to Dec 2033 | 2% | 34% | 80% | +2 mo | +3 mo |
| Internal-use lag, 9 months | Feb 2032 | Oct 2030 to Apr 2034 | 0% | 27% | 80% | +7 mo | +9 mo |
| R&D compute cut 3x | Oct 2032 | Dec 2030 to May 2035 | 1% | 27% | 69% | +16 mo | +23 mo |
| Comprehension audits (central) + 3-month lag | Oct 2031 | Apr 2030 to Feb 2034 | 2% | 31% | 80% | +3 mo | +4 mo |
| Comprehension audits (central) + 9-month lag | Apr 2032 | Nov 2030 to Jun 2034 | 0% | 27% | 80% | +8 mo | +10 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | after 2039 | Jul 2032 to after 2039 | 0% | 12% | 38% |  |  |
| Human sign-off, no comprehension standard | after 2039 | Aug 2032 to after 2039 | 0% | 12% | 38% | +0 mo | +0 mo |
| Comprehension audits, light | after 2039 | Sep 2032 to after 2039 | 0% | 12% | 38% | +2 mo | +4 mo |
| Comprehension audits, central | after 2039 | Jan 2033 to after 2039 | 0% | 10% | 38% | +3 mo | +8 mo |
| Comprehension audits, strict | after 2039 | Jul 2033 to after 2039 | 0% | 8% | 32% | +9 mo | +17 mo |
| Internal-use lag, 3 months | after 2039 | Dec 2032 to after 2039 | 0% | 9% | 38% | +4 mo | +5 mo |
| Internal-use lag, 9 months | after 2039 | Oct 2033 to after 2039 | 0% | 4% | 34% | +11 mo | +15 mo |
| R&D compute cut 3x | after 2039 | Nov 2033 to after 2039 | 0% | 6% | 35% | +16 mo | +20 mo |
| Comprehension audits (central) + 3-month lag | after 2039 | Apr 2033 to after 2039 | 0% | 8% | 35% | +7 mo | +12 mo |
| Comprehension audits (central) + 9-month lag | after 2039 | Mar 2034 to after 2039 | 0% | 3% | 30% | +13 mo | +19 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Jun 2031 | Jul 2031 |
| No pacing: median date of TED-AI | after 2039 | after 2039 |
| Central audits: median delay to superhuman AI researcher | +3 mo | +1 mo |
| Central audits: median delay to TED-AI | +5 mo | +3 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +22 days and TED-AI by +11 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | May 2032 | after 2039 | +1 mo | +3 mo | +3 mo |
| Nov 1, 2026 or later | 47 | Oct 2030 | Jul 2035 | +1 mo | +4 mo | +4 mo |
