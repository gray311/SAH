def run(ctx, args):
    import json
    
    seed_cell = args.get("seed_cell")
    direction = args.get("direction")
    max_length = args.get("max_length", 100)
    
    if seed_cell is None:
        return {"error": "seed_cell not provided"}
    if direction is None:
        return {"error": "direction not provided"}
    
    grid_size = 200  
    # Parse program to extract fish positions
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
    cell_size = 100000 // grid_size
    
    for x, y, ftype in fish_data:
        cx, cy = x // cell_size, y // cell_size
        if 0 <= cx < grid_size and 0 <= cy < grid_size:
            if ftype == 1:
                grid[cy][cx]['m'] += 1
            else:
                grid[cy][cx]['s'] += 1
    
    # Direction deltas
    deltas = {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "W": (0, -1)
    }
    if direction not in deltas:
        return {"error": "invalid direction"}
    dr, dc = deltas[direction]
    
    # Expand corridor
    corridor = [seed_cell]
    curr_r, curr_c = seed_cell["row"], seed_cell["col"]
    max_score = grid[curr_r][curr_c]["m"] - grid[curr_r][curr_c]["s"]
    
    for _ in range(max_length):
        new_r, new_c = curr_r + dr, curr_c + dc
        if not (0 <= new_r < grid_size and 0 <= new_c < grid_size):
            break
        
        m_count = grid[new_r][new_c]["m"]
        s_count = grid[new_r][new_c]["s"]
        score = m_count - s_count
        
        # Stop conditions
        if score < 0 and s_count > m_count + 2:
            break
        
        corridor.append({"row": new_r, "col": new_c, "m": m_count, "s": s_count, "score": score})
        curr_r, curr_c = new_r, new_c
    
    return {
        "corridor": corridor,
        "length": len(corridor),
        "final_score": corridor[-1]["score"] if corridor else 0
    }