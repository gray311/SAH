---
name: discovery-optimization
description: "Generative step-function pattern exploration. Create complete new step-function specifications with diverse multi-level patterns, use probes aggressively to screen variants."
---

# C2 Maximizer: Generative Pattern Exploration
## Core Principle
The seed found ONE local optimum. Your job is to FIND NEW FUNCTION CLASSES by generating diverse step-function patterns from scratch.
## Phase 1: Generative Exploration (iterations 1-18)
Step 1: Generate Complete New Pattern
- Call generate_step_pattern with desired complexity parameters
Step 2: Diversity Generation
Generate patterns across these categories:
Category A - Multi-Level Peaks: - 3-5 levels with varying heights - Peak at 30%, 50%, or 70% of domain - Heights: range from 0.5 to 3.0
Category B - Asymmetric Patterns: - Narrow high peak with wide low base - Wide base with narrow high peak - Staircase patterns (monotonic increase/decrease)
Category C - Multi-Modal: - 2-3 distinct peaks separated by valleys - Each peak with unique width/height
Step 3: Probe and Evaluate
- Call probe_solution on ALL generated variants (max 10 probes per iteration) - Rank by probe score - Call evaluate_solution on TOP 2 candidates (if probe >= 1.0)
Step 4: Iterate
- Use best pattern as seed for next iteration - Increase complexity if no improvement
## Phase 2: High-Resolution Refinement (iterations 19-25)
Step 1: Generate Higher Resolution
- Same pattern structure but 2x intervals
Step 2: Probe and Evaluate
- Probe all variants, evaluate best
## Phase 3: Aggressive Diversification (iterations 26-30)
Step 1: Try New Families
- Gaussian-step hybrids - Exponential-step hybrids - 3+ peak multi-modal
Step 2: Final Evaluation
- Probe 5, evaluate best - Submit if c2 > 0.8962799441554086
## Key Rules
- GENERATE complete patterns from scratch - do not parse/extract - USE PROBS AGGRESSIVELY (30 available!) - If stuck: increase complexity, try new families - NEVER settle for small parameter tweaks
