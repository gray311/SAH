def run(ctx, args):
    import json
    min_m = args.get("min_mackerels", 2)
    max_s = args.get("max_sardines", 1)
    max_perim = args.get("max_perimeter", 400000)
    
    # Parse program to get fish coordinates
    prog = ctx.get_program()
    fish_m = []
    fish_s = []
    
    for line in prog.split('\\n'):
        line = line.strip()
        if line.startswith('fish['):
            try:
                content = line.replace('fish[', '').replace(']', '')
                parts = content.split(',')
                if len(parts) >= 2:
                    x, y = int(parts[0]), int(parts[1])
                    if 'mackerel' in line.lower():
                        fish_m.append((x, y))
                    else:
                        fish_s.append((x, y))
            except:
                continue
    
    # Build grid with cell_size=100
    cell_size = 100
    grid = {}
    for x, y in fish_m:
        cx, cy = x // cell_size, y // cell_size
        key = (cx, cy)
        grid[key] = grid.get(key, {'m': 0, 's': 0})
        grid[key]['m'] += 1
    for x, y in fish_s:
        cx, cy = x // cell_size, y // cell_size
        key = (cx, cy)
        grid[key] = grid.get(key, {'m': 0, 's': 0})
        grid[key]['s'] += 1
    
    # Find candidate rectangles
    candidates = []
    
    for (cx, cy), counts in grid.items():
        if counts['m'] < min_m or counts['s'] > max_s:
            continue
        
        for width in [1, 2, 3, 4, 5]:
            for height in [1, 2, 3, 4, 5]:
                rect_x = cx * cell_size
                rect_y = cy * cell_size
                rect_w = width * cell_size
                rect_h = height * cell_size
                
                perim = 2 * (rect_w + rect_h)
                if perim > max_perim:
                    continue
                
                est_m = width * height * (counts['m'] / max(1, counts['s'] + 1))
                est_s = width * height * counts['s']
                
                candidates.append({
                    'rect_x': rect_x,
                    'rect_y': rect_y,
                    'rect_w': rect_w,
                    'rect_h': rect_h,
                    'est_score': est_m - est_s,
                    'area': width * height
                })
    
    candidates.sort(key=lambda x: x['est_score'], reverse=True)
    return {'candidates': candidates[:20]}
