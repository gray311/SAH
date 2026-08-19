---
name: rectangle-construction-playbook
description: Concrete checklist for constructing rectangle-based polygons for the mackerel-sardine problem. Focus on analyzing fish distribution, generating multiple rectangle candidates, probing them cheaply, and selecting the best one.
---

# Rectangle Construction Playbook for Mackerel-Sardine Problem

## Step 1: Analyze Fish Distribution (use analyze_fish_grid)
- Get the bounding box of mackerels: (min_x, min_y) to (max_x, max_y)
- Count mackerels vs sardines in sample
- Note any obvious sardine clusters near mackerel edges

## Step 2: Generate 3-5 Rectangle Candidates

**Candidate 1: Full Mackerel Box**
- x1, y1 = min_x, min_y of all mackerels
- x2, y2 = max_x, max_y of all mackerels
- Perimeter = 2*(x2-x1 + y2-y1)
- Pros: Captures all mackerels; Cons: May catch many sardines

**Candidate 2: Shrink by Margins**
- Add 10% margin to each side from step 1
- This reduces sardine overlap while losing few mackerels
- Check perimeter still ≤ 400,000

**Candidate 3: Grid Subdivisions**
- Split mackerel box into 3×3 grid (if size allows)
- Test each cell's score via probe
- Combine top 2-3 cells if perimeter permits

**Candidate 4: Multiple Separated Rectangles**
- If mackerels are in 2+ clusters, create separate rectangles
- This avoids sardine-rich regions between clusters
- More complex but potentially higher score

## Step 3: Probe Candidates
- For each candidate, edit solution with those coordinates
- Call probe_solution to quickly score (~10s, ~30 budget)
- Do NOT call evaluate_solution yet

## Step 4: Select and Evaluate
- Pick top 2 candidates by probe score
- Call evaluate_solution on first (use most budget)
- If time/budget allows, try second
- Always use full evaluation budget efficiently

## Step 5: Final Polish
- Ensure C++ code compiles: \\n for newlines, correct includes
- Verify perimeter constraint: ≤ 400,000
- Verify coordinates: 0-100,000, integers
- Run one more evaluate_solution if prompted

## Key Success Factors
- Systematic exploration (not random edits)
- Use probe_solution to avoid wasting full evaluations
- Bounded internal search (stay within 2s time limit)
- Validate constraints before final submission
