---
name: discovery-optimization
description: "Iteratively optimize a C++ program's EVOLVE-BLOCK to maximize geometric polygon scoring on a rectilinear polygon construction task. Uses density_probe to quickly rank candidate shapes by mackerel-sardine density before full evaluation."
---

# Geometric Polygon Optimization Strategy

## Understanding the Task
- Goal: Maximize (mackerels - sardines + 1) inside a rectilinear polygon
- Polygon edges must be axis-parallel (horizontal/vertical only)
- Max 1000 vertices, max perimeter 400,000

## Core Strategy: Density-Guided Search

### Step 1: Initial Exploration
Generate a base polygon (rectangle or simple shape) that covers a reasonable area.
Use density_probe to estimate net density in different regions of the solution.

### Step 2: Region Analysis with density_probe
Call density_probe with your current or candidate polygon to get:
- Mackerel count in the polygon (subsampled)
- Sardine count in the polygon (subsampled)
- Net density estimate

This is CHEAP and does not consume evaluation budget.

### Step 3: Targeted Modifications
Based on density_probe results:
- If a region has high mackerel density: expand the polygon into it
- If a region has high sardine density: contract or indent away from it
- Try adding indentations to exclude sardine clusters

### Step 4: Probe-Rank Before Full Eval
When you have multiple candidate edits:
1. Use density_probe on each variant to rank by net density
2. Select the top 1-2 candidates
3. Use evaluate_solution ONLY on the best one

This saves precious evaluation budget.

### Step 5: Iteration and Diversification
- If scores plateau, try a completely different polygon structure
- Try shifting the entire polygon to a different location
- Try increasing/decreasing the polygon's spread systematically

## Tool Usage Pattern
1. edit_solution: Propose a geometric change (expand to mackerel cluster, exclude sardine)
2. density_probe: Check if the change improved net density (cheap!)
3. edit_solution: Make another targeted change based on feedback
4. (repeat steps 1-3 several times)
5. evaluate_solution: Confirm the best candidate
6. If score improved, keep it and continue. If not, try a different direction.

## Emergency Strategies
- If stuck at low scores: try covering all points with a massive rectangle, then refine
- If hitting time limits: simplify your internal search, use greedy approximations
- If validity issues: check perimeter constraints, vertex count, self-intersection

## Key Rules
- Never fabricate scores — only use evaluate_solution results
- Best version is automatically kept, so you never lose progress
- Make one substantive change per iteration
- Use all 20 evaluations wisely — reserve for promising candidates
- Call finish when no improvement is possible
