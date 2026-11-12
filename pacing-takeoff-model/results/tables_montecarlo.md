# Model B Monte Carlo

Written by `montecarlo_b.py`. Do not edit by hand.

79 of 3851 sampled trajectories (2.1%) had a pace of 1.5x to 2x on Nov 1, 2026 and are kept. Parameters are drawn from AI Futures' August 2026 distribution for Daniel (`config/sampling_config_q2_daniel.yaml`), seed 20261110. Median pace of the kept trajectories: 1.68x. Delays are paired: each trajectory under a scenario against the same trajectory with no pacing.

## All kept trajectories

| Scenario | Median TED-AI | Middle half of trajectories | Median delay | Delay, upper quartile | Median SAR | Median ASI |
|---|---|---|---|---|---|---|
| No pacing | May 2027 | Jan 2027 to Dec 2027 | +0 mo | +0 mo | Jan 2027 | Aug 2027 |
| Human sign-off, no comprehension standard | May 2027 | Jan 2027 to Jan 2028 | +0 mo | +0 mo | Jan 2027 | Aug 2027 |
| Comprehension audits, light | May 2027 | Feb 2027 to Jan 2028 | +0 mo | +1 mo | Jan 2027 | Sep 2027 |
| Comprehension audits, central | May 2027 | Feb 2027 to Jan 2028 | +0 mo | +1 mo | Jan 2027 | Oct 2027 |
| Comprehension audits, strict | May 2027 | Feb 2027 to Mar 2028 | +0 mo | +2 mo | Jan 2027 | Oct 2027 |
| Internal-use lag, 3 months | Aug 2027 | Mar 2027 to May 2028 | +3 mo | +5 mo | Feb 2027 | Mar 2028 |
| Internal-use lag, 9 months | Dec 2027 | Mar 2027 to Jan 2029 | +7 mo | +12 mo | Feb 2027 | Oct 2028 |
| R&D compute cut 3x | Aug 2027 | Mar 2027 to Jun 2028 | +3 mo | +6 mo | Feb 2027 | Jan 2028 |
| Comprehension audits (central) + 3-month lag | Aug 2027 | Mar 2027 to Aug 2028 | +3 mo | +7 mo | Feb 2027 | Apr 2028 |
| Comprehension audits (central) + 9-month lag | Jan 2028 | Mar 2027 to Mar 2029 | +7 mo | +14 mo | Feb 2027 | Nov 2028 |

## Trajectories with no superhuman AI researcher before Nov 1, 2026 (61 of 79)

| Scenario | Median TED-AI | Middle half of trajectories | Median delay | Delay, upper quartile | Median SAR | Median ASI |
|---|---|---|---|---|---|---|
| No pacing | Jul 2027 | Mar 2027 to Jan 2028 | +0 mo | +0 mo | Mar 2027 | Sep 2027 |
| Human sign-off, no comprehension standard | Jul 2027 | Mar 2027 to Jan 2028 | +0 mo | +0 mo | Mar 2027 | Sep 2027 |
| Comprehension audits, light | Jul 2027 | Mar 2027 to Jun 2028 | +0 mo | +1 mo | Mar 2027 | Sep 2027 |
| Comprehension audits, central | Jul 2027 | Mar 2027 to Aug 2028 | +0 mo | +2 mo | Mar 2027 | Oct 2027 |
| Comprehension audits, strict | Aug 2027 | Mar 2027 to Aug 2028 | +1 mo | +3 mo | Mar 2027 | Nov 2027 |
| Internal-use lag, 3 months | Nov 2027 | May 2027 to Jul 2028 | +4 mo | +5 mo | Apr 2027 | Apr 2028 |
| Internal-use lag, 9 months | Apr 2028 | Sep 2027 to Feb 2029 | +9 mo | +13 mo | Jul 2027 | Jan 2029 |
| R&D compute cut 3x | Oct 2027 | Apr 2027 to Jul 2028 | +3 mo | +7 mo | May 2027 | Jan 2028 |
| Comprehension audits (central) + 3-month lag | Nov 2027 | May 2027 to Oct 2028 | +4 mo | +8 mo | Apr 2027 | Apr 2028 |
| Comprehension audits (central) + 9-month lag | Apr 2028 | Sep 2027 to Apr 2029 | +9 mo | +16 mo | Jul 2027 | Feb 2029 |
