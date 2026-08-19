---
name: discovery-optimization
description: "Iteratively optimize a C++ program for a rectilinear polygon covering problem.\nMaximize (mackerels_in - sardines_in + 1) by constructing a polygon that favors\nmackerel-rich regions while avoiding sardines. Use spatial analysis to guide\npolygon construction and search strategies. Budget: limited evaluations."
---

# Rectilinear Polygon Optimization

## Task
Construct a rectilinear polygon that maximizes: mackerels_inside - sardines_inside + 1

## Key Insights
- The seed program uses KD-tree + Simulated Annealing + Genetic algorithms
- It already runs a bounded internal search per test case
- Your job is to guide the search with spatial insights about fish distribution

## Method
1. **Call analyze_fish_distribution FIRST**: This reads the input coordinates
   and returns which x-y regions are mackerel-dense vs sardine-dense.

2. **Edit the polygon construction** using insights from the analysis:
   - If mackerels cluster in certain quadrants, bias your search toward those
   - If sardines are evenly distributed, focus on enclosing isolated mackerel clusters
   - Consider using disjoint sub-regions if they capture many mackerels with few sardines

3. **Modify the search strategy**:
   - Add constraints to your simulated annealing that respect the analysis
   - Use the analysis to initialize your genetic algorithm better
   - Prune search directions that lead to sardine-rich regions

4. **Evaluate sparingly**: Each evaluation is precious. Only evaluate after
   making changes that are guided by the analysis.

## Critical Details
- The analyze_fish_distribution tool is CHEAP (doesn't use your eval budget)
- Use it to understand the BEFORE state, then make targeted edits
- The seed program's search is sophisticated; augment it, don't replace it
- Keep C++ code within 1.9s per test case (safety margin = 0.1s)
