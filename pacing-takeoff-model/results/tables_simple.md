# Simple model: milestone dates by scenario

Written by `simple_model.py`. Do not edit by hand.

Delays are against no pacing. Pacing starts Jan 1, 2027. Critical rate: 2.34 SD per year of progress. Above it the loop runs away on judgment alone.

### One kind of judgment, +3 SD a year

Pace once AI labor is at its ceiling: runs away.

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Aug 2027 |  | Nov 2027 |  |
| Comprehension audits, light | Sep 2027 | +0 mo | Nov 2027 | +0 mo |
| Comprehension audits, central | Sep 2027 | +1 mo | Dec 2027 | +1 mo |
| Comprehension audits, strict | Oct 2027 | +2 mo | Jan 2028 | +3 mo |
| Internal-use lag, 3 months | Dec 2027 | +3 mo | Apr 2028 | +6 mo |
| Internal-use lag, 9 months | Mar 2028 | +6 mo | Oct 2028 | +12 mo |
| R&D compute cut 3x | Dec 2027 | +3 mo | Feb 2028 | +4 mo |
| Comprehension audits (central) + 9-month lag | Mar 2028 | +6 mo | Nov 2028 | +12 mo |

### One kind of judgment, +1 SD a year

Pace once AI labor is at its ceiling: 1.7x.

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Oct 2030 |  | Apr 2033 |  |
| Comprehension audits, light | Oct 2030 | +1 mo | Jun 2035 | +26 mo |
| Comprehension audits, central | Dec 2030 | +2 mo | Sep 2035 | +30 mo |
| Comprehension audits, strict | Mar 2031 | +5 mo | Jan 2036 | +33 mo |
| Internal-use lag, 3 months | Dec 2030 | +2 mo | Jun 2033 | +2 mo |
| Internal-use lag, 9 months | Mar 2031 | +6 mo | Nov 2033 | +7 mo |
| R&D compute cut 3x | Apr 2031 | +6 mo | Oct 2033 | +6 mo |
| Comprehension audits (central) + 9-month lag | May 2031 | +7 mo | Oct 2035 | +30 mo |

### Crisp +3, fuzzy +1 SD a year

Pace once AI labor is at its ceiling: 1.7x.

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Jul 2028 |  | May 2030 |  |
| Comprehension audits, light | Jul 2028 | +0 mo | Sep 2030 | +4 mo |
| Comprehension audits, central | Aug 2028 | +1 mo | Dec 2030 | +7 mo |
| Comprehension audits, strict | Sep 2028 | +2 mo | Mar 2031 | +10 mo |
| Internal-use lag, 3 months | Oct 2028 | +3 mo | Aug 2030 | +3 mo |
| Internal-use lag, 9 months | Jan 2029 | +6 mo | Feb 2031 | +10 mo |
| R&D compute cut 3x | Dec 2028 | +5 mo | Nov 2030 | +6 mo |
| Comprehension audits (central) + 9-month lag | Feb 2029 | +7 mo | Apr 2031 | +11 mo |

### Crisp +3, fuzzy +0.5 SD a year

Pace once AI labor is at its ceiling: 1.3x.

| Scenario | Researcher-level AI | Delay | TED-AI | Delay |
|---|---|---|---|---|
| No pacing | Nov 2030 |  | Oct 2037 |  |
| Comprehension audits, light | Nov 2030 | +0 mo | Jun 2038 | +7 mo |
| Comprehension audits, central | Dec 2030 | +1 mo | Sep 2038 | +11 mo |
| Comprehension audits, strict | Feb 2031 | +3 mo | Jan 2039 | +14 mo |
| Internal-use lag, 3 months | Dec 2030 | +1 mo | Nov 2037 | +1 mo |
| Internal-use lag, 9 months | Jan 2031 | +3 mo | Jan 2038 | +3 mo |
| R&D compute cut 3x | May 2031 | +6 mo | May 2038 | +6 mo |
| Comprehension audits (central) + 9-month lag | Feb 2031 | +4 mo | Sep 2038 | +10 mo |

