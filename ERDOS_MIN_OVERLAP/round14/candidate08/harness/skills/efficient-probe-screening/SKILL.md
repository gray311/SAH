---
name: efficient-probe-screening
description: Use the 30 probes to screen many candidates before spending evaluations.
---

# Efficient Probe Screening

## Budget Strategy
- 30 probes = plenty for initial screening
- Use ALL 30 to test diverse initializations
- Only spend 2-3 full evaluations on promising candidates

## Screening Criteria
Call probe_solution for each candidate and check:
- If probe fails integral constraint (sum != 1), SKIP
- If probe c5_bound >= 0.375, SKIP (too bad)
- If probe c5_bound < 0.37, KEEP for full evaluation

## Expected Outcome
- 15-20 probes will fail (constraint or high c5_bound)
- 5-10 probes will pass and be worth full evaluation
- 2-3 full evaluations will give the answer
