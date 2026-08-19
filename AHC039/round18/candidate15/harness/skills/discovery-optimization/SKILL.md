---
name: discovery-optimization
description: "Mackerel cluster rectangle packing. Parse input, find dense clusters, build bounding rectangles, use KD-tree for scoring, try local perturbations, use probe to rank variants before full eval."
---

# Mackerel Cluster Rectangle Packing

## Step 1: Input Parsing
- Read N=5000 mackerels from lines 1-5000
- Read N=5000 sardines from lines 5001-10000
- Store in vectors for KD-tree construction

## Step 2: KD-Tree Construction
- Build KD-tree on ALL points (mackerels and sardines)
- Use 2-level tree: first split by X, then by Y
- Query function returns count of points in rectangle

## Step 3: Rectangle Generation
Generate candidate rectangles:

a) Unit square: [0,100000]x[0,100000] (baseline)

b) Around each mackerel: create 3x3 grid of 1000x1000 rectangles centered on fish

c) Cluster-based: group nearby mackerels (distance < 5000), find bounding box

d) Random seeds: generate 5 random rectangles with random corners

## Step 4: Score Each Candidate
For each rectangle, compute:
- m_count = kd_tree_query(rect.x0, rect.x1, rect.y0, rect.y1)
- s_count = kd_tree_query(rect.x0, rect.x1, rect.y0, rect.y1) 
  (use separate queries or query all points and filter)
- score = max(0, m_count - s_count + 1)

## Step 5: Local Perturbations
For top 3 candidates by score:
- For each edge, try shifts of ±5, ±10 in x or y direction
- Keep shifts that improve score

## Step 6: Probe-Based Ranking
- Generate 10 variants with different random seeds
- For each, do ONE probe (not full eval) to rank
- Take top 3 and do full evaluation

## Step 7: Output Best
- Output vertices of best polygon
- Ensure valid format: m followed by m lines of "x y"
- Perimeter must be ≤ 400000
