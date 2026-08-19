---
name: parameter-escape-strategy
description: Playbook for escaping local optima in C2 optimization. The seed optimizer already creates step functions; focus on strategic hyperparameter mutations, especially boosting reinitialization, to escape poor regions. Use probing to rank variants before evaluation, and escalate reinit_fraction when stuck.
---

# Parameter Escape Strategy for C2 Optimization

## Core Insight

The seed optimizer already creates step functions correctly. It's stuck in a local
optimum at c2 ≈ 0.928. Your job is NOT to create step functions - it's to guide the
optimizer to ESCAPE using strategic reinitialization and parameter mutations.

## Escape Protocol

### When Stagnation Occurs
If the optimizer's best score hasn't improved after ~2000-3000 steps:
1. Call analyze_hyperparameters to see current settings
2. Check reinit_fraction (0.18 likely too low)
3. Escalate with mutations: reinit_fraction → 0.30-0.40, reinit_std → 0.05-0.08

### Parameter Mutation Strategy
Always test these mutation types when improving:

**Reinitialization Boost** (PRIMARY ESCAPE MECHANISM):
- reinit_fraction: 0.18 → 0.30-0.40 (reset 30-40% of function, not 18%)
- reinit_std: 0.028 → 0.05-0.08 (larger perturbations)
- reinit_interval: 180 → 250-300 (less frequent but more aggressive)

**Structure Refinement**:
- num_intervals: 400 → 600-800 (finer discretization)
- num_steps: 37000 → 45000-55000 (more optimization)
- learning_rate: 0.22 → 0.15-0.18 (more careful refinement)

**Pattern Innovation**:
- Modify _create_step_initializer with heights in 1.8-2.2 range
- Add asymmetric patterns, multiple peaks
- Try pyramid shapes, multi-level staircases

### Evaluation Discipline

1. **Analyze First**: Call analyze_hyperparameters before each edit
2. **Generate Mutations**: Call generate_parameter_mutations for structured suggestions
3. **Probe Extensively**: Test 6-10 variants with probe_solution
4. **Evaluate Sparingly**: Only evaluate top 2, and only if probe scores beat seed
5. **Escalate**: After 5-7 evals without improvement, drastically change reinit_fraction

### What NOT to Do
- Don't waste edits on basic step-function creation (seed does this)
- Don't evaluate without probing first
- Don't disable reinitialization (it's your escape hatch!)
- Don't use tiny parameter changes (need big escapes)

## Checklist
- [ ] Called analyze_hyperparameters before edit
- [ ] Proposed mutations focused on reinit boost
- [ ] Probed 6-10 variants before evaluation
- [ ] Evaluated only top 2
- [ ] Used escape protocol (high reinit_fraction) when stuck
