---
name: pattern-first-search
description: Use generate_pattern_candidates to explore diverse initializations before hyperparameter tuning.  This skill implements the pattern-first strategy - generate 8 diverse patterns, screen with probe_solution, evaluate top 2-3, then only if no success, tune hyperparameters.  The key insight is that the seed's patterns may all converge to the same local minimum, so fresh pattern designs are needed to e
---

# Pattern-First Search for Erdos C5

## Core Idea

The seed optimizer's 15 patterns all converge to similar local minima (same score 0.999945).
We need FRESH pattern designs to escape this basin.

## Step-by-Step Workflow

### Step 1: Generate Patterns
1. CALL generate_pattern_candidates() ONCE
   - Returns 8 diverse initializations
   - Each precomputed with integral and c5_bound (no training!)

### Step 2: Screen with Probe
2. Analyze the 8 candidates:
   - Filter: keep only c5_bound < 0.375 (allows ~5% margin)
   - Sort by c5_bound (lowest = best)

### Step 3: Evaluate Top Candidates
3. CALL evaluate_solution on top 2-3 candidates
   - Only if probe suggests improvement
   - Stop early if combined_score > 1.0

### Step 4: If No Success (Optional)
4. Only if all 8 patterns fail to improve:
   - Take BEST pattern from Step 2
   - Vary ONE hyperparameter at a time:
     * num_intervals: 400, 800, 1600, 3200
     * base_learning_rate: 0.001, 0.005, 0.01, 0.02
     * penalty_strength: 20, 40, 60, 80, 120
   - Continue using probe_solution before full eval

## Why This Works

- Fresh pattern designs escape the seed's optimization basin
- 8 diverse patterns cover Golomb, bipartite, tri-modal, uniform bases
- probe_solution allows cheap screening (~10s each) before expensive full eval
- If patterns fail, hyperparameter tuning on best pattern is a fallback

## Success Criteria

- Call generate_pattern_candidates FIRST (before any hyperparameter changes)
- Use probe_solution to screen all 8 candidates
- Evaluate only top 2-3 after probe screening
- If no improvement after 5 patterns, try new pattern set or hyperparameter tuning
