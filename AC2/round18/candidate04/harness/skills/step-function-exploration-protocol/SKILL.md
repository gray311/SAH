---
name: step-function-exploration-protocol
description: Systematically explore step-function topologies to find variants that beat the current record. Focus on multi-level patterns, asymmetric structures, and gap-based designs within the step-function paradigm.
---

# Step-Function Topology Exploration Protocol for C2 Maximization

## Core Principle
The current best (0.8962799441554086) is achieved by step functions.
Systematically explore the step-function design space instead of abandoning
it for incompatible families.

## Architecture Families to Explore

1. **Multi-peak Structures**
   - 2-7 distinct peaks with varying heights
   - Asymmetric peak distributions
   - Multiple peaks with gaps between them

2. **Wide Base + Narrow Peak**
   - Wide low base with narrow high peak(s)
   - Stabilizes integral while boosting sup

3. **Asymmetric Multi-Level**
   - 3-7 levels with non-uniform heights
   - Rising or falling step sequences

4. **Gap-Based Structures**
   - Low regions separating high regions
   - Reduces sup norm through separation

5. **Triangle-Like Stepped Functions**
   - Symmetric or asymmetric rising/falling steps
   - 5-7 level pyramidal structures

## Execution Protocol

### Phase 1: Diverse Topology Generation (iterations 1-18)

1. Generate 5 diverse step-function variants using step_topology_generator
   - Different number of levels (2-7)
   - Heights in range [0.3, 3.0]
   - Completely different topologies
   
2. Probe all 5 variants (5 probes)
   - Skip full eval if probe score < 1.0

3. Evaluate top 2 by probe score

4. If neither beats record: generate 5 MORE diverse variants
   - Ensure maximum topology diversity (not minor tweaks)

5. Repeat until iteration 18 or improvement

### Phase 2: Focused Refinement (iterations 19-30)

Only if Phase 1 found improvement:
1. Generate 3 variants with SMALL mutations:
   - Height: ±0.15
   - Width: ±5% of segment
   - Reorder levels

2. Probe all, evaluate top 1

3. If no improvement after 5 iterations: return to Phase 1

## Key Rules
- ALL variants must be non-negative step functions
- Use 30 probes to explore 10-15+ step-topology variants
- NEVER change the FFT-based evaluation structure
- If iteration 15+: ensure maximum topology diversity
- Focus on structural changes, not parameter tuning
