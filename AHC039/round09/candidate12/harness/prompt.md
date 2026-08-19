You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

CRITICAL STRATEGY: Enumerate candidate axis-aligned rectangles using KD-tree scoring.

SEARCH METHOD (encodes in EVOLVE-BLOCK C++ code):

1. KD-TREE SETUP: Build a KD-tree from all fish positions at startup (O(N log N)).

2. RECTANGLE ENUMERATION: Generate candidate rectangles by varying:
   - X range: 0 to 100000, try multiple widths (500, 1000, 2000, 5000, 10000)
   - Y range: 0 to 100000, try multiple heights (500, 1000, 2000, 5000, 10000)
   - Center points: sample from mackerel-dense regions (top 10 mackerel positions)

3. KD-TREE SCORING: For each candidate rectangle, use KD-tree to count mackerels and sardines in O(log N) time.
   - Score = mackerels - sardines
   - Track best rectangle

4. POLYGON CONSTRUCTION: Convert best rectangle to polygon vertices (4 vertices minimum).
   - Ensure perimeter <= 400,000 and coords in [0,100000]
   - Use KD-tree to verify no self-intersection (trivial for axis-aligned rectangles)

5. MULTIPLE RESTARTS: Run 20-25 restarts with different random seeds for center point selection.
   - Each restart: pick 3-5 random mackerel positions, enumerate rectangles around them
   - Track best score across all restarts

6. OUTPUT: Best rectangle as polygon (4 vertices in order).

Tools:
- edit_solution: Replace EVOLVE-BLOCK with C++ implementing rectangle enumeration with KD-tree scoring
- evaluate_solution: Run C++ program, get score
- probe_solution: NOT useful - need full evaluation for accurate scoring
- finish: Submit when you have encoded working rectangle enumeration with KD-tree scoring

Preserve EVOLVE-BLOCK markers, exact I/O format (m then vertices), and ensure <2.0s execution.

KEY DIFFERENCE from seed: Simplified rectangle enumeration focused on axis-aligned bounding boxes around mackerel clusters, using KD-tree for efficient O(log N) scoring instead of complex corridor expansion.
