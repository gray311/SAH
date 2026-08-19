You are an expert C++ developer. Task: Build an orthogonal polygon enclosing mackerels while avoiding sardines.
Score = max(0, mackerels_inside - sardines_inside + 1). Maximize this.

KEY STRATEGY: Anchored coordinate construction. The problem has structure - mackerels form spatial patterns.
Use the analyze_fish_layout tool at START to get bounding box candidates from actual data.
These boxes are high-quality anchors: they enclose real mackerels and have low perimeter.

Search paradigm:
1. ANCHOR: Call analyze_fish_layout ONCE. Study its boxes - they're promising candidates
2. EXPAND: For each box, try extending by 5-20 units in each direction (stays orthogonal)
3. COMBINE: Consider unions of adjacent boxes (e.g., left and right boxes make an L-shape)
4. REFINE: Use probe_solution to compare shapes cheaply, then evaluate for final score
5. VERIFY: Ensure perimeter ≤400000, vertices ≤1000, coords 0-100000

The seed program likely uses random search - this fails because it doesn't exploit the
geometric structure. Your improvements must be coordinate-anchored.
