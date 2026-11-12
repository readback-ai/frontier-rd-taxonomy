# What the labs' own usage data change, on one trajectory

Written by `real_research_effect.py`. Do not edit by hand.

## Task length finished with no human intervention

| Source | 80% of the time | Half the time |
|---|---|---|
| OpenAI, January to July 2026 pooled | 15 min | 4.0 h |
| OpenAI, each month from March to July | 9 to 22 min | |
| Google DeepMind, Gemini 4 Argon | 11 min | 1.4 h |
| METR benchmark, Claude Mythos Preview, as the AI Futures Model takes it | 186 min | |

Interpolated between the published buckets in log task length. OpenAI's January and February values are below 80% in every bucket.

## How fast work is handed over

| Series | First value | Last value | Change in log-odds per month |
|---|---|---|---|
| Anthropic, share of work that AI leads | 1.0% in Mar 2026 | 26.0% in Aug 2026 | +0.70 |
| Anthropic, the same without March | 12.0% in May 2026 | 26.0% in Aug 2026 | +0.34 |
| Google DeepMind, fully delegated pull requests (under 3 human turns) | 7.5% in Apr 2026 | 11.9% in Sep 2026 | +0.09 |
| Google DeepMind, over 98% AI-written with under 10 human turns, or better | 18.8% in Apr 2026 | 46.3% in Sep 2026 | +0.26 |

The model's supervision schedule is a logistic in capability fitted to the first series. The delegation rows below fit it to the third.

## Model A, no pacing

| Supervision fitted to | Capability of the superhuman AI researcher reached | Pace in January 2028 | Labor uplift in January 2028 |
|---|---|---|---|
| Anthropic's automation levels | Jul 2027 | off scale | off scale |
| Google DeepMind's fully delegated pull requests | Feb 2028 | 1.3x | 11x |

Model A has no research-judgment term, so the residue rule does not apply to it.

## Model B, AI Futures' Nov 10 example trajectory

The link from comprehension to human judgment is on. Pacing starts Jan 1, 2027. With the residue, 15% of work needs a person on Nov 1, 2026, and that share falls with the share of researchers whose judgment is still better than the AI's.

### Taste improves +3 SD per year of 2025 progress (baseline)

| Supervision | No pacing: superhuman AI researcher | No pacing: TED-AI | Central audits: delay to superhuman AI researcher | Central audits: delay to TED-AI | 3-month lag: delay to TED-AI |
|---|---|---|---|---|---|
| Anthropic's automation levels, no residue (as in earlier sections) | Sep 2027 | Nov 2027 | +0 mo | +1 mo | +5 mo |
| Delegation as Google DeepMind measures it | Jan 2028 | May 2028 | +0 mo | +0 mo | +4 mo |
| Work that needs a person, tied to AI judgment | Sep 2027 | Nov 2027 | +0 mo | +1 mo | +5 mo |
| Both | Jan 2028 | May 2028 | +0 mo | +0 mo | +4 mo |

### Taste improves +1 SD per year of 2025 progress (slow)

| Supervision | No pacing: superhuman AI researcher | No pacing: TED-AI | Central audits: delay to superhuman AI researcher | Central audits: delay to TED-AI | 3-month lag: delay to TED-AI |
|---|---|---|---|---|---|
| Anthropic's automation levels, no residue (as in earlier sections) | Apr 2029 | Sep 2030 | +11 mo | +32 mo | +8 mo |
| Delegation as Google DeepMind measures it | Aug 2031 | Feb 2034 | +2 mo | +7 mo | +7 mo |
| Work that needs a person, tied to AI judgment | May 2030 | Sep 2031 | +4 mo | +24 mo | +8 mo |
| Both | Aug 2031 | Feb 2034 | +2 mo | +7 mo | +7 mo |

### Crisp tasks improve +3 SD and fuzzy tasks +1 SD per year of 2025 progress (split_3_1)

| Supervision | No pacing: superhuman AI researcher | No pacing: TED-AI | Central audits: delay to superhuman AI researcher | Central audits: delay to TED-AI | 3-month lag: delay to TED-AI |
|---|---|---|---|---|---|
| Anthropic's automation levels, no residue (as in earlier sections) | Feb 2028 | Jul 2028 | +1 mo | +8 mo | +8 mo |
| Delegation as Google DeepMind measures it | Nov 2028 | Feb 2030 | +0 mo | +1 mo | +6 mo |
| Work that needs a person, tied to AI judgment | Jun 2028 | Mar 2029 | +0 mo | +4 mo | +8 mo |
| Both | Nov 2028 | Feb 2030 | +0 mo | +1 mo | +6 mo |

### Crisp tasks improve +3 SD and fuzzy tasks +0.5 SD per year of 2025 progress (split_3_0.5)

| Supervision | No pacing: superhuman AI researcher | No pacing: TED-AI | Central audits: delay to superhuman AI researcher | Central audits: delay to TED-AI | 3-month lag: delay to TED-AI |
|---|---|---|---|---|---|
| Anthropic's automation levels, no residue (as in earlier sections) | Nov 2028 | Feb 2034 | +6 mo | +57 mo | +5 mo |
| Delegation as Google DeepMind measures it | Jul 2030 | Jul 2037 | +1 mo | +24 mo | +5 mo |
| Work that needs a person, tied to AI judgment | Mar 2030 | Jun 2037 | +1 mo | +25 mo | +5 mo |
| Both | Aug 2030 | Oct 2037 | +0 mo | +22 mo | +5 mo |

### Crisp tasks improve +2.1 SD and fuzzy tasks +1 SD per year of 2025 progress (split_2.1_1)

| Supervision | No pacing: superhuman AI researcher | No pacing: TED-AI | Central audits: delay to superhuman AI researcher | Central audits: delay to TED-AI | 3-month lag: delay to TED-AI |
|---|---|---|---|---|---|
| Anthropic's automation levels, no residue (as in earlier sections) | May 2028 | Nov 2028 | +2 mo | +10 mo | +8 mo |
| Delegation as Google DeepMind measures it | Jun 2029 | Sep 2030 | +0 mo | +2 mo | +6 mo |
| Work that needs a person, tied to AI judgment | Nov 2028 | Aug 2029 | +1 mo | +5 mo | +8 mo |
| Both | Jun 2029 | Sep 2030 | +0 mo | +2 mo | +6 mo |

### Crisp tasks improve +2.1 SD and fuzzy tasks +0.5 SD per year of 2025 progress (split_2.1_0.5)

| Supervision | No pacing: superhuman AI researcher | No pacing: TED-AI | Central audits: delay to superhuman AI researcher | Central audits: delay to TED-AI | 3-month lag: delay to TED-AI |
|---|---|---|---|---|---|
| Anthropic's automation levels, no residue (as in earlier sections) | Mar 2029 | Jun 2034 | +8 mo | +58 mo | +5 mo |
| Delegation as Google DeepMind measures it | Feb 2031 | Nov 2037 | +1 mo | +24 mo | +5 mo |
| Work that needs a person, tied to AI judgment | Oct 2030 | Oct 2037 | +1 mo | +25 mo | +6 mo |
| Both | Apr 2031 | Mar 2038 | +1 mo | past 2039 | +5 mo |
