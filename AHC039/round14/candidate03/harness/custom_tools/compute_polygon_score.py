def run(ctx, args):
    import math
    from collections import defaultdict
    import re
    
    vertices = args.get("vertices", [])
    use_full = args.get("use_full_eval", False)
    
    if not vertices or len(vertices) < 4:
        return {"score": 0.0, "mackerels": 0, "sardines": 0, "note": "invalid polygon"}
    
    # Parse program to extract fish positions
    program_text = ctx.get_program()
    fish_by_type = {"mackerel": [], "sardine": []}
    
    # Look for EVOLVE-BLOCK to extract fish data
    match = re.search(r"CPP_CODE\s*=\s*'''([\s\S]*?)'''", program_text)
    if match:
        cpp_code = match.group(1)
        # Extract fish coordinates from common patterns
        # Pattern 1: Point{ x, y } structures
        point_pattern = r'\{\s*(-?\d+)\s*,\s*(-?\d+)\s*\}'
        for line in cpp_code.split('\n'):
            if 'mackerel' in line.lower() or 'sardine' in line.lower():
                coords = re.findall(point_pattern, line)
                for x, y in coords:
                    fish_by_type["mackerel"].append((int(x), int(y)))
    
    # Build spatial grid (100x100, cell size 1000)
    grid_size = 100
    cell_size = 100000 // grid_size
    grid = defaultdict(lambda: {"mackerel": 0, "sardine": 0})
    
    for x, y in fish_by_type["mackerel"]:
        if 0 <= x < 100000 and 0 <= y < 100000:
            cx, cy = x // cell_size, y // cell_size
            grid[(cx, cy)]["mackerel"] += 1
    
    for x, y in fish_by_type["sardine"]:
        if 0 <= x < 100000 and 0 <= y < 100000:
            cx, cy = x // cell_size, y // cell_size
            grid[(cx, cy)]["sardine"] += 1
    
    # Compute polygon score using grid (O(vertices))
    # For axis-aligned polygon, approximate with bounding box decomposition
    xs = [v["x"] for v in vertices]
    ys = [v["y"] for v in vertices]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    # Handle edge cases
    if min_x >= max_x or min_y >= max_y:
        return {"score": 0.0, "mackerels": 0, "sardines": 0, "note": "degenerate polygon"}
    
    # Count cells covered by bounding box
    cx_min, cx_max = max(0, min_x // cell_size), min(100, (max_x + cell_size - 1) // cell_size)
    cy_min, cy_max = max(0, min_y // cell_size), min(100, (max_y + cell_size - 1) // cell_size)
    
    mackerels = 0
    sardines = 0
    
    for cx in range(cx_min, cx_max + 1):
        for cy in range(cy_min, cy_max + 1):
            if (cx, cy) in grid:
                mackerels += grid[(cx, cy)]["mackerel"]
                sardines += grid[(cx, cy)]["sardine"]
    
    score = max(0, mackerels - sardines + 1)
    
    return {
        "score": float(score),
        "mackerels": mackerels,
        "sardines": sardines,
        "grid_score": True,
        "use_full": use_full
    }
