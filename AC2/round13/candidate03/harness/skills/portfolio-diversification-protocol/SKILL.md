---
name: portfolio-diversification-protocol
description: Mandatory diversity protocol with probe-based filtering and automatic stale detection. Forces exploration across function families when stuck in local optima.
---

# C2 Maximizer: Mandatory Portfolio Diversification Protocol

## THE PROBLEM: You're Stuck in a Local Optimum

The step-function solutions (13 patterns) are LOCAL optima. Every time you refine
the same pattern class, you get diminishing returns. You ARE STUCK if you keep making
tiny edits to the same function family without beating 1.03841.

## THE SOLUTION: Parallel Diversity with Probe Filtering

### Rule 1: Generate Diversity Early
At iteration 1-2, call generate_candidates to get 4-6 function proposals across DIFFERENT families.
Do NOT start by refining the seed's step patterns.

### Rule 2: Probe Everything Before Evaluating
You have 30 probes. Use them WISELY but AGGRESSIVELY:
- For each NEW function proposal, call probe_solution FIRST
- Rank proposals by probe score
- Only call evaluate_solution on top 3-5 proposals by probe score
- SKIP any proposal with probe score < current best (1.03841)

### Rule 3: Track and Diversify When Stuck
Track these stats mentally:
- Consecutive evaluations on current family: ?
- Best score for current family: ?
- Number of different families tried: ?

YOU ARE STUCK (and MUST diversify) if ANY of:
1. 3+ consecutive evaluations on SAME family with no improvement
2. 2+ evaluations on same family without beating 1.03841
3. 15+ iterations without trying a new family
4. Last 3 evaluated patterns all scored < 1.03841

When stuck:
1. Call analyze_function_class to understand why
2. Call generate_candidates with orthogonal families
3. Probe and filter quickly
4. Evaluate only the best 3-4 proposals

### Rule 4: One Evaluation Per Variant
Each evaluate_solution call tests ONE function. Make sure it's COMPLETELY SPECIFIED.
Do not chain multiple variants in one edit. Do not re-evaluate the same function.

### Rule 5: Grace Period After Success
If you beat 1.03841, you get a 2-eval grace period. After that, diversify again.
Do not over-refine a successful family - it's likely also a local optimum.

### Rule 6: Hybridization as Last Resort
If multiple families show promise (probe scores within 10% of best) but none beat the record:
- Extract structural elements from successful families
- Create hybrids (e.g., Gaussian core with step wings)
- Probe and evaluate hybrids

## Summary: PORTFOLIO > SINGLE FAMILY

- Generate diverse candidates -> Probe filter -> Evaluate top 3-5 -> Track family stats -> Diversify when stuck
- Your goal is to FIND A NEW FUNCTION CLASS, not refine step functions.
- 30 probes are your main weapon. Don't waste them, but use them to filter aggressively.
