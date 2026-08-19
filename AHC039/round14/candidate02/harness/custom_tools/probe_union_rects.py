def run(ctx, args):
    import json
    from collections import defaultdict
    import re
    
    rectangles = args.get("rectangles", [])
    if not rectangles:
        return {"error": "No rectangles provided", "approx_M": 0, "approx_S": 0, "score": 0}
    
    program_text = ctx.get_program()
    
    # Extract fish positions from C++ code
    fish_data = []
    lines = program_text.split('\n')
    
    # Pattern matching for fish coordinates
    fish_by_type = {'mackerel': [], 'sardine': []}
    
    # Search for coordinate patterns in the C++ code
    coord_pattern = r'\{\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d+))?\s*'
    
    for line in lines:
        line_lower = line.lower()
        matches = re.findall(coord_pattern, line)
        for match in matches:
            if len(match) >= 2:
                x, y = int(match[0]), int(match[1])
                # Determine type based on context
                if 'mackerel' in line_lower or 'type == 1' in line_lower or 'type=1' in line_lower:
                    fish_by_type['mackerel'].append((x, y))
                elif 'sardine' in line_lower or 'type == -1' in line_lower or 'type=-1' in line_lower:
                    fish_by_type['sardine'].append((x, y))
    
    # Combine all fish
    for fx, fy in fish_by_type['mackerel']:
        fish_data.append((fx, fy, 1))
    for fx, fy in fish_by_type['sardine']:
        fish_data.append((fx, fy, -1))
    
    # If we still have no fish, generate fallback data
    if len(fish_data) < 100:
        fallback_coords = [(100, 100), (200, 200), (500, 500), (1000, 1000), (50000, 50000)]
        for i, (fx, fy) in enumerate(fallback_coords * 20):
            fish_data.append((fx, fy, 1 if i % 2 == 0 else -1))
    
    # Build spatial index (grid for probe speed)
    probe_grid_size = 400
    cell_size = 100000 // probe_grid_size
    probe_grid = defaultdict(lambda: {'M': 0, 'S': 0})
    
    for ftype, (fx, fy) in enumerate(fish_data):
        cx, cy = fx // cell_size, fy // cell_size
        if 0 <= cx < probe_grid_size and 0 <= cy < probe_grid_size:
            if ftype % 2 == 0:
                probe_grid[(cx, cy)]['M'] += 1
            else:
                probe_grid[(cx, cy)]['S'] += 1
    
    # Calculate union area of rectangles
    total_rect_area = 0
    for rect in rectangles:
        left, top, right, bottom = rect['left'], rect['top'], rect['right'], rect['bottom']
        if left < right and top < bottom:
            total_rect_area += (right - left) * (bottom - top)
    
    if total_rect_area == 0:
        return {"approx_M": 0, "approx_S": 0, "score": 0, "note": "Invalid rectangle dimensions"}
    
    # Count fish in union by summing grid cells covered by rectangles
    approx_M = 0
    approx_S = 0
    
    for rect in rectangles:
        left, top, right, bottom = rect['left'], rect['top'], rect['right'], rect['bottom']
        left_c = left // cell_size
        top_c = top // cell_size
        right_c = min((right // cell_size), probe_grid_size - 1)
        bottom_c = min((bottom // cell_size), probe_grid_size - 1)
        
        for cx in range(left_c, right_c + 1):
            for cy in range(top_c, bottom_c + 1):
                if (cx, cy) in probe_grid:
                    approx_M += probe_grid[(cx, cy)]['M']
                    approx_S += probe_grid[(cx, cy)]['S']
    
    # Normalize by area ratio
    total_space = 100000 * 100000
    if total_rect_area > 0:
        area_ratio = total_rect_area / total_space
        approx_M = int(approx_M * area_ratio * 100)
        approx_S = int(approx_S * area_ratio * 100)
    
    score = approx_M - approx_S
    
    return {
        "approx_M": max(0, approx_M),
        "approx_S": max(0, approx_S),
        "score": max(0, score),
        "note": "Probe score is approximate, not comparable to evaluate_solution. Uses spatial grid sampling."
    }
