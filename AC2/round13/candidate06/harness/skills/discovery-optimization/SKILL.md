---
name: discovery-optimization
description: "Systematic step-function refinement for C2 maximization. Focus on depth-first search within\nthe step-function class: small height perturbations, width adjustments, and asymmetric variations.\nUse probe_solution to filter variants before full evaluation. Only explore new seed patterns after\nexhausting refinement of current pattern. Step functions are the proven path to beating 0.8962799441554086."
---

# Step-Function Refinement Protocol for C2 Maximization

## Core Principle

Step functions are the PROVEN path to beating the record (0.8962799441554086). The record is CLOSE.
Focus on DEEP REFINEMENT: small, systematic perturbations within step-function architectures.
AVOID smooth/diverse function families until step-function refinement is exhausted.

## Phase 1: Pattern Selection

Start with ONE seed pattern from the 13 available step patterns. Prefer patterns with:
- Multiple levels (2+ distinct heights)
- Asymmetric structures
- Peak positions around 0.25-0.75 of domain

## Phase 2: Systematic Mutation Pipeline

For your CURRENT pattern, generate mutations in this ORDER:

### Step 2.1: Height Perturbation (±0.02-0.08)
- Increase/decrease the highest peak by 0.03-0.08
- Slightly adjust secondary peaks (±0.02-0.05)
- Try asymmetric variations: make adjacent levels unequal (e.g., 1.40, 1.46, 1.34)

### Step 2.2: Width Adjustment (±2-5% of interval)
- Expand the highest-peak interval by 3-5%
- Contract the "wing" intervals by 2-4%
- Shift left/right boundaries by constant offset (1-2% of domain)

### Step 2.3: Level Addition/Removal (for multi-level patterns)
- Add a new level: insert an intermediate height between existing levels
- Remove one level: merge two adjacent levels into one
- Adjust level ordering: experiment with different height permutations

### Step 2.4: Symmetry Breaking
- Start with symmetric pattern, then perturb to make asymmetric
- Example: symmetric pyramid 0.7, 1.5, 2.1, 1.5, 0.7 → 0.7, 1.52, 2.11, 1.48, 0.71

## Phase 3: Probe-Based Filtering

1. Generate 5-8 variants with small mutations
2. Call probe_solution for ALL variants (use your 30-probe budget!)
3. Rank by probe score, EVALUATE only the top 2-3
4. If probe scores all below current best: regenerate variants with different mutations

## Phase 4: Pattern Switching (after 8 iterations on current pattern)
- If no improvement after 8 iterations, switch to a DIFFERENT seed pattern
- Try patterns with different characteristics: more levels, different peak positions
- Don't try >3 different patterns before deepening refinement of any one

## Phase 5: Late-Stage Exploration (after 20 iterations)
- Only after exhausting step-function refinement, try new architectures
- Multi-peaked functions, asymmetric structures, hybrid step+smooth

## Phase 6: Documentation

Track for each pattern:
- Initial score, best score achieved
- Most successful mutation types (height vs width vs asymmetric)
- Iteration count to best improvement

## Key Rules

1. DEPTH > BREADTH: Refine ONE pattern to 20+ iterations before switching
2. USE PROBES: Always probe 5+ variants before spending 1-2 evals
3. SMALL STEPS: Keep mutations small (±2-8% for heights, ±2-5% for widths)
4. SYSTEMATIC: Follow the mutation pipeline order (height → width → levels → symmetry)
5. PATIENT: The record is close; incremental improvements compound
