def run(ctx, args):
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no task inputs"}
    try:
        first_line = ctx.read_input_sample(names[0], nrows=1)
        N = int(first_line.strip())
        all_lines = ctx.read_input_sample(names[0], nrows=10001)
        coords = []
        for line in all_lines.strip().split("\\n")[1:]:
            if line:
                x, y = map(int, line.split())
                coords.append((x, y))
        
        mackerels = coords[:N]
        sardines = coords[N:2*N]
        
        GRID_SIZE = 100
        cell_size = 100000 // GRID_SIZE
        
        mackerel_counts = {}
        sardine_counts = {}
        
        for (x, y) in mackerels:
            cx, cy = x // cell_size, y // cell_size
            mackerel_counts[(cx, cy)] = mackerel_counts.get((cx, cy), 0) + 1
        
        for (x, y) in sardines:
            cx, cy = x // cell_size, y // cell_size
            sardine_counts[(cx, cy)] = sardine_counts.get((cx, cy), 0) + 1
        
        hotspot_cells = sorted(mackerel_counts.items(), key=lambda v: v[1], reverse=True)[:20]
        
        return {
            "total_mackerels": N,
            "total_sardines": N,
            "grid_size": GRID_SIZE,
            "hotspot_cells": [{"grid_x": c[0], "grid_y": c[1], "count": cnt} for c, cnt in hotspot_cells],
            "max_mackerel_density": hotspot_cells[0][1] if hotspot_cells else 0,
            "recommendation": "Focus polygon construction on top 20 mackerel hotspot cells"
        }
    except Exception as e:
        return {"error": str(e)}
