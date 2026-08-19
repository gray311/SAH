---
name: discovery-optimization
description: "Targeted mutation search for Erdos minimum overlap: analyze current solution,\ngenerate systematic mutations, probe to rank, evaluate winners"
---

# Erdos Minimum Overlap - Targeted Mutation Strategy

## Why This Works
The current harness stuck because it only offered static constructions. We need to:
1. Analyze what the current best solution looks like
2. Systematically mutate specific features
3. Use probe-based search to efficiently find improvements

## Step-by-Step Workflow

### Step 1: Analyze Current Best
Call analyze_current_best() FIRST. This gives you:
- Number of peaks detected
- Peak positions and widths
- Integral value (should be ~1)
- Current c5 bound

### Step 2: Generate Targeted Mutations
Call analyze_and_mutate() with the analysis. It generates mutants that:
- Shift peaks: Move each detected peak by small amounts (-0.05 to +0.05)
- Adjust widths: Widen or narrow each peak by 10-30%
- Try bimodal splits: Create new 2-peak functions at splits 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8
- Asymmetric variants: Make one peak wider than the other
- Phase shifts: Create patterns like peak at (x, x+1) for various x

### Step 3: Probe-Based Search
For each mutant, call probe_solution() to quickly get approximate c5 bound.
This is cheap (seconds vs minutes) and lets you rank many candidates.

### Step 4: Evaluate Winners
Take top 2-3 candidates by probe score and call evaluate_solution() for final confirmation.

## Key Principles
- Always start with analysis, don't just mutate randomly
- Use probes to screen, only full eval for winners
- Focus mutations on the actual structure of current best, not generic patterns
- Track: you likely have 1-2 peaks; try moving them closer/farther
- Bimodal at midpoint (1.0 split) is a good baseline to beat
