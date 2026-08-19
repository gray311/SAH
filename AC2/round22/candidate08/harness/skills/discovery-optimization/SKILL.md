---
name: discovery-optimization
description: "Pattern enumeration for step-function optimization. Systematically try seed's 12+ patterns, refine best, then gradient escape. Avoid tiny perturbations - try structural changes first."
---

# C2 Maximizer: Pattern Enumeration + Hybrid Refinement
## Core Principle
The seed program defines 12+ step patterns. Most harnesses fail because they perturb parameters without changing the underlying structure. You must systematically enumerate patterns first, then refine.
## Phase 1: Step Pattern Enumeration (iterations 1-12)
Step 1: Identify Active Pattern
- Examine your current best function - Find which pattern index (0-11) it most resembles - If ambiguous: use scan_step_patterns to enumerate all patterns
Step 2: Generate 4 Targeted Variants
For the active pattern, create EXACTLY 4 variants:
Variant A (Height Boost): - Increase the central/tallest peak height by 5% - Example: if peak=1.50, new height=1.575
Variant B (Widen Peak): - Shift start index INWARD by 2% of domain - Shift end index INWARD by 2% of domain - This widens the peak while keeping height constant
Variant C (Narrow + Boost): - Narrow peak by shifting start/end INWARD by 3% - Increase height by 0.15 - This creates a sharper, taller peak
Variant D (Structural Change): - If single peak: split into 2-peak configuration - If multiple peaks: make one peak 10% taller and one 10% shorter - This tests asymmetry hypothesis
Step 3: Probe All Variants
- Call probe_solution on ALL 4 variants - Rank by probe score (higher c2 is better) - Call evaluate_solution on TOP 1 only
Step 4: Iterate
- If beats record (score > 1.042): refine this pattern - If no improvement after 3 iterations: switch to Phase 2
## Phase 2: Systematic Pattern Scan (iterations 13-20)
Step 1: Enumerate Patterns
- If you have not done so, call scan_step_patterns - This lists patterns 0-11 with their key characteristics
Step 2: Try Untried Patterns
- For each pattern not yet tried: create a variant with +2% height boost - Probe all new pattern variants - Evaluate the best one
Step 3: Refine Winner
- If a new pattern beats record: refine it with gradient methods (Phase 3)
## Phase 3: Gradient Escape (iterations 21-25)
Step 1: Large Gradient Steps
- Use @jax.grad on -c2_ratio - Take larger step: new_param = param + 0.1 * gradient - This helps escape local optima
Step 2: Probe and Evaluate
- Generate 2 variants (ascent and descent) - Probe both, evaluate best - If gradient norm < 0.005: switch to Phase 4
## Phase 4: Final Dive (iterations 26-30)
Step 1: Aggressive Reinitialization
- Keep the target c2 you found - Reinitialize 80% of parameters with std=0.05*value - Create 3 variants
Step 2: Final Evaluation
- Probe all 3, evaluate best - Submit if c2 > 0.8962799441554086
## Key Rules
- SYSTEMATICALLY try patterns before perturbations - Use probes to filter: 4 probes before any eval in Phase 1 - If score <= 1.042 after 5 iterations: switch to Phase 2 - Gradient steps should be LARGER (0.1) to escape local optima
