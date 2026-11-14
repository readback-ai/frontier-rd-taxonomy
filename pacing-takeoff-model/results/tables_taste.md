# Probability of each milestone by date, by taste model and pacing scenario

Written by `montecarlo_taste.py`. Do not edit by hand.

96 of 9630 sampled trajectories (1.0%) had a pace of 1.5x to 2x on Nov 1, 2026 with AI research taste too low to contribute, and are kept. Parameters other than taste are drawn from AI Futures' August 2026 distribution for Daniel, seed 20261110. Median pace of the kept trajectories: 1.67x. Every taste model puts AI research taste at -3.5 SD on Sep 2026, in both classes of task where there are two. In the split models supervisable tasks take 80% of research effort while judgment is equal across the classes, and the elasticity of substitution between the classes is 0.25. Pacing starts Jan 1, 2027. Delays are paired: each trajectory under a scenario against the same trajectory with no pacing. A milestone not reached by the end of 2039 counts as later than that. The link from comprehension to human judgment is on except where a table says otherwise.

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

### Superhuman AI researcher, supervisable and HTS fuzzy tasks: median date and median delay

| Scenario | Supervisable +3, HTS fuzzy +1 SD: median date | Supervisable +3, HTS fuzzy +1 SD: median delay | Supervisable +3, HTS fuzzy +0.5 SD: median date | Supervisable +3, HTS fuzzy +0.5 SD: median delay | Supervisable +2.1, HTS fuzzy +1 SD: median date | Supervisable +2.1, HTS fuzzy +1 SD: median delay | Supervisable +2.1, HTS fuzzy +0.5 SD: median date | Supervisable +2.1, HTS fuzzy +0.5 SD: median delay |
|---|---|---|---|---|---|---|---|---|
| No pacing | Oct 2027 |  | Feb 2028 |  | Jan 2028 |  | Jun 2028 |  |
| Human sign-off, no comprehension standard | Oct 2027 | +0 mo | Mar 2028 | +0 mo | Jan 2028 | +0 mo | Jul 2028 | +0 mo |
| Comprehension audits, light | Oct 2027 | +0 mo | Apr 2028 | +1 mo | Feb 2028 | +1 mo | Oct 2028 | +1 mo |
| Comprehension audits, central | Oct 2027 | +1 mo | May 2028 | +1 mo | Mar 2028 | +2 mo | Nov 2028 | +2 mo |
| Comprehension audits, strict | Dec 2027 | +2 mo | Jun 2028 | +3 mo | May 2028 | +3 mo | Mar 2029 | +5 mo |
| Internal-use lag, 3 months | Feb 2028 | +4 mo | Jul 2028 | +4 mo | May 2028 | +4 mo | Dec 2028 | +4 mo |
| Internal-use lag, 9 months | Aug 2028 | +10 mo | Jan 2029 | +11 mo | Dec 2028 | +11 mo | Aug 2029 | +11 mo |
| R&D compute cut 3x | Mar 2028 | +5 mo | Jul 2028 | +6 mo | Jul 2028 | +6 mo | Jan 2029 | +8 mo |
| Comprehension audits (central) + 3-month lag | Feb 2028 | +4 mo | Aug 2028 | +5 mo | Jun 2028 | +5 mo | Feb 2029 | +6 mo |
| Comprehension audits (central) + 9-month lag | Aug 2028 | +10 mo | Feb 2029 | +11 mo | Dec 2028 | +11 mo | Oct 2029 | +12 mo |

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

### TED-AI, supervisable and HTS fuzzy tasks: median date and median delay

| Scenario | Supervisable +3, HTS fuzzy +1 SD: median date | Supervisable +3, HTS fuzzy +1 SD: median delay | Supervisable +3, HTS fuzzy +0.5 SD: median date | Supervisable +3, HTS fuzzy +0.5 SD: median delay | Supervisable +2.1, HTS fuzzy +1 SD: median date | Supervisable +2.1, HTS fuzzy +1 SD: median delay | Supervisable +2.1, HTS fuzzy +0.5 SD: median date | Supervisable +2.1, HTS fuzzy +0.5 SD: median delay |
|---|---|---|---|---|---|---|---|---|
| No pacing | Apr 2028 |  | Nov 2031 |  | Oct 2028 |  | Sep 2032 |  |
| Human sign-off, no comprehension standard | Apr 2028 | +0 mo | Mar 2032 | +0 mo | Dec 2028 | +0 mo | Apr 2033 | +1 mo |
| Comprehension audits, light | Jun 2028 | +1 mo | Jul 2032 | +3 mo | Feb 2029 | +2 mo | Nov 2033 | +5 mo |
| Comprehension audits, central | Aug 2028 | +2 mo | Aug 2032 | +5 mo | Mar 2029 | +3 mo | Mar 2034 | +9 mo |
| Comprehension audits, strict | Nov 2028 | +4 mo | Oct 2032 | +9 mo | Jun 2029 | +6 mo | Oct 2034 | +14 mo |
| Internal-use lag, 3 months | Sep 2028 | +5 mo | Jan 2032 | +5 mo | Mar 2029 | +5 mo | Dec 2032 | +5 mo |
| Internal-use lag, 9 months | Jun 2029 | +13 mo | Jul 2032 | +12 mo | Nov 2029 | +14 mo | Jul 2033 | +13 mo |
| R&D compute cut 3x | Dec 2028 | +7 mo | Jun 2033 | +9 mo | Aug 2029 | +9 mo | Jul 2034 | +11 mo |
| Comprehension audits (central) + 3-month lag | Dec 2028 | +7 mo | Oct 2032 | +9 mo | Sep 2029 | +9 mo | Apr 2034 | +12 mo |
| Comprehension audits (central) + 9-month lag | Aug 2029 | +15 mo | Jul 2033 | +16 mo | May 2030 | +17 mo | Sep 2034 | +21 mo |

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

## Supervisable tasks improve +3 SD and HTS fuzzy tasks +1 SD per year of 2025 progress (split_3_1)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Oct 2027 | Jul 2027 to Feb 2028 | 100% | 100% | 100% |  |  |
| Human sign-off, no comprehension standard | Oct 2027 | Jul 2027 to Feb 2028 | 100% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, light | Oct 2027 | Aug 2027 to Mar 2028 | 100% | 100% | 100% | +0 mo | +1 mo |
| Comprehension audits, central | Oct 2027 | Aug 2027 to Mar 2028 | 100% | 100% | 100% | +1 mo | +1 mo |
| Comprehension audits, strict | Dec 2027 | Sep 2027 to Apr 2028 | 100% | 100% | 100% | +2 mo | +2 mo |
| Internal-use lag, 3 months | Feb 2028 | Dec 2027 to Jun 2028 | 99% | 100% | 100% | +4 mo | +5 mo |
| Internal-use lag, 9 months | Aug 2028 | Jun 2028 to Nov 2028 | 85% | 100% | 100% | +10 mo | +11 mo |
| R&D compute cut 3x | Mar 2028 | Nov 2027 to Oct 2028 | 83% | 100% | 100% | +5 mo | +7 mo |
| Comprehension audits (central) + 3-month lag | Feb 2028 | Dec 2027 to Jun 2028 | 99% | 100% | 100% | +4 mo | +5 mo |
| Comprehension audits (central) + 9-month lag | Aug 2028 | Jun 2028 to Nov 2028 | 85% | 100% | 100% | +10 mo | +12 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Apr 2028 | Sep 2027 to May 2029 | 68% | 89% | 94% |  |  |
| Human sign-off, no comprehension standard | Apr 2028 | Sep 2027 to May 2029 | 68% | 89% | 94% | +0 mo | +1 mo |
| Comprehension audits, light | Jun 2028 | Oct 2027 to Jul 2029 | 64% | 85% | 93% | +1 mo | +2 mo |
| Comprehension audits, central | Aug 2028 | Nov 2027 to Sep 2029 | 60% | 84% | 93% | +2 mo | +4 mo |
| Comprehension audits, strict | Nov 2028 | Jan 2028 to Oct 2029 | 55% | 83% | 93% | +4 mo | +7 mo |
| Internal-use lag, 3 months | Sep 2028 | Apr 2028 to Sep 2029 | 53% | 86% | 94% | +5 mo | +6 mo |
| Internal-use lag, 9 months | Jun 2029 | Nov 2028 to Jun 2030 | 31% | 83% | 92% | +13 mo | +15 mo |
| R&D compute cut 3x | Dec 2028 | Jan 2028 to May 2030 | 53% | 80% | 92% | +7 mo | +12 mo |
| Comprehension audits (central) + 3-month lag | Dec 2028 | May 2028 to Feb 2030 | 51% | 84% | 93% | +7 mo | +10 mo |
| Comprehension audits (central) + 9-month lag | Aug 2029 | Nov 2028 to Nov 2030 | 30% | 78% | 92% | +15 mo | +18 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Sep 2027 | Oct 2027 |
| No pacing: median date of TED-AI | Apr 2028 | Apr 2028 |
| Central audits: median delay to superhuman AI researcher | +1 mo | +1 mo |
| Central audits: median delay to TED-AI | +2 mo | +2 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +11 days and TED-AI by +8 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Oct 2027 | Jun 2028 | +0 mo | +1 mo | +5 mo |
| Nov 1, 2026 or later | 47 | Sep 2027 | Feb 2028 | +1 mo | +2 mo | +6 mo |

## Supervisable tasks improve +3 SD and HTS fuzzy tasks +0.5 SD per year of 2025 progress (split_3_0.5)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Feb 2028 | Sep 2027 to Jan 2029 | 74% | 94% | 98% |  |  |
| Human sign-off, no comprehension standard | Mar 2028 | Oct 2027 to Feb 2029 | 74% | 94% | 98% | +0 mo | +0 mo |
| Comprehension audits, light | Apr 2028 | Nov 2027 to Feb 2029 | 74% | 94% | 98% | +1 mo | +2 mo |
| Comprehension audits, central | May 2028 | Nov 2027 to Feb 2029 | 74% | 94% | 98% | +1 mo | +2 mo |
| Comprehension audits, strict | Jun 2028 | Jan 2028 to Feb 2029 | 69% | 91% | 98% | +3 mo | +4 mo |
| Internal-use lag, 3 months | Jul 2028 | Feb 2028 to May 2029 | 70% | 93% | 98% | +4 mo | +5 mo |
| Internal-use lag, 9 months | Jan 2029 | Sep 2028 to Oct 2029 | 46% | 92% | 98% | +11 mo | +13 mo |
| R&D compute cut 3x | Jul 2028 | Mar 2028 to Nov 2029 | 60% | 83% | 96% | +6 mo | +11 mo |
| Comprehension audits (central) + 3-month lag | Aug 2028 | Mar 2028 to May 2029 | 65% | 93% | 98% | +5 mo | +7 mo |
| Comprehension audits (central) + 9-month lag | Feb 2029 | Sep 2028 to Nov 2029 | 43% | 90% | 98% | +11 mo | +14 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Nov 2031 | Mar 2028 to Dec 2038 | 41% | 45% | 64% |  |  |
| Human sign-off, no comprehension standard | Mar 2032 | Apr 2028 to Mar 2039 | 40% | 44% | 64% | +0 mo | +3 mo |
| Comprehension audits, light | Jul 2032 | Aug 2028 to Aug 2039 | 29% | 44% | 59% | +3 mo | +11 mo |
| Comprehension audits, central | Aug 2032 | Sep 2028 to after 2039 | 28% | 43% | 58% | +5 mo | +12 mo |
| Comprehension audits, strict | Oct 2032 | Nov 2028 to after 2039 | 26% | 42% | 56% | +9 mo | +18 mo |
| Internal-use lag, 3 months | Jan 2032 | Oct 2028 to Mar 2039 | 31% | 44% | 64% | +5 mo | +6 mo |
| Internal-use lag, 9 months | Jul 2032 | Jul 2029 to May 2039 | 16% | 43% | 62% | +12 mo | +16 mo |
| R&D compute cut 3x | Jun 2033 | Oct 2028 to after 2039 | 29% | 44% | 59% | +9 mo | +22 mo |
| Comprehension audits (central) + 3-month lag | Oct 2032 | Jan 2029 to after 2039 | 25% | 43% | 58% | +9 mo | +16 mo |
| Comprehension audits (central) + 9-month lag | Jul 2033 | Oct 2029 to after 2039 | 14% | 39% | 57% | +16 mo | +24 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Dec 2027 | Feb 2028 |
| No pacing: median date of TED-AI | Oct 2031 | Nov 2031 |
| Central audits: median delay to superhuman AI researcher | +2 mo | +1 mo |
| Central audits: median delay to TED-AI | +6 mo | +5 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +24 days and TED-AI by +29 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Aug 2028 | Jun 2032 | +1 mo | +6 mo | +3 mo |
| Nov 1, 2026 or later | 47 | Nov 2027 | Oct 2028 | +1 mo | +5 mo | +6 mo |

## Supervisable tasks improve +2.1 SD and HTS fuzzy tasks +1 SD per year of 2025 progress (split_2.1_1)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Jan 2028 | Sep 2027 to Aug 2028 | 85% | 100% | 100% |  |  |
| Human sign-off, no comprehension standard | Jan 2028 | Sep 2027 to Aug 2028 | 85% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, light | Feb 2028 | Oct 2027 to Sep 2028 | 83% | 100% | 100% | +1 mo | +2 mo |
| Comprehension audits, central | Mar 2028 | Nov 2027 to Oct 2028 | 83% | 100% | 100% | +2 mo | +3 mo |
| Comprehension audits, strict | May 2028 | Jan 2028 to Nov 2028 | 80% | 100% | 100% | +3 mo | +4 mo |
| Internal-use lag, 3 months | May 2028 | Feb 2028 to Nov 2028 | 79% | 100% | 100% | +4 mo | +5 mo |
| Internal-use lag, 9 months | Dec 2028 | Sep 2028 to May 2029 | 56% | 100% | 100% | +11 mo | +12 mo |
| R&D compute cut 3x | Jul 2028 | Feb 2028 to May 2029 | 64% | 98% | 100% | +6 mo | +9 mo |
| Comprehension audits (central) + 3-month lag | Jun 2028 | Mar 2028 to Dec 2028 | 76% | 100% | 100% | +5 mo | +7 mo |
| Comprehension audits (central) + 9-month lag | Dec 2028 | Oct 2028 to May 2029 | 53% | 100% | 100% | +11 mo | +13 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Oct 2028 | Dec 2027 to Feb 2030 | 53% | 79% | 93% |  |  |
| Human sign-off, no comprehension standard | Dec 2028 | Dec 2027 to Mar 2030 | 51% | 77% | 93% | +0 mo | +1 mo |
| Comprehension audits, light | Feb 2029 | Feb 2028 to May 2030 | 47% | 76% | 90% | +2 mo | +5 mo |
| Comprehension audits, central | Mar 2029 | Apr 2028 to Oct 2030 | 45% | 76% | 90% | +3 mo | +8 mo |
| Comprehension audits, strict | Jun 2029 | Jul 2028 to Feb 2031 | 38% | 71% | 89% | +6 mo | +12 mo |
| Internal-use lag, 3 months | Mar 2029 | Jun 2028 to Jul 2030 | 43% | 77% | 92% | +5 mo | +7 mo |
| Internal-use lag, 9 months | Nov 2029 | Apr 2029 to Apr 2031 | 18% | 69% | 91% | +14 mo | +16 mo |
| R&D compute cut 3x | Aug 2029 | Jun 2028 to Aug 2031 | 41% | 68% | 89% | +9 mo | +16 mo |
| Comprehension audits (central) + 3-month lag | Sep 2029 | Oct 2028 to Mar 2031 | 33% | 73% | 90% | +9 mo | +12 mo |
| Comprehension audits (central) + 9-month lag | May 2030 | May 2029 to Jan 2032 | 11% | 61% | 89% | +17 mo | +21 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Dec 2027 | Jan 2028 |
| No pacing: median date of TED-AI | Oct 2028 | Oct 2028 |
| Central audits: median delay to superhuman AI researcher | +2 mo | +2 mo |
| Central audits: median delay to TED-AI | +4 mo | +3 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +15 days and TED-AI by +8 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Apr 2028 | Jan 2029 | +1 mo | +2 mo | +5 mo |
| Nov 1, 2026 or later | 47 | Dec 2027 | Jun 2028 | +2 mo | +4 mo | +6 mo |

## Supervisable tasks improve +2.1 SD and HTS fuzzy tasks +0.5 SD per year of 2025 progress (split_2.1_0.5)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Jun 2028 | Jan 2028 to Oct 2029 | 61% | 89% | 98% |  |  |
| Human sign-off, no comprehension standard | Jul 2028 | Feb 2028 to Oct 2029 | 61% | 89% | 98% | +0 mo | +1 mo |
| Comprehension audits, light | Oct 2028 | Mar 2028 to Nov 2029 | 56% | 88% | 98% | +1 mo | +3 mo |
| Comprehension audits, central | Nov 2028 | Apr 2028 to Dec 2029 | 54% | 88% | 98% | +2 mo | +5 mo |
| Comprehension audits, strict | Mar 2029 | Jun 2028 to Apr 2030 | 47% | 85% | 98% | +5 mo | +8 mo |
| Internal-use lag, 3 months | Dec 2028 | Jun 2028 to Feb 2030 | 55% | 88% | 98% | +4 mo | +6 mo |
| Internal-use lag, 9 months | Aug 2029 | Jan 2029 to Aug 2030 | 20% | 84% | 98% | +11 mo | +13 mo |
| R&D compute cut 3x | Jan 2029 | Jun 2028 to Jan 2031 | 49% | 74% | 96% | +8 mo | +14 mo |
| Comprehension audits (central) + 3-month lag | Feb 2029 | Aug 2028 to Mar 2030 | 45% | 85% | 98% | +6 mo | +8 mo |
| Comprehension audits (central) + 9-month lag | Oct 2029 | Mar 2029 to Aug 2030 | 14% | 81% | 98% | +12 mo | +16 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Sep 2032 | Aug 2028 to Apr 2039 | 33% | 45% | 60% |  |  |
| Human sign-off, no comprehension standard | Apr 2033 | Oct 2028 to Aug 2039 | 32% | 44% | 60% | +1 mo | +4 mo |
| Comprehension audits, light | Nov 2033 | Mar 2029 to after 2039 | 20% | 41% | 56% | +5 mo | +15 mo |
| Comprehension audits, central | Mar 2034 | May 2029 to after 2039 | 19% | 40% | 55% | +9 mo | +19 mo |
| Comprehension audits, strict | Oct 2034 | Sep 2029 to after 2039 | 12% | 39% | 52% | +14 mo | +32 mo |
| Internal-use lag, 3 months | Dec 2032 | Feb 2029 to Jun 2039 | 22% | 44% | 58% | +5 mo | +6 mo |
| Internal-use lag, 9 months | Jul 2033 | Dec 2029 to Dec 2039 | 3% | 40% | 57% | +13 mo | +17 mo |
| R&D compute cut 3x | Jul 2034 | Mar 2029 to after 2039 | 21% | 43% | 52% | +11 mo | +24 mo |
| Comprehension audits (central) + 3-month lag | Apr 2034 | Oct 2029 to after 2039 | 10% | 40% | 55% | +12 mo | +21 mo |
| Comprehension audits (central) + 9-month lag | Sep 2034 | May 2030 to after 2039 | 2% | 33% | 51% | +21 mo | +32 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Apr 2028 | Jun 2028 |
| No pacing: median date of TED-AI | Aug 2032 | Sep 2032 |
| Central audits: median delay to superhuman AI researcher | +4 mo | +2 mo |
| Central audits: median delay to TED-AI | +9 mo | +9 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +33 days and TED-AI by +31 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Apr 2029 | Aug 2034 | +2 mo | +10 mo | +3 mo |
| Nov 1, 2026 or later | 47 | Mar 2028 | Mar 2029 | +2 mo | +9 mo | +5 mo |
