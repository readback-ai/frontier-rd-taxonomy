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

Crisp tasks improve 3 SD per year of 2025 progress. The link from comprehension to human judgment is on. Pacing starts Jan 1, 2027. Each row changes one input of the central case.

### Fuzzy tasks at +1 SD (split_3_1)

| Case | No pacing: superhuman AI researcher | No pacing: TED-AI | Central audits: delay to TED-AI | Audits at 3.5 times the hours: delay to superhuman AI researcher | Audits at 3.5 times the hours: delay to TED-AI | 9-month lag: delay to TED-AI |
|---|---|---|---|---|---|---|
| No work needs a person | Feb 2028 | Jul 2028 | +8 mo | +5 mo | +16 mo | +19 mo |
| Central: 14% of work, supervised at 0.5% of its time | Mar 2028 | Nov 2028 | +5 mo | +4 mo | +14 mo | +18 mo |
| Starting share 7% | Mar 2028 | Oct 2028 | +6 mo | +5 mo | +14 mo | +18 mo |
| Starting share 28% | Apr 2028 | Dec 2028 | +5 mo | +4 mo | +13 mo | +18 mo |
| Supervised at 4.0% of its time | Jun 2028 | Mar 2029 | +4 mo | +3 mo | +11 mo | +18 mo |
| Supervised at 2.0% of its time | Apr 2028 | Jan 2029 | +4 mo | +4 mo | +12 mo | +19 mo |
| Supervised at 1.0% of its time | Apr 2028 | Dec 2028 | +5 mo | +4 mo | +13 mo | +18 mo |
| Supervised at 0.1% of its time | Feb 2028 | Sep 2028 | +6 mo | +5 mo | +15 mo | +19 mo |
| Share halves per 1 SD of judgment the AI gains | Feb 2028 | Oct 2028 | +5 mo | +5 mo | +14 mo | +18 mo |
| Share halves per 0.5 SD of judgment the AI gains | Feb 2028 | Aug 2028 | +7 mo | +5 mo | +16 mo | +18 mo |

### Fuzzy tasks at +0.5 SD (split_3_0.5)

| Case | No pacing: superhuman AI researcher | No pacing: TED-AI | Central audits: delay to TED-AI | Audits at 3.5 times the hours: delay to superhuman AI researcher | Audits at 3.5 times the hours: delay to TED-AI | 9-month lag: delay to TED-AI |
|---|---|---|---|---|---|---|
| No work needs a person | Nov 2028 | Feb 2034 | +57 mo | +16 mo | past 2039 | +14 mo |
| Central: 14% of work, supervised at 0.5% of its time | Jul 2029 | Mar 2036 | +35 mo | +10 mo | past 2039 | +15 mo |
| Starting share 7% | Jun 2029 | Nov 2035 | +38 mo | +10 mo | past 2039 | +15 mo |
| Starting share 28% | Sep 2029 | Jul 2036 | +32 mo | +9 mo | past 2039 | +15 mo |
| Supervised at 4.0% of its time | Feb 2030 | Jun 2037 | +25 mo | +7 mo | past 2039 | +16 mo |
| Supervised at 2.0% of its time | Nov 2029 | Dec 2036 | +28 mo | +8 mo | past 2039 | +15 mo |
| Supervised at 1.0% of its time | Sep 2029 | Jul 2036 | +32 mo | +9 mo | past 2039 | +15 mo |
| Supervised at 0.1% of its time | Apr 2029 | Jun 2035 | +42 mo | +11 mo | past 2039 | +16 mo |
| Share halves per 1 SD of judgment the AI gains | May 2029 | Jun 2036 | +31 mo | +11 mo | past 2039 | +12 mo |
| Share halves per 0.5 SD of judgment the AI gains | Feb 2029 | Dec 2034 | +48 mo | +13 mo | past 2039 | +15 mo |
