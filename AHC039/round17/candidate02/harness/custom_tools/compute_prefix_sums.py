def run(ctx, args):
    import math
    
    search_x1 = args.get("search_area_x1", 0)
    search_x2 = args.get("search_area_x2", 100000)
    search_y1 = args.get("search_area_y1", 0)
    search_y2 = args.get("search_area_y2", 100000)
    
    cell_size = 100
    grid_rows = (search_y2 - search_y1) // cell_size + 1
    grid_cols = (search_x2 - search_x1) // cell_size + 1
    
    # Parse fish from program
    program_text = ctx.get_program()
    fish = []
    for line in program_text.split('\n'):
        line = line.strip()
        if 'mackerel' in line.lower() or 'sardine' in line.lower():
            try:
                coords = [int(x.strip()) for x in line.split() if x.strip().isdigit()]
                if len(coords) >= 2:
                    fx, fy = coords[0], coords[1]
                    ftype = 1 if 'mackerel' in line.lower() else -1
                    fish.append((fx, fy, ftype))
            except:
                continue
    
    # Build grid
    grid = [[0] * grid_cols for _ in range(grid_rows)]
    for fx, fy, ftype in fish:
        cx = max(0, min(grid_cols - 1, (fx - search_x1) // cell_size))
        cy = max(0, min(grid_rows - 1, (fy - search_y1) // cell_size))
        grid[cy][cx] += ftype
    
    # Compute prefix sums
    prefix = [[0] * (grid_cols + 1) for _ in range(grid_rows + 1)]
    for i in range(grid_rows):
        row_sum = 0
        for j in range(grid_cols):
            row_sum += grid[i][j]
            prefix[i+1][j+1] = prefix[i][j+1] + row_sum
    
    # Find best rectangle using prefix sums
    best_score = float('-inf')
    best_rect = (0, 0, 0, 0)
    best_perimeter = 1000000000
    
    # Sample key points to speed up
    sample_step_x = max(1, (search_x2 - search_x1) // 200)
    sample_step_y = max(1, (search_y2 - search_y1) // 200)
    
    for x1 in range(search_x1, search_x2, sample_step_x):
        x1_cell = (x1 - search_x1) // cell_size
        x1_bound = x1_cell * cell_size + cell_size
        for y1 in range(search_y1, search_y2, sample_step_y):
            y1_cell = (y1 - search_y1) // cell_size
            y1_bound = y1_cell * cell_size + cell_size
            for x2 in range(x1_bound, min(x1_bound + cell_size * 100, search_x2), sample_step_x):
                x2_cell = (x2 - search_x1) // cell_size
                x2_bound = x2_cell * cell_size + cell_size
                for y2 in range(y1_bound, min(y1_bound + cell_size * 100, search_y2), sample_step_y):
                    y2_cell = (y2 - search_y1) // cell_size
                    score = prefix[y2_cell+1][x2_cell+1] - prefix[y1_cell][x2_cell+1] - prefix[y2_cell+1][x1_cell] + prefix[y1_cell][x1_cell]
                    if score > best_score:
                        best_score = score
                        best_rect = (x1, y1, x2, y2)
                        best_perimeter = 2 * (x2 - x1 + y2 - y1)
    
    return {
        "grid_rows": grid_rows,
        "grid_cols": grid_cols,
        "best_score": best_score,
        "best_rect": list(best_rect),
        "best_perimeter": best_perimeter
    }