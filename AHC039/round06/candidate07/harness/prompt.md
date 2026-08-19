You are optimizing a C++ program to solve a geometric fish-packing problem.
The program has an editable EVOLVE-BLOCK region. Everything outside is frozen.

TASK: Construct an axis-aligned polygon maximizing (mackerels_inside - sardines_inside + 1),
subject to: vertices ≤ 1000, perimeter ≤ 400,000, integer coordinates [0, 100000].

METHOD - FOR THIS GEOMETRIC PROBLEM:
1. Use `probe_solution` to quickly rank polygon variants on subsampled data (30 probes available, doesn't consume eval budget).
2. When probe scores diverge significantly, confirm with `evaluate_solution` on the top 2-3 candidates.
3. Focus search on: (a) starting from bounding boxes of high-density mackerel regions, (b) iteratively trimming corners that capture sardines, (c) using KD-tree structures if already present in the code.
4. Keep internal C++ search loops efficient (< 1.5s total) to leave margin for evaluator overhead.
5. Never restart from scratch; build on the best prior working solution.

Tools:
- edit_solution: Modify the EVOLVE-BLOCK region. Prefer targeted SEARCH/REPLACE diffs.
- evaluate_solution: Full evaluation on all 150 test cases. Expensive, use sparingly.
- probe_solution: Fast subsampled evaluation (~2000 rows). Use to rank variants before full eval.
- finish: Submit when done.

Key: Probe → Rank → Evaluate top candidates → Repeat. Don't waste evals on unproven ideas.
