# Probability of each milestone by date, by taste model and pacing scenario

Written by `montecarlo_taste.py`. Do not edit by hand.

96 of 9630 sampled trajectories (1.0%) had a pace of 1.5x to 2x on Nov 1, 2026 with AI research taste too low to contribute, and are kept. Parameters other than taste are drawn from AI Futures' August 2026 distribution for Daniel, seed 20261110. Median pace of the kept trajectories: 1.67x. Every taste model puts AI research taste at -3.5 SD on Sep 2026, in both classes of task where there are two. In the split models supervisable tasks take 80% of research effort while judgment is equal across the classes, and the elasticity of substitution between the classes is 0.25. Pacing starts Jan 1, 2027. Delays are paired: each trajectory under a scenario against the same trajectory with no pacing. A milestone not reached by the end of 2039 counts as later than that. The link from comprehension to human judgment is on except where a table says otherwise. 14% of work needs a person on Nov 1, 2026, and that share falls with the share of researchers whose judgment is still better than the AI's. A person spends 0.5% of that work's time supervising it.

## Summary

### Superhuman AI researcher, one taste: median date and median delay

| Scenario | +3 SD: median date | +3 SD: median delay | +1 SD: median date | +1 SD: median delay |
|---|---|---|---|---|
| No pacing | Jul 2027 |  | Dec 2029 |  |
| Human sign-off, no comprehension standard | Jul 2027 | +0 mo | Jan 2030 | +0 mo |
| Comprehension audits, light | Jul 2027 | +0 mo | Jun 2030 | +3 mo |
| Comprehension audits, central | Jul 2027 | +0 mo | Oct 2030 | +5 mo |
| Comprehension audits, strict | Aug 2027 | +1 mo | Mar 2031 | +10 mo |
| Internal-use lag, 3 months | Oct 2027 | +3 mo | May 2030 | +4 mo |
| Internal-use lag, 9 months | Mar 2028 | +8 mo | Dec 2030 | +11 mo |
| R&D compute cut 3x | Nov 2027 | +4 mo | Jan 2031 | +13 mo |
| Comprehension audits (central) + 3-month lag | Nov 2027 | +3 mo | Jan 2031 | +9 mo |
| Comprehension audits (central) + 9-month lag | Mar 2028 | +8 mo | Jun 2031 | +15 mo |

### Superhuman AI researcher, supervisable and HTS fuzzy tasks: median date and median delay

| Scenario | Supervisable +3, HTS fuzzy +1 SD: median date | Supervisable +3, HTS fuzzy +1 SD: median delay | Supervisable +3, HTS fuzzy +0.5 SD: median date | Supervisable +3, HTS fuzzy +0.5 SD: median delay | Supervisable +2.1, HTS fuzzy +1 SD: median date | Supervisable +2.1, HTS fuzzy +1 SD: median delay | Supervisable +2.1, HTS fuzzy +0.5 SD: median date | Supervisable +2.1, HTS fuzzy +0.5 SD: median delay |
|---|---|---|---|---|---|---|---|---|
| No pacing | Oct 2027 |  | May 2028 |  | Mar 2028 |  | Jan 2029 |  |
| Human sign-off, no comprehension standard | Oct 2027 | +0 mo | May 2028 | +0 mo | Mar 2028 | +0 mo | Jan 2029 | +0 mo |
| Comprehension audits, light | Nov 2027 | +0 mo | Jun 2028 | +0 mo | Apr 2028 | +0 mo | Jan 2029 | +0 mo |
| Comprehension audits, central | Nov 2027 | +0 mo | Jun 2028 | +0 mo | Apr 2028 | +1 mo | Jan 2029 | +1 mo |
| Comprehension audits, strict | Dec 2027 | +1 mo | Jul 2028 | +2 mo | Jun 2028 | +2 mo | Apr 2029 | +3 mo |
| Internal-use lag, 3 months | Feb 2028 | +3 mo | Aug 2028 | +3 mo | Jun 2028 | +3 mo | May 2029 | +3 mo |
| Internal-use lag, 9 months | Aug 2028 | +9 mo | Mar 2029 | +9 mo | Jan 2029 | +9 mo | Nov 2029 | +9 mo |
| R&D compute cut 3x | Apr 2028 | +5 mo | Jan 2029 | +7 mo | Sep 2028 | +7 mo | Sep 2029 | +9 mo |
| Comprehension audits (central) + 3-month lag | Mar 2028 | +4 mo | Sep 2028 | +4 mo | Jul 2028 | +4 mo | Jun 2029 | +4 mo |
| Comprehension audits (central) + 9-month lag | Aug 2028 | +9 mo | Mar 2029 | +9 mo | Jan 2029 | +9 mo | Dec 2029 | +10 mo |

### TED-AI, one taste: median date and median delay

| Scenario | +3 SD: median date | +3 SD: median delay | +1 SD: median date | +1 SD: median delay |
|---|---|---|---|---|
| No pacing | Sep 2027 |  | Jan 2033 |  |
| Human sign-off, no comprehension standard | Sep 2027 | +0 mo | Feb 2033 | +1 mo |
| Comprehension audits, light | Oct 2027 | +0 mo | Dec 2033 | +5 mo |
| Comprehension audits, central | Oct 2027 | +1 mo | Aug 2034 | +10 mo |
| Comprehension audits, strict | Nov 2027 | +2 mo | Apr 2035 | +16 mo |
| Internal-use lag, 3 months | Feb 2028 | +5 mo | Jun 2033 | +5 mo |
| Internal-use lag, 9 months | Sep 2028 | +11 mo | Feb 2034 | +14 mo |
| R&D compute cut 3x | Feb 2028 | +5 mo | Sep 2034 | +16 mo |
| Comprehension audits (central) + 3-month lag | Mar 2028 | +5 mo | Nov 2034 | +16 mo |
| Comprehension audits (central) + 9-month lag | Sep 2028 | +11 mo | May 2035 | +25 mo |

### TED-AI, supervisable and HTS fuzzy tasks: median date and median delay

| Scenario | Supervisable +3, HTS fuzzy +1 SD: median date | Supervisable +3, HTS fuzzy +1 SD: median delay | Supervisable +3, HTS fuzzy +0.5 SD: median date | Supervisable +3, HTS fuzzy +0.5 SD: median delay | Supervisable +2.1, HTS fuzzy +1 SD: median date | Supervisable +2.1, HTS fuzzy +1 SD: median delay | Supervisable +2.1, HTS fuzzy +0.5 SD: median date | Supervisable +2.1, HTS fuzzy +0.5 SD: median delay |
|---|---|---|---|---|---|---|---|---|
| No pacing | Jul 2028 |  | Jul 2032 |  | Feb 2029 |  | Nov 2033 |  |
| Human sign-off, no comprehension standard | Jul 2028 | +0 mo | Jul 2032 | +0 mo | Feb 2029 | +0 mo | Nov 2033 | +0 mo |
| Comprehension audits, light | Aug 2028 | +0 mo | Jul 2032 | +1 mo | Mar 2029 | +1 mo | Jan 2034 | +1 mo |
| Comprehension audits, central | Sep 2028 | +1 mo | Aug 2032 | +2 mo | Apr 2029 | +2 mo | Jul 2034 | +3 mo |
| Comprehension audits, strict | Nov 2028 | +3 mo | Dec 2032 | +5 mo | Jul 2029 | +4 mo | Jan 2035 | +7 mo |
| Internal-use lag, 3 months | Jan 2029 | +5 mo | Oct 2032 | +4 mo | Jul 2029 | +5 mo | Dec 2033 | +3 mo |
| Internal-use lag, 9 months | Sep 2029 | +13 mo | Mar 2033 | +10 mo | Apr 2030 | +13 mo | Jul 2034 | +11 mo |
| R&D compute cut 3x | Mar 2029 | +8 mo | Jan 2034 | +11 mo | Jan 2030 | +10 mo | Dec 2035 | +12 mo |
| Comprehension audits (central) + 3-month lag | Feb 2029 | +6 mo | Oct 2032 | +6 mo | Sep 2029 | +7 mo | Oct 2034 | +6 mo |
| Comprehension audits (central) + 9-month lag | Oct 2029 | +13 mo | Sep 2033 | +13 mo | Jun 2030 | +14 mo | Feb 2035 | +13 mo |

## Taste improves +3 SD per year of 2025 progress (baseline)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2028 | By start of 2029 | By start of 2030 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Jul 2027 | May 2027 to Sep 2027 | 94% | 100% | 100% |  |  |
| Human sign-off, no comprehension standard | Jul 2027 | May 2027 to Sep 2027 | 94% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, light | Jul 2027 | Jun 2027 to Sep 2027 | 93% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, central | Jul 2027 | Jun 2027 to Oct 2027 | 92% | 100% | 100% | +0 mo | +1 mo |
| Comprehension audits, strict | Aug 2027 | Jul 2027 to Oct 2027 | 92% | 100% | 100% | +1 mo | +1 mo |
| Internal-use lag, 3 months | Oct 2027 | Sep 2027 to Dec 2027 | 80% | 100% | 100% | +3 mo | +4 mo |
| Internal-use lag, 9 months | Mar 2028 | Feb 2028 to Apr 2028 | 9% | 100% | 100% | +8 mo | +8 mo |
| R&D compute cut 3x | Nov 2027 | Sep 2027 to Mar 2028 | 59% | 99% | 100% | +4 mo | +6 mo |
| Comprehension audits (central) + 3-month lag | Nov 2027 | Sep 2027 to Dec 2027 | 79% | 100% | 100% | +3 mo | +4 mo |
| Comprehension audits (central) + 9-month lag | Mar 2028 | Feb 2028 to Apr 2028 | 9% | 99% | 100% | +8 mo | +8 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2028 | By start of 2029 | By start of 2030 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Sep 2027 | Jul 2027 to Dec 2027 | 75% | 95% | 98% |  |  |
| Human sign-off, no comprehension standard | Sep 2027 | Jul 2027 to Dec 2027 | 75% | 95% | 98% | +0 mo | +0 mo |
| Comprehension audits, light | Oct 2027 | Jul 2027 to Jan 2028 | 72% | 95% | 98% | +0 mo | +1 mo |
| Comprehension audits, central | Oct 2027 | Jul 2027 to Feb 2028 | 66% | 94% | 98% | +1 mo | +2 mo |
| Comprehension audits, strict | Nov 2027 | Aug 2027 to Mar 2028 | 60% | 93% | 98% | +2 mo | +3 mo |
| Internal-use lag, 3 months | Feb 2028 | Nov 2027 to Jun 2028 | 36% | 93% | 98% | +5 mo | +6 mo |
| Internal-use lag, 9 months | Sep 2028 | May 2028 to Jan 2029 | 1% | 73% | 95% | +11 mo | +13 mo |
| R&D compute cut 3x | Feb 2028 | Oct 2027 to Jul 2028 | 41% | 89% | 96% | +5 mo | +7 mo |
| Comprehension audits (central) + 3-month lag | Mar 2028 | Dec 2027 to Jul 2028 | 34% | 89% | 98% | +5 mo | +6 mo |
| Comprehension audits (central) + 9-month lag | Sep 2028 | Jun 2028 to Feb 2029 | 1% | 69% | 93% | +11 mo | +14 mo |

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
| Nov 1, 2026 or later | 47 | Jul 2027 | Sep 2027 | +1 mo | +1 mo | +5 mo |

## Taste improves +1 SD per year of 2025 progress (slow)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Dec 2029 | Mar 2029 to Nov 2031 | 18% | 67% | 97% |  |  |
| Human sign-off, no comprehension standard | Jan 2030 | Apr 2029 to Jan 2032 | 16% | 67% | 97% | +0 mo | +0 mo |
| Comprehension audits, light | Jun 2030 | Jun 2029 to May 2032 | 12% | 59% | 97% | +3 mo | +4 mo |
| Comprehension audits, central | Oct 2030 | Aug 2029 to Jul 2032 | 10% | 55% | 97% | +5 mo | +8 mo |
| Comprehension audits, strict | Mar 2031 | Jan 2030 to Oct 2032 | 6% | 49% | 96% | +10 mo | +14 mo |
| Internal-use lag, 3 months | May 2030 | Aug 2029 to Feb 2032 | 7% | 59% | 97% | +4 mo | +5 mo |
| Internal-use lag, 9 months | Dec 2030 | Apr 2030 to Aug 2032 | 0% | 52% | 97% | +11 mo | +14 mo |
| R&D compute cut 3x | Jan 2031 | Dec 2029 to Aug 2033 | 7% | 50% | 85% | +13 mo | +20 mo |
| Comprehension audits (central) + 3-month lag | Jan 2031 | Dec 2029 to Sep 2032 | 1% | 50% | 97% | +9 mo | +11 mo |
| Comprehension audits (central) + 9-month lag | Jun 2031 | Jul 2030 to Jan 2033 | 0% | 44% | 97% | +15 mo | +17 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Jan 2033 | Nov 2029 to Dec 2038 | 9% | 36% | 59% |  |  |
| Human sign-off, no comprehension standard | Feb 2033 | Mar 2030 to Dec 2038 | 9% | 33% | 59% | +1 mo | +3 mo |
| Comprehension audits, light | Dec 2033 | Oct 2030 to after 2039 | 8% | 28% | 56% | +5 mo | +16 mo |
| Comprehension audits, central | Aug 2034 | Feb 2031 to after 2039 | 3% | 24% | 54% | +10 mo | +24 mo |
| Comprehension audits, strict | Apr 2035 | Sep 2031 to after 2039 | 2% | 19% | 50% | +16 mo | +33 mo |
| Internal-use lag, 3 months | Jun 2033 | Aug 2030 to Feb 2039 | 2% | 31% | 58% | +5 mo | +7 mo |
| Internal-use lag, 9 months | Feb 2034 | Jul 2031 to Aug 2039 | 0% | 20% | 56% | +14 mo | +18 mo |
| R&D compute cut 3x | Sep 2034 | Oct 2030 to after 2039 | 4% | 26% | 52% | +16 mo | +26 mo |
| Comprehension audits (central) + 3-month lag | Nov 2034 | Jun 2031 to after 2039 | 0% | 20% | 51% | +16 mo | +27 mo |
| Comprehension audits (central) + 9-month lag | May 2035 | Feb 2032 to after 2039 | 0% | 10% | 47% | +25 mo | +37 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Dec 2029 | Dec 2029 |
| No pacing: median date of TED-AI | Jan 2033 | Jan 2033 |
| Central audits: median delay to superhuman AI researcher | +6 mo | +5 mo |
| Central audits: median delay to TED-AI | +11 mo | +10 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +11 days and TED-AI by +5 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Dec 2030 | Apr 2034 | +3 mo | +6 mo | +5 mo |
| Nov 1, 2026 or later | 47 | Jul 2029 | Aug 2031 | +6 mo | +14 mo | +5 mo |

## Supervisable tasks improve +3 SD and HTS fuzzy tasks +1 SD per year of 2025 progress (split_3_1)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Oct 2027 | Aug 2027 to Mar 2028 | 100% | 100% | 100% |  |  |
| Human sign-off, no comprehension standard | Oct 2027 | Aug 2027 to Mar 2028 | 100% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, light | Nov 2027 | Aug 2027 to Mar 2028 | 100% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, central | Nov 2027 | Aug 2027 to Mar 2028 | 100% | 100% | 100% | +0 mo | +1 mo |
| Comprehension audits, strict | Dec 2027 | Sep 2027 to Apr 2028 | 100% | 100% | 100% | +1 mo | +2 mo |
| Internal-use lag, 3 months | Feb 2028 | Dec 2027 to Jun 2028 | 99% | 100% | 100% | +3 mo | +4 mo |
| Internal-use lag, 9 months | Aug 2028 | Jun 2028 to Nov 2028 | 85% | 100% | 100% | +9 mo | +10 mo |
| R&D compute cut 3x | Apr 2028 | Dec 2027 to Oct 2028 | 81% | 100% | 100% | +5 mo | +8 mo |
| Comprehension audits (central) + 3-month lag | Mar 2028 | Dec 2027 to Jun 2028 | 99% | 100% | 100% | +4 mo | +4 mo |
| Comprehension audits (central) + 9-month lag | Aug 2028 | Jun 2028 to Nov 2028 | 84% | 100% | 100% | +9 mo | +10 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Jul 2028 | Oct 2027 to Jun 2029 | 66% | 89% | 94% |  |  |
| Human sign-off, no comprehension standard | Jul 2028 | Nov 2027 to Jun 2029 | 64% | 89% | 94% | +0 mo | +0 mo |
| Comprehension audits, light | Aug 2028 | Nov 2027 to Aug 2029 | 62% | 85% | 93% | +0 mo | +1 mo |
| Comprehension audits, central | Sep 2028 | Dec 2027 to Sep 2029 | 58% | 85% | 93% | +1 mo | +3 mo |
| Comprehension audits, strict | Nov 2028 | Feb 2028 to Oct 2029 | 54% | 83% | 93% | +3 mo | +5 mo |
| Internal-use lag, 3 months | Jan 2029 | May 2028 to Nov 2029 | 50% | 86% | 94% | +5 mo | +6 mo |
| Internal-use lag, 9 months | Sep 2029 | Nov 2028 to Sep 2030 | 30% | 81% | 92% | +13 mo | +15 mo |
| R&D compute cut 3x | Mar 2029 | Mar 2028 to May 2030 | 45% | 79% | 92% | +8 mo | +13 mo |
| Comprehension audits (central) + 3-month lag | Feb 2029 | May 2028 to Feb 2030 | 46% | 84% | 93% | +6 mo | +8 mo |
| Comprehension audits (central) + 9-month lag | Oct 2029 | Nov 2028 to Nov 2030 | 30% | 76% | 92% | +13 mo | +17 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Oct 2027 | Oct 2027 |
| No pacing: median date of TED-AI | Jun 2028 | Jul 2028 |
| Central audits: median delay to superhuman AI researcher | +1 mo | +0 mo |
| Central audits: median delay to TED-AI | +2 mo | +1 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +10 days and TED-AI by +6 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Dec 2027 | Oct 2028 | +0 mo | +1 mo | +4 mo |
| Nov 1, 2026 or later | 47 | Oct 2027 | Mar 2028 | +0 mo | +1 mo | +5 mo |

## Supervisable tasks improve +3 SD and HTS fuzzy tasks +0.5 SD per year of 2025 progress (split_3_0.5)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | May 2028 | Nov 2027 to Mar 2029 | 71% | 93% | 98% |  |  |
| Human sign-off, no comprehension standard | May 2028 | Nov 2027 to Mar 2029 | 71% | 93% | 98% | +0 mo | +0 mo |
| Comprehension audits, light | Jun 2028 | Nov 2027 to Mar 2029 | 70% | 93% | 98% | +0 mo | +0 mo |
| Comprehension audits, central | Jun 2028 | Dec 2027 to Apr 2029 | 70% | 92% | 98% | +0 mo | +1 mo |
| Comprehension audits, strict | Jul 2028 | Jan 2028 to Jul 2029 | 66% | 90% | 98% | +2 mo | +3 mo |
| Internal-use lag, 3 months | Aug 2028 | Mar 2028 to Aug 2029 | 60% | 92% | 98% | +3 mo | +4 mo |
| Internal-use lag, 9 months | Mar 2029 | Sep 2028 to Mar 2030 | 39% | 88% | 98% | +9 mo | +11 mo |
| R&D compute cut 3x | Jan 2029 | May 2028 to Feb 2030 | 48% | 83% | 96% | +7 mo | +11 mo |
| Comprehension audits (central) + 3-month lag | Sep 2028 | Apr 2028 to Aug 2029 | 59% | 90% | 98% | +4 mo | +5 mo |
| Comprehension audits (central) + 9-month lag | Mar 2029 | Oct 2028 to Mar 2030 | 39% | 88% | 98% | +9 mo | +11 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Jul 2032 | Sep 2028 to May 2039 | 30% | 43% | 61% |  |  |
| Human sign-off, no comprehension standard | Jul 2032 | Sep 2028 to Jun 2039 | 30% | 43% | 60% | +0 mo | +0 mo |
| Comprehension audits, light | Jul 2032 | Sep 2028 to Oct 2039 | 28% | 42% | 57% | +1 mo | +3 mo |
| Comprehension audits, central | Aug 2032 | Oct 2028 to after 2039 | 28% | 42% | 57% | +2 mo | +6 mo |
| Comprehension audits, strict | Dec 2032 | Feb 2029 to after 2039 | 25% | 41% | 56% | +5 mo | +14 mo |
| Internal-use lag, 3 months | Oct 2032 | Feb 2029 to Jun 2039 | 24% | 42% | 60% | +4 mo | +5 mo |
| Internal-use lag, 9 months | Mar 2033 | Dec 2029 to Sep 2039 | 10% | 39% | 57% | +10 mo | +13 mo |
| R&D compute cut 3x | Jan 2034 | Mar 2029 to after 2039 | 22% | 43% | 55% | +11 mo | +23 mo |
| Comprehension audits (central) + 3-month lag | Oct 2032 | Feb 2029 to after 2039 | 23% | 41% | 57% | +6 mo | +9 mo |
| Comprehension audits (central) + 9-month lag | Sep 2033 | Dec 2029 to after 2039 | 9% | 39% | 56% | +13 mo | +17 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Apr 2028 | May 2028 |
| No pacing: median date of TED-AI | Jul 2032 | Jul 2032 |
| Central audits: median delay to superhuman AI researcher | +1 mo | +0 mo |
| Central audits: median delay to TED-AI | +3 mo | +2 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +21 days and TED-AI by +19 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Oct 2028 | Jan 2034 | +0 mo | +2 mo | +3 mo |
| Nov 1, 2026 or later | 47 | Jan 2028 | Sep 2029 | +1 mo | +2 mo | +4 mo |

## Supervisable tasks improve +2.1 SD and HTS fuzzy tasks +1 SD per year of 2025 progress (split_2.1_1)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Mar 2028 | Nov 2027 to Oct 2028 | 83% | 100% | 100% |  |  |
| Human sign-off, no comprehension standard | Mar 2028 | Nov 2027 to Oct 2028 | 83% | 100% | 100% | +0 mo | +0 mo |
| Comprehension audits, light | Apr 2028 | Dec 2027 to Oct 2028 | 83% | 100% | 100% | +0 mo | +1 mo |
| Comprehension audits, central | Apr 2028 | Dec 2027 to Oct 2028 | 83% | 100% | 100% | +1 mo | +1 mo |
| Comprehension audits, strict | Jun 2028 | Feb 2028 to Nov 2028 | 79% | 100% | 100% | +2 mo | +3 mo |
| Internal-use lag, 3 months | Jun 2028 | Mar 2028 to Dec 2028 | 75% | 100% | 100% | +3 mo | +4 mo |
| Internal-use lag, 9 months | Jan 2029 | Oct 2028 to Jun 2029 | 47% | 100% | 100% | +9 mo | +10 mo |
| R&D compute cut 3x | Sep 2028 | May 2028 to Jul 2029 | 55% | 98% | 100% | +7 mo | +10 mo |
| Comprehension audits (central) + 3-month lag | Jul 2028 | Apr 2028 to Dec 2028 | 75% | 100% | 100% | +4 mo | +5 mo |
| Comprehension audits (central) + 9-month lag | Jan 2029 | Oct 2028 to Jun 2029 | 45% | 100% | 100% | +9 mo | +11 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Feb 2029 | Feb 2028 to Apr 2030 | 47% | 78% | 93% |  |  |
| Human sign-off, no comprehension standard | Feb 2029 | Mar 2028 to May 2030 | 47% | 77% | 93% | +0 mo | +0 mo |
| Comprehension audits, light | Mar 2029 | Apr 2028 to Sep 2030 | 44% | 77% | 90% | +1 mo | +2 mo |
| Comprehension audits, central | Apr 2029 | Jun 2028 to Dec 2030 | 42% | 76% | 90% | +2 mo | +4 mo |
| Comprehension audits, strict | Jul 2029 | Aug 2028 to Feb 2031 | 36% | 71% | 89% | +4 mo | +7 mo |
| Internal-use lag, 3 months | Jul 2029 | Oct 2028 to Aug 2030 | 33% | 75% | 92% | +5 mo | +6 mo |
| Internal-use lag, 9 months | Apr 2030 | May 2029 to Jun 2031 | 8% | 66% | 91% | +13 mo | +15 mo |
| R&D compute cut 3x | Jan 2030 | Sep 2028 to Oct 2031 | 31% | 67% | 88% | +10 mo | +16 mo |
| Comprehension audits (central) + 3-month lag | Sep 2029 | Nov 2028 to Apr 2031 | 30% | 72% | 90% | +7 mo | +10 mo |
| Comprehension audits (central) + 9-month lag | Jun 2030 | Jul 2029 to Jan 2032 | 7% | 60% | 89% | +14 mo | +18 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Mar 2028 | Mar 2028 |
| No pacing: median date of TED-AI | Jan 2029 | Feb 2029 |
| Central audits: median delay to superhuman AI researcher | +2 mo | +1 mo |
| Central audits: median delay to TED-AI | +2 mo | +2 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +13 days and TED-AI by +5 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | Jun 2028 | Jul 2029 | +0 mo | +1 mo | +4 mo |
| Nov 1, 2026 or later | 47 | Feb 2028 | Sep 2028 | +1 mo | +2 mo | +5 mo |

## Supervisable tasks improve +2.1 SD and HTS fuzzy tasks +0.5 SD per year of 2025 progress (split_2.1_0.5)

### Superhuman AI researcher

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Jan 2029 | May 2028 to Feb 2030 | 50% | 86% | 98% |  |  |
| Human sign-off, no comprehension standard | Jan 2029 | May 2028 to Feb 2030 | 49% | 86% | 98% | +0 mo | +0 mo |
| Comprehension audits, light | Jan 2029 | May 2028 to Feb 2030 | 48% | 86% | 98% | +0 mo | +1 mo |
| Comprehension audits, central | Jan 2029 | Jun 2028 to Mar 2030 | 48% | 85% | 98% | +1 mo | +1 mo |
| Comprehension audits, strict | Apr 2029 | Aug 2028 to Apr 2030 | 42% | 85% | 98% | +3 mo | +4 mo |
| Internal-use lag, 3 months | May 2029 | Sep 2028 to Apr 2030 | 42% | 84% | 98% | +3 mo | +4 mo |
| Internal-use lag, 9 months | Nov 2029 | Mar 2029 to Oct 2030 | 9% | 81% | 98% | +9 mo | +11 mo |
| R&D compute cut 3x | Sep 2029 | Nov 2028 to May 2031 | 29% | 71% | 96% | +9 mo | +15 mo |
| Comprehension audits (central) + 3-month lag | Jun 2029 | Oct 2028 to May 2030 | 38% | 84% | 98% | +4 mo | +5 mo |
| Comprehension audits (central) + 9-month lag | Dec 2029 | Apr 2029 to Nov 2030 | 8% | 80% | 98% | +10 mo | +12 mo |

### TED-AI

| Scenario | Median date | Middle half of trajectories | By start of 2029 | By start of 2031 | By start of 2035 | Median delay | Delay, upper quartile |
|---|---|---|---|---|---|---|---|
| No pacing | Nov 2033 | Apr 2029 to after 2039 | 17% | 40% | 56% |  |  |
| Human sign-off, no comprehension standard | Nov 2033 | May 2029 to after 2039 | 17% | 39% | 55% | +0 mo | +0 mo |
| Comprehension audits, light | Jan 2034 | Jun 2029 to after 2039 | 14% | 38% | 55% | +1 mo | +3 mo |
| Comprehension audits, central | Jul 2034 | Aug 2029 to after 2039 | 12% | 38% | 54% | +3 mo | +7 mo |
| Comprehension audits, strict | Jan 2035 | Nov 2029 to after 2039 | 9% | 36% | 50% | +7 mo | +15 mo |
| Internal-use lag, 3 months | Dec 2033 | Oct 2029 to after 2039 | 8% | 38% | 55% | +3 mo | +5 mo |
| Internal-use lag, 9 months | Jul 2034 | Jun 2030 to after 2039 | 1% | 32% | 53% | +11 mo | +14 mo |
| R&D compute cut 3x | Dec 2035 | Jan 2030 to after 2039 | 8% | 36% | 47% | +12 mo | +25 mo |
| Comprehension audits (central) + 3-month lag | Oct 2034 | Nov 2029 to after 2039 | 7% | 36% | 51% | +6 mo | +10 mo |
| Comprehension audits (central) + 9-month lag | Feb 2035 | Jul 2030 to after 2039 | 1% | 28% | 50% | +13 mo | +19 mo |

### What the link from comprehension to judgment changes

| | Link off | Link on |
|---|---|---|
| No pacing: median date of superhuman AI researcher | Dec 2028 | Jan 2029 |
| No pacing: median date of TED-AI | Nov 2033 | Nov 2033 |
| Central audits: median delay to superhuman AI researcher | +2 mo | +1 mo |
| Central audits: median delay to TED-AI | +4 mo | +3 mo |

Paired across trajectories, the link moves the no-pacing date of the superhuman AI researcher by a median of +28 days and TED-AI by +22 days.

### Split by when coding is fully automated

| Automated coder | Trajectories | No pacing: median superhuman AI researcher | No pacing: median TED-AI | Central audits: median delay to superhuman AI researcher | Central audits: median delay to TED-AI | 3-month lag: median delay to TED-AI |
|---|---|---|---|---|---|---|
| Before Nov 1, 2026 | 49 | May 2029 | Jan 2035 | +1 mo | +2 mo | +3 mo |
| Nov 1, 2026 or later | 47 | Aug 2028 | Feb 2030 | +1 mo | +3 mo | +4 mo |
