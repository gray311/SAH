---
name: discovery-optimization
description: "C2 maximization via strategic parameter exploration. The seed optimizer already\ncreates step functions; focus on escaping local optima through reinitialization\nstrategy and hyperparameter mutations. Use extensive probing to rank variants\nbefore full evaluation. Escalate reinit_fraction when stuck."
---

# C2 Maximization: Strategic Parameter Exploration

## Critical Insight

The seed program's C2Optimizer already:
- Creates piecewise-constant step functions (NOT linear ramps)
- Uses built-in reinitialization: reinit_fraction=0.18, reinit_std=0.028, reinit_interval=180
- Optimizes over 37000 steps on 400 intervals

Your task is NOT to create step functions - it's to GUIDE THE OPTIMIZER to ESCAPE
LOCAL OPTIMA where it's stuck.

## Escape Strategy

When the optimizer stagnates (likely at the seed's c2 ≈ 0.928):

### Phase 1: Analyze Current State
- Call analyze_hyperparameters to see current settings
- Check if reinit_fraction is too low (0.18 might not escape well)
- Check if num_intervals is limiting (400 might miss finer structures)

### Phase 2: Strategic Mutations
Try these parameter changes when stuck:

**Reinitialization boost** (most important!):
- reinit_fraction: 0.18 → 0.25-0.35 (reset more of the function periodically)
- reinit_std: 0.028 → 0.035-0.05 (larger perturbations on reset)
- reinit_interval: 180 → 250-300 (reset less frequently but more aggressively)

**Structure refinement**:
- num_intervals: 400 → 600-800 (finer discretization for complex steps)
- learning_rate: 0.22 → 0.15-0.18 (more conservative optimization)
- num_steps: 37000 → 45000-55000 (allow more refinement)

**Pattern diversity**:
- Modify _create_step_initializer to try more extreme heights (1.8-2.2 range)
- Add new pattern variants (more peaks, asymmetric distributions)

### Phase 3: Evaluation Discipline
- Call generate_parameter_mutations to get structured suggestions
- Use probe_solution to rank 6-10 variants BEFORE any full evaluation
- Evaluate ONLY the top 2 variants
- If best probe score doesn't beat seed, don't waste evals!

### Phase 4: Escape Protocol
After 5-7 evaluations with no improvement:
- Drastically change reinit_fraction (0.18 → 0.40 or 0.50)
- Change reinit_std (0.028 → 0.06-0.08)
- This forces a different search trajectory

## Common Mistakes
- Wasting edits on step-function creation (seed already does this!)
- Evaluating before probing (wastes precious evals)
- Not using reinitialization aggressively enough
- Using too few num_intervals (limiting structural complexity)
- Random mutations instead of structured parameter sweeps

## Checklist
- [ ] Called analyze_hyperparameters first
- [ ] Proposed structured parameter mutations
- [ ] Probed 6-10 variants before any evaluation
- [ ] Evaluated only top 2
- [ ] Used escape protocol when stuck (high reinit_fraction)
