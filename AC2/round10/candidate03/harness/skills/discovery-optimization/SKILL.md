---
name: discovery-optimization
description: "Escape local optima in step function optimization. Analyze current structure, then generate and probe completely new step function architectures (different number of steps, asymmetric layouts, new peaked patterns) rather than just tweaking existing parameters. Only evaluate the most promising new architectures."
---

# Step Function Architecture Search for C2

## Phase 1: Analysis
1. Call analyze_step_params once to understand current heights and structure
2. Note the total number of step levels and their distribution

## Phase 2: Generate New Architectures
Create NEW step patterns with fundamentally different structures using generate_step_architectures:

### Architecture A: Narrow Central Peak
- Fewer total steps (10-15 levels)
- Very narrow central peak (5-10% of domain)
- Low surrounding plateaus (0.3-0.5 height)

### Architecture B: Asymmetric Multi-peak
- 3-5 steps of varying heights, not symmetric
- Different heights on left vs right side

### Architecture C: Flat-top with Corners
- Wide plateau (60-80% of domain) at medium height
- Sharp transitions at edges

### Architecture D: Multiple Small Peaks
- 4-6 small peaks (5-8% width each) scattered across domain
- Heights: 1.5-2.0 each

## Phase 3: Probe and Evaluate
1. Generate 3-5 different new architectures using generate_step_architectures
2. Call probe_solution on each with a function parameter tweak (±0.05-0.1 height)
3. Track probe scores
4. Call evaluate_solution on the 1-2 architectures with highest probe scores
5. If evaluation improves score, proceed to next phase; if not, generate even more diverse architectures

## Phase 4: Iteration
- After each successful evaluation, analyze the new best pattern
- Generate variants that preserve the successful structure but vary details
- Continue probing until budget exhausted or no new patterns found
