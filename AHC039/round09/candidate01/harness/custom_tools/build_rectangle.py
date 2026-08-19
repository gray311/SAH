def run(ctx, args):
    import json
    
    seed_cell = args.get("seed_cell")
    max_perimeter = args.get("max_perimeter", 400000)
    expansion_factor = args.get("expansion_factor", 200)
    
    if seed_cell is None:
        return {"error": "seed_cell not provided"}
    
    # Parse program to extract fish positions
    program_text = ctx.get_program()
    fish_data = []
    for line in program_text.split('\n'):
        line = line.strip()
        if 'mackerel' in line.lower() or 'sardine' in line.lower():
            try:
                if '[' in line and ']' in line:
                    parts = line.split('[')
                    if len(parts) > 1:
                        coords = parts[1].split(']')[0]
                        if ',' in coords:
                            x_str, y_str = coords.split(',')
                            x, y = int(x_str.strip()), int(y_str.strip())
                            fish_type = 1 if 'mackerel' in line.lower() else -1
                            fish_data.append((x, y, fish_type))
            except:
                continue
    
    # Build 50x50 grid (cell_size=2000)
    grid_size = 50
    cell_size = 100000 // grid_size
    grid = [[{"m": 0, "s": 0} for _ in range(grid_size)] for _ in range(grid_size)]
    
    for x, y, ftype in fish_data:
        cx, cy = x // cell_size, y // cell_size
        if 0 <= cx < grid_size and 0 <= cy < grid_size:
            if ftype == 1:
                grid[cy][cx]["m"] += 1
            else:
                grid[cy][cx]["s"] += 1
    
    # Start from seed cell and expand
    sr, sc = seed_cell["row"], seed_cell["col"]
    
    # Expand in 4 directions
    directions = [
        ("N", -1, 0),
        ("S", 1, 0),
        ("E", 0, 1),
        ("W", 0, -1)
    ]
    
    # Try each direction to find optimal expansion
    best_rect = None
    best_score = -float("inf")
    
    for dir_name, dr, dc in directions:
        # Expand in this direction
        row_start, col_start = sr, sc
        row_end, col_end = sr, sc
        
        curr_r, curr_c = sr, sc
        curr_score = grid[sr][sc]["m"] - grid[sr][sc]["s"]
        
        # Expand up to expansion_factor cells in this direction
        for _ in range(expansion_factor):
            new_r, new_c = curr_r + dr, curr_c + dc
            if not (0 <= new_r < grid_size and 0 <= new_c < grid_size):
                break
            
            m_count = grid[new_r][new_c]["m"]
            s_count = grid[new_r][new_c]["s"]
            cell_score = m_count - s_count
            
            # Stop if too many sardines
            if s_count > m_count * 3:
                break
            
            if cell_score > 0:
                curr_r, curr_c = new_r, new_c
            else:
                break
        
        # Compute rectangle from (row_start, col_start) to (curr_r, curr_c)
        r_min, r_max = min(row_start, curr_r), max(row_start, curr_r)
        c_min, c_max = min(col_start, curr_c), max(col_start, curr_c)
        
        # Check perimeter constraint
        perimeter = 2 * ((r_max - r_min + 1) * cell_size + (c_max - c_min + 1) * cell_size)
        if perimeter > max_perimeter * 0.8:  # Leave room for refinement
            continue
        
        # Compute rectangle score
        rect_score = 0
        for r in range(r_min, r_max + 1):
            for c in range(c_min, c_max + 1):
                rect_score += grid[r][c]["m"] - grid[r][c]["s"]
        
        if rect_score > best_score:
            best_score = rect_score
            best_rect = {
                "r_min": r_min,
                "r_max": r_max,
                "c_min": c_min,
                "c_max": c_max,
                "score": rect_score,
                "perimeter": perimeter
            }
    
    if best_rect is None:
        # Fallback to single cell
        best_rect = {
            "r_min": sr,
            "r_max": sr,
            "c_min": sc,
            "c_max": sc,
            "score": grid[sr][sc]["m"] - grid[sr][sc]["s"],
            "perimeter": 4 * cell_size
        }
    
    # Convert to vertices
    cell_size = 100000 // 50
    vertices = [
        (best_rect["c_min"] * cell_size, best_rect["r_min"] * cell_size),
        (best_rect["c_max"] * cell_size, best_rect["r_min"] * cell_size),
        (best_rect["c_max"] * cell_size, best_rect["r_max"] * cell_size),
        (best_rect["c_min"] * cell_size, best_rect["r_max"] * cell_size)
    ]
    
    return {
        "vertices": vertices,
        "score": best_rect["score"],
        "perimeter": best_rect["perimeter"],
        "grid_cells": {
            "r_min": best_rect["r_min"],
            "r_max": best_rect["r_max"],
            "c_min": best_rect["c_min"],
            "c_max": best_rect["c_max"]
        }
    }
