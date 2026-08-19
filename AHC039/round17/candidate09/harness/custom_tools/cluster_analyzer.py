def run(ctx, args):
    import json
    grid_size = args.get("grid_size", 100)
    cell_size = 100000 // grid_size
    
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
    
    # Build grid
    grid = [[{'m': 0, 's': 0} for _ in range(grid_size)] for _ in range(grid_size)]
    for x, y, ftype in fish_data:
        cx, cy = x // cell_size, y // cell_size
        if 0 <= cx < grid_size and 0 <= cy < grid_size:
            if ftype == 1:
                grid[cy][cx]['m'] += 1
            else:
                grid[cy][cx]['s'] += 1
    
    # Compute scores and find top 10
    scores = []
    for cy in range(grid_size):
        for cx in range(grid_size):
            score = grid[cy][cx]['m'] - grid[cy][cx]['s']
            if score > 0:
                scores.append((score, cy, cx, grid[cy][cx]['m'], grid[cy][cx]['s']))
    
    scores.sort(reverse=True, key=lambda x: x[0])
    top_10 = scores[:10]
    
    result = []
    for score, cy, cx, m_count, s_count in top_10:
        result.append({
            "row": cy,
            "col": cx,
            "score": score,
            "mackerels": m_count,
            "sardines": s_count,
            "center_x": cx * cell_size + cell_size // 2,
            "center_y": cy * cell_size + cell_size // 2
        })
    
    return {"top_cells": result, "count": len(result)}
