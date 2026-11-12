# Research judgment, data generation and pace: effect on audits

Written by `judgment_sensitivity.py`. Do not edit by hand.

## Varying research judgment on AI Futures' example trajectory

| Case | Pace Nov 2026 | No pacing: SAR | No pacing: TED-AI | Central audits: TED-AI delay | Strict audits: TED-AI delay | 3-month lag: TED-AI delay | Central audits with data-driven progress: TED-AI delay |
|---|---|---|---|---|---|---|---|
| AI Futures' Nov 10 example (judgment +0.5 SD at automated coder, +2.1 SD a year) | 1.72x | Jun 2027 | Oct 2027 | +2 mo | +4 mo | +6 mo | +4 mo |
| Judgment -1 SD at automated coder | 1.56x | Nov 2027 | Feb 2028 | +4 mo | +7 mo | +7 mo | +7 mo |
| Judgment -2.5 SD at automated coder | 1.55x | Mar 2028 | Jul 2028 | +7 mo | +11 mo | +7 mo | +12 mo |
| Judgment improves +1.0 SD a year | 1.80x | Nov 2027 | Mar 2029 | +20 mo | +28 mo | +7 mo | +30 mo |

Data-driven progress: dataset updates grow in proportion to AI labor and carry half of progress (training improvements 0.3, system software 0.2).

## Monte Carlo trajectories split by sampled research judgment

61 trajectories with a pace of 1.5x to 2x on Nov 1, 2026, no superhuman AI researcher by then, and TED-AI reached by 2035 with no pacing.

| Split | Third | Range | No pacing: median SAR | No pacing: median TED-AI | Central audits: median delay | Strict audits: median delay | 3-month lag: median delay |
|---|---|---|---|---|---|---|---|
| Judgment improvement per year | lowest | +0.8 to +2.2 SD | Jun 2027 | Jan 2028 | +2.1 mo | +3.7 mo | +4.9 mo |
| Judgment improvement per year | middle | +2.2 to +3.6 SD | Mar 2027 | Jul 2027 | +0.5 mo | +0.9 mo | +4.1 mo |
| Judgment improvement per year | highest | +3.6 to +17.3 SD | Jan 2027 | Feb 2027 | +0.1 mo | +0.3 mo | +2.2 mo |
| Judgment at automated coder | lowest | -5.1 to -0.9 SD | Jul 2027 | Aug 2027 | +0.9 mo | +1.7 mo | +4.4 mo |
| Judgment at automated coder | middle | -0.8 to +1.7 SD | Mar 2027 | Jul 2027 | +0.7 mo | +1.3 mo | +4.5 mo |
| Judgment at automated coder | highest | +1.9 to +6.5 SD | Dec 2026 | Apr 2027 | +0.1 mo | +0.3 mo | +2.2 mo |

## Monte Carlo by pace on Nov 1, 2026

| Pace band | Trajectories | No pacing: median SAR | No pacing: median TED-AI | Central audits: median delay | Central audits: delayed 6 months or more | Strict audits: median delay | 3-month lag: median delay |
|---|---|---|---|---|---|---|---|
| 1.5x to 2x (METR's central estimate) | 61 | Mar 2027 | Jul 2027 | +0.4 mo | 15% | +0.8 mo | +3.7 mo |
| 1.25x to 1.5x (slower real pace) | 154 | Jun 2027 | Oct 2027 | +0.7 mo | 15% | +1.5 mo | +3.4 mo |

Trajectories with a superhuman AI researcher already on Nov 1, 2026 are excluded. Delays are over trajectories that reach TED-AI by 2035 with no pacing.
