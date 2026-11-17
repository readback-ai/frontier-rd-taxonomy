# Work that needs a person: what is reported, and how far the result depends on it

Written by `residue_sensitivity.py`. Do not edit by hand.

## What three developers report

| Source | Measure | Earlier | Latest |
|---|---|---|---|
| OpenAI | Tasks under 15 minutes that needed an intervention or failed | 9% to 20% in each month from March to July 2026 | 14%, January to July 2026 pooled |
| Google DeepMind, Gemini 4 Argon | Tasks under 15 minutes that needed an intervention or failed | | 18% of 114 tasks |
| Anthropic | Sessions on trivial tasks that needed a correction | 20% in Sep 2025 | 12% in Sep 2026 |
| Anthropic | Sessions on routine tasks that needed a correction | 34% in Sep 2025 | 8% in Sep 2026 |
| Anthropic | Sessions on substantial tasks that needed a correction | 61% in Sep 2025 | 8% in Sep 2026 |
| Anthropic | Sessions on open-ended tasks that needed a correction | 80% in Sep 2025 | 9% in Sep 2026 |

OpenAI's monthly values and Anthropic's values were read by eye from charts, to about 2 points.

## Sensitivity on AI Futures' Nov 10 example trajectory

Supervisable tasks improve 3 SD per year of 2025 progress. The link from comprehension to human judgment is on. Pacing starts Jan 1, 2027. Each row changes one input of the central case.

### HTS fuzzy tasks at +1 SD (split_3_1)

| Case | No pacing: superhuman AI researcher | No pacing: TED-AI | Central audits: delay to TED-AI | Audits at 3.5 times the hours: delay to superhuman AI researcher | Audits at 3.5 times the hours: delay to TED-AI | 9-month lag: delay to TED-AI |
|---|---|---|---|---|---|---|
| No work needs a person | Nov 2027 | Mar 2028 | +4 mo | +3 mo | +9 mo | +17 mo |
| Central: 14% of work, supervised at 0.5% of its time | Dec 2027 | May 2028 | +2 mo | +3 mo | +7 mo | +16 mo |
| Starting share 7% | Dec 2027 | Apr 2028 | +2 mo | +3 mo | +8 mo | +16 mo |
| Starting share 28% | Dec 2027 | Jun 2028 | +2 mo | +3 mo | +7 mo | +16 mo |
| Supervised at 4.0% of its time | Feb 2028 | Aug 2028 | +1 mo | +2 mo | +6 mo | +16 mo |
| Supervised at 2.0% of its time | Jan 2028 | Jul 2028 | +1 mo | +3 mo | +6 mo | +16 mo |
| Supervised at 1.0% of its time | Dec 2027 | Jun 2028 | +2 mo | +3 mo | +7 mo | +16 mo |
| Supervised at 0.1% of its time | Nov 2027 | Apr 2028 | +3 mo | +3 mo | +8 mo | +16 mo |
| Share halves per 1 SD of judgment the AI gains | Nov 2027 | Apr 2028 | +2 mo | +3 mo | +8 mo | +16 mo |
| Share halves per 0.5 SD of judgment the AI gains | Nov 2027 | Mar 2028 | +3 mo | +3 mo | +9 mo | +16 mo |

### HTS fuzzy tasks at +0.5 SD (split_3_0.5)

| Case | No pacing: superhuman AI researcher | No pacing: TED-AI | Central audits: delay to TED-AI | Audits at 3.5 times the hours: delay to superhuman AI researcher | Audits at 3.5 times the hours: delay to TED-AI | 9-month lag: delay to TED-AI |
|---|---|---|---|---|---|---|
| No work needs a person | Feb 2028 | Oct 2029 | +23 mo | +5 mo | +41 mo | +19 mo |
| Central: 14% of work, supervised at 0.5% of its time | Mar 2028 | Apr 2031 | +8 mo | +4 mo | +25 mo | +16 mo |
| Starting share 7% | Mar 2028 | Jan 2031 | +10 mo | +4 mo | +27 mo | +17 mo |
| Starting share 28% | Apr 2028 | Jul 2031 | +7 mo | +4 mo | +23 mo | +16 mo |
| Supervised at 4.0% of its time | Jun 2028 | Mar 2032 | +5 mo | +3 mo | +19 mo | +15 mo |
| Supervised at 2.0% of its time | May 2028 | Oct 2031 | +6 mo | +3 mo | +21 mo | +16 mo |
| Supervised at 1.0% of its time | Apr 2028 | Jul 2031 | +7 mo | +4 mo | +23 mo | +16 mo |
| Supervised at 0.1% of its time | Feb 2028 | Oct 2030 | +12 mo | +4 mo | +30 mo | +17 mo |
| Share halves per 1 SD of judgment the AI gains | Mar 2028 | Nov 2030 | +11 mo | +4 mo | +28 mo | +16 mo |
| Share halves per 0.5 SD of judgment the AI gains | Feb 2028 | Apr 2030 | +17 mo | +5 mo | +35 mo | +18 mo |
