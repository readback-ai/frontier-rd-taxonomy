# Probability of each milestone by date, by taste model and pacing scenario

Written by `montecarlo_taste.py`. Do not edit by hand.

96 of 9630 sampled trajectories (1.0%) had a pace of 1.5x to 2x on Nov 1, 2026 with AI research taste too low to contribute, and are kept. Parameters other than taste are drawn from AI Futures' August 2026 distribution for Daniel, seed 20261110. Median pace of the kept trajectories: 1.67x. Every taste model puts AI research taste at -3.5 SD on Sep 2026, in both classes of task where there are two. In the split models supervisable tasks take 65% of research effort while judgment is equal across the classes, and the elasticity of substitution between the classes is 0.25. Pacing starts Jan 1, 2027. Delays are paired: each trajectory under a scenario against the same trajectory with no pacing. A milestone not reached by the end of 2039 counts as later than that. The link from comprehension to human judgment is on except where a table says otherwise. 14% of work needs a person on Nov 1, 2026, and that share falls with the share of researchers whose judgment is still better than the AI's. A person spends 0.5% of that work's time supervising it.

## Summary

### Superhuman AI researcher, supervisable and HTS fuzzy tasks: median date and median delay

| Scenario | Supervisable +3, HTS fuzzy +1 SD: median date | Supervisable +3, HTS fuzzy +1 SD: median delay | Supervisable +3, HTS fuzzy +0.5 SD: median date | Supervisable +3, HTS fuzzy +0.5 SD: median delay | Supervisable +2.1, HTS fuzzy +1 SD: median date | Supervisable +2.1, HTS fuzzy +1 SD: median delay | Supervisable +2.1, HTS fuzzy +0.5 SD: median date | Supervisable +2.1, HTS fuzzy +0.5 SD: median delay |
|---|---|---|---|---|---|---|---|---|
| No pacing | Feb 2028 |  | Feb 2030 |  | Jun 2028 |  | Oct 2030 |  |
| Human sign-off, no comprehension standard | Feb 2028 | +0 mo | Feb 2030 | +0 mo | Jun 2028 | +0 mo | Oct 2030 | +0 mo |
| Comprehension audits, light | Feb 2028 | +0 mo | Mar 2030 | +1 mo | Jul 2028 | +1 mo | Dec 2030 | +1 mo |
| Comprehension audits, central | Mar 2028 | +1 mo | May 2030 | +1 mo | Jul 2028 | +1 mo | Jan 2031 | +2 mo |
| Comprehension audits, strict | Apr 2028 | +2 mo | Oct 2030 | +4 mo | Oct 2028 | +3 mo | Jul 2031 | +6 mo |
| Internal-use lag, 3 months | Jun 2028 | +3 mo | May 2030 | +3 mo | Oct 2028 | +4 mo | Dec 2030 | +2 mo |
| Internal-use lag, 9 months | Dec 2028 | +9 mo | Nov 2030 | +8 mo | Apr 2029 | +9 mo | Jul 2031 | +8 mo |
| R&D compute cut 3x | Aug 2028 | +6 mo | Feb 2031 | +13 mo | Feb 2029 | +8 mo | Mar 2032 | +14 mo |
| Comprehension audits (central) + 3-month lag | Jun 2028 | +4 mo | Jul 2030 | +4 mo | Nov 2028 | +4 mo | Apr 2031 | +4 mo |
| Comprehension audits (central) + 9-month lag | Dec 2028 | +10 mo | Jan 2031 | +9 mo | May 2029 | +10 mo | Sep 2031 | +10 mo |

### TED-AI, supervisable and HTS fuzzy tasks: median date and median delay

| Scenario | Supervisable +3, HTS fuzzy +1 SD: median date | Supervisable +3, HTS fuzzy +1 SD: median delay | Supervisable +3, HTS fuzzy +0.5 SD: median date | Supervisable +3, HTS fuzzy +0.5 SD: median delay | Supervisable +2.1, HTS fuzzy +1 SD: median date | Supervisable +2.1, HTS fuzzy +1 SD: median delay | Supervisable +2.1, HTS fuzzy +0.5 SD: median date | Supervisable +2.1, HTS fuzzy +0.5 SD: median delay |
|---|---|---|---|---|---|---|---|---|
| No pacing | Mar 2029 |  | after 2039 |  | Sep 2029 |  | after 2039 |  |
| Human sign-off, no comprehension standard | Mar 2029 | +0 mo | after 2039 | +0 mo | Oct 2029 | +0 mo | after 2039 | +0 mo |
| Comprehension audits, light | Jul 2029 | +1 mo | after 2039 | +3 mo | Jan 2030 | +1 mo | after 2039 | +3 mo |
| Comprehension audits, central | Sep 2029 | +2 mo | after 2039 | +6 mo | Mar 2030 | +3 mo | after 2039 | +6 mo |
| Comprehension audits, strict | Dec 2029 | +4 mo | after 2039 | +13 mo | Jun 2030 | +6 mo | after 2039 | +14 mo |
| Internal-use lag, 3 months | Sep 2029 | +5 mo | after 2039 | +4 mo | Feb 2030 | +5 mo | after 2039 | +4 mo |
| Internal-use lag, 9 months | Jul 2030 | +12 mo | after 2039 | +11 mo | Jan 2031 | +13 mo | after 2039 | +12 mo |
| R&D compute cut 3x | Feb 2030 | +10 mo | after 2039 | +13 mo | Nov 2030 | +11 mo | after 2039 | +14 mo |
| Comprehension audits (central) + 3-month lag | Feb 2030 | +7 mo | after 2039 | +8 mo | Aug 2030 | +8 mo | after 2039 | +9 mo |
| Comprehension audits (central) + 9-month lag | Oct 2030 | +14 mo | after 2039 | +14 mo | Apr 2031 | +16 mo | after 2039 | +15 mo |

## Supervisable tasks improve +3 SD and HTS fuzzy tasks +1 SD per year of 2025 progress (split_3_1)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Feb 2028 | Nov 2027 to Aug 2028 | 86% | 100% | 100% |  |  |
| Human sign-off, no comprehension standard | Feb 2028 | Nov 2027 to Aug 2028 | 86% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, light | Feb 2028 | Nov 2027 to Aug 2028 | 86% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, central | Mar 2028 | Nov 2027 to Sep 2028 | 82% | 100% | 100% | +1 mo | +1 mo |
| Comprehension audits, strict | Apr 2028 | Jan 2028 to Oct 2028 | 79% | 100% | 100% | +2 mo | +3 mo |
| Internal-use lag, 3 months | Jun 2028 | Mar 2028 to Nov 2028 | 79% | 100% | 100% | +3 mo | +4 mo |
| Internal-use lag, 9 months | Dec 2028 | Sep 2028 to May 2029 | 55% | 100% | 100% | +9 mo | +10 mo |
| R&D compute cut 3x | Aug 2028 | Apr 2028 to May 2029 | 59% | 97% | 100% | +6 mo | +10 mo |
| Comprehension audits (central) + 3-month lag | Jun 2028 | Apr 2028 to Nov 2028 | 78% | 100% | 100% | +4 mo | +5 mo |
| Comprehension audits (central) + 9-month lag | Dec 2028 | Sep 2028 to May 2029 | 54% | 100% | 100% | +10 mo | +11 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Mar 2029 | Feb 2028 to Jan 2031 | 44% | 74% | 91% |  |  |
| Human sign-off, no comprehension standard | Mar 2029 | Feb 2028 to Jan 2031 | 43% | 74% | 91% | +0 mo | +0 mo |
| Comprehension audits, light | Jul 2029 | Mar 2028 to Jun 2031 | 42% | 71% | 89% | +1 mo | +3 mo |
| Comprehension audits, central | Sep 2029 | Apr 2028 to Jul 2031 | 42% | 69% | 86% | +2 mo | +5 mo |
| Comprehension audits, strict | Dec 2029 | Jun 2028 to Nov 2031 | 39% | 67% | 86% | +4 mo | +9 mo |
| Internal-use lag, 3 months | Sep 2029 | Aug 2028 to Apr 2031 | 36% | 72% | 90% | +5 mo | +6 mo |
| Internal-use lag, 9 months | Jul 2030 | Apr 2029 to Dec 2031 | 10% | 58% | 90% | +12 mo | +16 mo |
| R&D compute cut 3x | Feb 2030 | Aug 2028 to Apr 2032 | 38% | 59% | 86% | +10 mo | +16 mo |
| Comprehension audits (central) + 3-month lag | Feb 2030 | Sep 2028 to Dec 2031 | 34% | 67% | 86% | +7 mo | +11 mo |
| Comprehension audits (central) + 9-month lag | Oct 2030 | Apr 2029 to Sep 2032 | 9% | 53% | 86% | +14 mo | +20 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Jan 2028 | Feb 2028 |
| No pacing: median date of TED-AI | Mar 2029 | Mar 2029 |
| Central audits: median delay to superhuman AI researcher | +1 mo | +1 mo |
| Central audits: median delay to TED-AI | +3 mo | +2 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +14 days and TED-AI by +7 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | May 2028 | Nov 2029 | +1 mo | +2 mo | +4 mo |
| Nov 1, 2026 or later | 47 | Dec 2027 | Jul 2028 | +1 mo | +2 mo | +6 mo |

## Supervisable tasks improve +3 SD and HTS fuzzy tasks +0.5 SD per year of 2025 progress (split_3_0.5)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Feb 2030 | Sep 2028 to Apr 2032 | 29% | 65% | 88% |  |  |
| Human sign-off, no comprehension standard | Feb 2030 | Sep 2028 to Apr 2032 | 29% | 65% | 88% | +0 mo | +0 mo |
| Comprehension audits, light | Mar 2030 | Sep 2028 to May 2032 | 28% | 62% | 86% | +1 mo | +1 mo |
| Comprehension audits, central | May 2030 | Oct 2028 to Sep 2032 | 28% | 61% | 85% | +1 mo | +3 mo |
| Comprehension audits, strict | Oct 2030 | Jan 2029 to Feb 2033 | 25% | 55% | 83% | +4 mo | +8 mo |
| Internal-use lag, 3 months | May 2030 | Jan 2029 to May 2032 | 25% | 62% | 86% | +3 mo | +4 mo |
| Internal-use lag, 9 months | Nov 2030 | Sep 2029 to Dec 2032 | 7% | 53% | 85% | +8 mo | +11 mo |
| R&D compute cut 3x | Feb 2031 | May 2029 to Dec 2033 | 20% | 47% | 80% | +13 mo | +20 mo |
| Comprehension audits (central) + 3-month lag | Jul 2030 | Feb 2029 to Nov 2032 | 23% | 58% | 84% | +4 mo | +5 mo |
| Comprehension audits (central) + 9-month lag | Jan 2031 | Sep 2029 to Feb 2033 | 6% | 50% | 83% | +9 mo | +12 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | after 2039 | Oct 2030 to after 2039 | 6% | 26% | 42% |  |  |
| Human sign-off, no comprehension standard | after 2039 | Oct 2030 to after 2039 | 6% | 26% | 42% | +0 mo | +1 mo |
| Comprehension audits, light | after 2039 | Oct 2031 to after 2039 | 5% | 24% | 42% | +3 mo | +6 mo |
| Comprehension audits, central | after 2039 | Mar 2032 to after 2039 | 5% | 23% | 41% | +6 mo | +12 mo |
| Comprehension audits, strict | after 2039 | Sep 2032 to after 2039 | 3% | 21% | 39% | +13 mo | +21 mo |
| Internal-use lag, 3 months | after 2039 | Apr 2031 to after 2039 | 3% | 24% | 42% | +4 mo | +5 mo |
| Internal-use lag, 9 months | after 2039 | May 2032 to after 2039 | 1% | 20% | 41% | +11 mo | +15 mo |
| R&D compute cut 3x | after 2039 | Nov 2031 to after 2039 | 3% | 22% | 40% | +13 mo | +17 mo |
| Comprehension audits (central) + 3-month lag | after 2039 | Jul 2032 to after 2039 | 3% | 22% | 40% | +8 mo | +14 mo |
| Comprehension audits (central) + 9-month lag | after 2039 | Mar 2033 to after 2039 | 1% | 19% | 38% | +14 mo | +21 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Dec 2029 | Feb 2030 |
| No pacing: median date of TED-AI | after 2039 | after 2039 |
| Central audits: median delay to superhuman AI researcher | +3 mo | +1 mo |
| Central audits: median delay to TED-AI | +7 mo | +6 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +42 days and TED-AI by +31 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Nov 2030 | after 2039 | +1 mo | +4 mo | +3 mo |
| Nov 1, 2026 or later | 47 | May 2029 | Jul 2032 | +1 mo | +6 mo | +4 mo |

## Supervisable tasks improve +2.1 SD and HTS fuzzy tasks +1 SD per year of 2025 progress (split_2.1_1)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Jun 2028 | Feb 2028 to Apr 2029 | 69% | 99% | 100% |  |  |
| Human sign-off, no comprehension standard | Jun 2028 | Feb 2028 to Apr 2029 | 69% | 99% | 100% | +0 mo | +0 mo |
| Comprehension audits, light | Jul 2028 | Mar 2028 to Apr 2029 | 67% | 99% | 100% | +1 mo | +1 mo |
| Comprehension audits, central | Jul 2028 | Mar 2028 to May 2029 | 66% | 99% | 100% | +1 mo | +2 mo |
| Comprehension audits, strict | Oct 2028 | May 2028 to Jun 2029 | 57% | 99% | 100% | +3 mo | +4 mo |
| Internal-use lag, 3 months | Oct 2028 | Jun 2028 to Jun 2029 | 57% | 99% | 100% | +4 mo | +4 mo |
| Internal-use lag, 9 months | Apr 2029 | Jan 2029 to Nov 2029 | 24% | 98% | 100% | +9 mo | +11 mo |
| R&D compute cut 3x | Feb 2029 | Aug 2028 to Mar 2030 | 49% | 92% | 100% | +8 mo | +12 mo |
| Comprehension audits (central) + 3-month lag | Nov 2028 | Jul 2028 to Jun 2029 | 55% | 99% | 100% | +4 mo | +5 mo |
| Comprehension audits (central) + 9-month lag | May 2029 | Jan 2029 to Nov 2029 | 18% | 98% | 100% | +10 mo | +11 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Sep 2029 | Jun 2028 to Sep 2031 | 39% | 67% | 86% |  |  |
| Human sign-off, no comprehension standard | Oct 2029 | Jun 2028 to Sep 2031 | 36% | 64% | 85% | +0 mo | +0 mo |
| Comprehension audits, light | Jan 2030 | Aug 2028 to Jul 2032 | 32% | 64% | 83% | +1 mo | +3 mo |
| Comprehension audits, central | Mar 2030 | Oct 2028 to Aug 2032 | 30% | 60% | 83% | +3 mo | +7 mo |
| Comprehension audits, strict | Jun 2030 | Jan 2029 to Dec 2032 | 25% | 57% | 83% | +6 mo | +12 mo |
| Internal-use lag, 3 months | Feb 2030 | Jan 2029 to Dec 2031 | 25% | 60% | 85% | +5 mo | +6 mo |
| Internal-use lag, 9 months | Jan 2031 | Oct 2029 to Sep 2032 | 2% | 48% | 84% | +13 mo | +16 mo |
| R&D compute cut 3x | Nov 2030 | Jan 2029 to May 2033 | 24% | 52% | 81% | +11 mo | +18 mo |
| Comprehension audits (central) + 3-month lag | Aug 2030 | Feb 2029 to Nov 2032 | 20% | 55% | 83% | +8 mo | +12 mo |
| Comprehension audits (central) + 9-month lag | Apr 2031 | Dec 2029 to Jul 2033 | 2% | 47% | 83% | +16 mo | +21 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Jun 2028 | Jun 2028 |
| No pacing: median date of TED-AI | Sep 2029 | Sep 2029 |
| Central audits: median delay to superhuman AI researcher | +2 mo | +1 mo |
| Central audits: median delay to TED-AI | +3 mo | +3 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +15 days and TED-AI by +5 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Oct 2028 | Mar 2030 | +1 mo | +2 mo | +4 mo |
| Nov 1, 2026 or later | 47 | Apr 2028 | Dec 2028 | +1 mo | +4 mo | +6 mo |

## Supervisable tasks improve +2.1 SD and HTS fuzzy tasks +0.5 SD per year of 2025 progress (split_2.1_0.5)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Oct 2030 | Apr 2029 to Jan 2033 | 18% | 54% | 85% |  |  |
| Human sign-off, no comprehension standard | Oct 2030 | Apr 2029 to Jan 2033 | 18% | 54% | 85% | +0 mo | +0 mo |
| Comprehension audits, light | Dec 2030 | Apr 2029 to Feb 2033 | 18% | 52% | 84% | +1 mo | +2 mo |
| Comprehension audits, central | Jan 2031 | Jun 2029 to Apr 2033 | 17% | 49% | 83% | +2 mo | +3 mo |
| Comprehension audits, strict | Jul 2031 | Nov 2029 to Sep 2033 | 7% | 42% | 81% | +6 mo | +9 mo |
| Internal-use lag, 3 months | Dec 2030 | Jul 2029 to Feb 2033 | 8% | 51% | 84% | +2 mo | +4 mo |
| Internal-use lag, 9 months | Jul 2031 | Feb 2030 to May 2033 | 2% | 40% | 84% | +8 mo | +10 mo |
| R&D compute cut 3x | Mar 2032 | Jan 2030 to Nov 2034 | 3% | 36% | 75% | +14 mo | +22 mo |
| Comprehension audits (central) + 3-month lag | Apr 2031 | Sep 2029 to May 2033 | 5% | 46% | 82% | +4 mo | +6 mo |
| Comprehension audits (central) + 9-month lag | Sep 2031 | Mar 2030 to Oct 2033 | 2% | 35% | 82% | +10 mo | +12 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | after 2039 | Apr 2031 to after 2039 | 3% | 20% | 41% |  |  |
| Human sign-off, no comprehension standard | after 2039 | Jun 2031 to after 2039 | 3% | 20% | 41% | +0 mo | +1 mo |
| Comprehension audits, light | after 2039 | Sep 2031 to after 2039 | 2% | 18% | 39% | +3 mo | +7 mo |
| Comprehension audits, central | after 2039 | Mar 2032 to after 2039 | 2% | 15% | 39% | +6 mo | +13 mo |
| Comprehension audits, strict | after 2039 | Oct 2032 to after 2039 | 1% | 14% | 36% | +14 mo | +23 mo |
| Internal-use lag, 3 months | after 2039 | Aug 2031 to after 2039 | 1% | 17% | 41% | +4 mo | +6 mo |
| Internal-use lag, 9 months | after 2039 | Jun 2032 to after 2039 | 0% | 9% | 39% | +12 mo | +17 mo |
| R&D compute cut 3x | after 2039 | Aug 2032 to after 2039 | 1% | 14% | 38% | +14 mo | +19 mo |
| Comprehension audits (central) + 3-month lag | after 2039 | Jun 2032 to after 2039 | 1% | 15% | 36% | +9 mo | +18 mo |
| Comprehension audits (central) + 9-month lag | after 2039 | Apr 2033 to after 2039 | 0% | 9% | 35% | +15 mo | +25 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Aug 2030 | Oct 2030 |
| No pacing: median date of TED-AI | after 2039 | after 2039 |
| Central audits: median delay to superhuman AI researcher | +4 mo | +2 mo |
| Central audits: median delay to TED-AI | +8 mo | +6 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +45 days and TED-AI by +29 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Sep 2031 | after 2039 | +2 mo | +6 mo | +3 mo |
| Nov 1, 2026 or later | 47 | Nov 2029 | Aug 2033 | +2 mo | +7 mo | +4 mo |
