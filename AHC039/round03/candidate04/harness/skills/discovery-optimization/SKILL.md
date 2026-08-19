---
name: discovery-optimization
description: "Optimize a C++ geometric algorithm through structured internal search and probe-based ranking. Use for tasks requiring constructive search over combinatorial solution spaces."
---

Geometric Polygon Optimization Harness
Core Strategy: You are optimizing a C++ program that constructs an axis-aligned polygon to maximize: (mackerels inside) - (sardines inside) + 1.
The key insight is that the seed program likely outputs a single fixed polygon. You must transform it into a search-based algorithm that adapts to each test case's fish distribution.
Step 1: Analyze the Seed After the first evaluation, ask yourself: - What polygon shape does it use? - How many vertices? What is the perimeter? - Is it deterministic or does it search internally? - Where does it likely under-cover mackerels or over-cover sardines?
Step 2: Design a Search Algorithm
Approach A: Greedy Expansion 1. Start with a minimal polygon (e.g., bounding box of one mackerel) 2. Iteratively expand in the 4 cardinal directions 3. For each expansion, estimate: Will this add more mackerels than sardines? 4. Keep expanding if beneficial, stop when perimeter budget reached
Approach B: Density-Based Clustering 1. Group mackerels into clusters (spatial proximity) 2. Group sardines into clusters 3. For each mackerel cluster, find a local polygon that covers the cluster center and excludes nearby sardines if possible 4. Combine local polygons into one simple polygon
Approach C: Rectangular Partitioning 1. Divide the plane into a grid (e.g., 100x100 cells) 2. For each cell, decide: include it in polygon or exclude it? 3. Decision rule: include if (mackerels in cell) - (sardines in cell) > threshold 4. Extract the union of included cells as a polygon
Step 3: Use probe_solution Extensively
CRITICAL: probe_solution is FREE and fast. Use it to rank 5-10 variants before spending a single evaluation budget call.
Example workflow: 1. Design 5 different polygon construction strategies 2. For each strategy, run probe_solution (5 cheap calls) 3. Pick the top 2 with highest probe scores 4. Run evaluate_solution on those 2 (2 budget calls) 5. The winner gets refined further
Step 4: Iterate and Refine If a variant improves the score: Understand WHY (what changed?) and apply the same principle to other variants. If a variant fails: Check validity, if invalid fix the constraint, if valid but worse try a different approach.
Step 5: Handle Time Limits The code must run all 150 test cases in 2.0s total. This means ~13ms per test case. Don't use heavy internal search - O(n^2) operations where n=5000 is too slow. Use O(n log n) algorithms like KD-tree.
Code Modification Guidelines: Look for patterns of fixed polygons and replace with search-based construction. Use KD-tree for fast spatial queries to find fish in bounding boxes. Add perimeter calculations and validation.
Common Failure Modes: 1. Outputting Fixed Polygons: Symptom is seed score or 0. Fix: make the code iterate and construct from input data. 2. Time Limit Exceeded: No output or crash. Fix: reduce internal search complexity to O(n log n). 3. Invalid Polygon: Symptom validity=0. Fix: add validation checks or simplify construction. 4. Malformed C++ Code: Symptom compilation errors. Fix: use proper escaping, keep triple-quoted strings intact.
Evaluation Strategy: 1. Start: evaluate_solution on seed (1 call) 2. Explore: edit, then probe_solution x3 (rank 4 variants, 0 budget) 3. Evaluate: evaluate_solution on best probe (1 call) 4. Refine: If improved, edit, probe x2, evaluate (2 calls) 5. Repeat until score plateaus or 20 calls used 6. Finish: submit best version
Success Signals: - Score > seed (2.47329) - Probability of validity = 1.0 - Runtime < 2.0s on all 150 test cases - Using probe_solution to guide decisions - Evidence of structured search, not random changes
