def run(ctx, args):
    import json
    from collections import defaultdict
    
    seed_cell = args.get("seed_cell")
    corridors = args.get("corridors", [])
    
    if seed_cell is None or corridors is None or len(corridors) == 0:
        return {"error": "Invalid input", "note": "Need seed_cell and at least one corridor"}
    
    program_text = ctx.get_program()
    fish_data = []
    for line in program_text.split('\n'):
        line = line.strip()
        if line.startswith('fish['):
            try:
                parts = line.replace('fish[', '').replace(']', '').split(',')
                if len(parts) >= 2:
                    x, y = int(parts[0]), int(parts[1])
                    fish_type = 1 if 'mackerel' in line.lower() else -1
                    fish_data.append((x, y, fish_type))
            except:
                continue
    
    grid_size = 200
    grid = defaultdict(lambda: {'m': 0, 's': 0})
    cell_size = 100000 // grid_size
    
    for x, y, ftype in fish_data:
        cx, cy = x // cell_size, y // cell_size
        if 0 <= cx < grid_size and 0 <= cy < grid_size:
            grid[(cy, cx)]['m'] += (1 if ftype == 1 else 0)
            grid[(cy, cx)]['s'] += (1 if ftype == -1 else 0)
    
    def count_in_rect(min_r, max_r, min_c, max_c):
        total_m, total_s = 0, 0
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if (r, c) in grid:
                    total_m += grid[(r, c)]['m']
                    total_s += grid[(r, c)]['s']
        return total_m - total_s
    
    def corridor_to_rect(corridor):
        if not corridor:
            return None
        rows = [cell['row'] for cell in corridor]
        cols = [cell['col'] for cell in corridor]
        min_r, max_r = min(rows), max(rows)
        min_c, max_c = min(cols), max(cols)
        return (min_r, max_r, min_c, max_c)
    
    # Generate test configurations
    num_corridors = len(corridors)
    if num_corridors > 5:
        num_corridors = 5
    
    # Generate 12 different combination configurations
    configs = []
    
    # Config 1: All corridors from seed
    r, c = seed_cell['row'], seed_cell['col']
    configs.append({'rect': (r, r, c, c), 'corridors': list(corridors)})
    
    # Config 2: Each corridor individually
    for i, corr in enumerate(corridors[:min(num_corridors, 4)]):
        rect = corridor_to_rect(corr)
        if rect:
            configs.append({'rect': rect, 'corridors': [corr]})
    
    # Config 3: Pairs of corridors
    for i in range(min(num_corridors, 3)):
        for j in range(i+1, min(num_corridors, 4)):
            if corridors[i] and corridors[j]:
                corr1_rect = corridor_to_rect(corridors[i])
                corr2_rect = corridor_to_rect(corridors[j])
                if corr1_rect and corr2_rect:
                    union_r = min(corr1_rect[0], corr2_rect[0])
                    union_c = min(corr1_rect[2], corr2_rect[2])
                    union_R = max(corr1_rect[1], corr2_rect[1])
                    union_C = max(corr1_rect[3], corr2_rect[3])
                    configs.append({'rect': (union_r, union_R, union_c, union_C), 'corridors': [corridors[i], corridors[j]]})
    
    # Score each configuration
    results = []
    for config in configs[:15]:  # Limit to 15 configs
        rect = config['rect']
        score = count_in_rect(rect[0], rect[1], rect[2], rect[3])
        results.append({
            'config_id': len(results),
            'rect': rect,
            'score': score
        })
    
    return {'probe_results': results, 'num_configurations_tested': len(results)}