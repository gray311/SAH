def run(ctx, args):
    rows = args.get("grid_rows", 50)
    cols = args.get("grid_cols", 50)
    k_top = args.get("k_top", 10)
    
    program = ctx.get_program()
    fish_coords = []
    
    for line in program.split('\n'):
        line = line.strip()
        # Parse fish coordinates from C++ code
        if 'mackerel' in line.lower() or 'sardine' in line.lower():
            try:
                # Extract x,y from fish structure or input reading
                import re
                matches = re.findall(r'(\d+)\s*,\s*(\d+)', line)
                for x, y in matches:
                    fish_coords.append((int(x), int(y)))
            except:
                continue
    
    # Alternative: read from stdin simulation (program would read from input)
    # For now, assume we parse from a known format
    grid_size = max(rows, cols)
    cell_size = 100000 // grid_size
    
    # Initialize grid
    grid = [[{'m': 0, 's': 0} for _ in range(cols)] for _ in range(rows)]
    
    # Count fish per cell
    for x, y in fish_coords:
        cx, cy = min(x // cell_size, cols-1), min(y // cell_size, rows-1)
        if 0 <= cy < rows and 0 <= cx < cols:
            if 'mackerel' in line.lower():
                grid[cy][cx]['m'] += 1
            elif 'sardine' in line.lower():
                grid[cy][cx]['s'] += 1
    
    # Compute scores and find top k
    cells_with_score = []
    for r in range(rows):
        for c in range(cols):
            score = grid[r][c]['m'] - grid[r][c]['s']
            if score > 0:
                cells_with_score.append((r, c, score, grid[r][c]['m'], grid[r][c]['s']))
    
    cells_with_score.sort(key=lambda x: -x[2])
    top_cells = cells_with_score[:k_top]
    
    return {
        "cells": top_cells,
        "grid_rows": rows,
        "grid_cols": cols
    }
