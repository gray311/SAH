---
name: discovery-optimization
description: "Systematic step-function topology exploration. Generate diverse multi-level\nstep patterns, use probes to filter before full evaluation. Stay within the\nstep-function paradigm that achieves the current record."
---

# C2 Maximizer: Step-Function Topology Exploration Protocol

## Core Principle
The current best (0.8962799441554086) is achieved by step functions.
Abandoning to incompatible families wastes evaluation budget.
Systematically explore the step-function design space instead.

## Architecture Families (ALL valid step functions)

1. **Multi-peak variants**
   - Wide base with narrow high peak
   - Narrow base with wide high peak
   - Asymmetric single peaks

2. **Multi-level structures** (2-7 levels)
   - Linear progression: ascending/descending steps
   - Symmetric peaks: plateau with higher center
   - Asymmetric peaks: higher left/right side
   - Multiple isolated peaks

3. **Gap-based structures**
   - Central gap with elevated sides
   - Alternating high/low segments
   - Nested gaps

4. **Triangle-like steps**
   - Rising then falling steps
   - Plateau peaks

## Execution Protocol

### Phase 1: Diverse Topology Generation (iterations 1-18)

Step 1: Analyze Current Best
- Note: How many levels? Where are peaks? Symmetric/asymmetric?
- If all levels similar: introduce height variation
- If single peak: try multi-peak
- If symmetric: try asymmetric

Step 2: Generate 5 DIVERSE Step Variants
Use step_topology_generator to create variants with:
- Different number of levels (2-7)
- Heights in range [0.3, 3.0] (ensure non-negative)
- Positions shifted ±10% from centers
- Completely different topologies (not just parameter tweaks)

Step 3: Probe-Based Filtering
- Call probe_solution on ALL 5 variants (5 probes)
- Skip full eval if probe score < 1.0 (worse than seed)
- Evaluate top 2 by probe score

Step 4: Iterate
- If neither beats record: generate 5 MORE diverse variants
- Continue until iteration 18 or improvement

### Phase 2: Focused Refinement (iterations 19-30)

Only if Phase 1 found improvement:
1. Analyze best variant's structure
2. Generate 3 variants with SMALL mutations:
   - Height: ±0.15
   - Width: ±5% of segment
   - Reorder levels
3. Probe all, evaluate top 1
4. If no improvement after 5 iterations: return to Phase 1

## Key Rules
- PARALLEL DIVERSITY > SEQUENTIAL REFINEMENT
- Use 30 probes to explore 10-15+ step-topology variants
- NEVER change FFT-based evaluation structure
- If iteration 15+: ensure maximum topology diversity (not minor tweaks)
- All functions must be non-negative step functions
