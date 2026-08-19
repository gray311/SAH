def run(ctx, args):
    import json
    
    # Parse fish positions from program
    program_text = ctx.get_program()
    fish_data = []
    for line in program_text.split('\n'):
        line = line.strip()
        if line.startswith('fish['):
            try:
                # Extract mackerel or sardine coordinates
                parts = line.replace('fish[', '').replace(']', '').split(',')
                if len(parts) >= 2:
                    x, y = int(parts[0].strip()), int(parts[1].strip())
                    # Default: first N are mackerels, next N are sardines
                    fish_idx = int(parts[0])
                    if fish_idx < 5000:
                        fish_type = 1
                    else:
                        fish_type = -1
                    fish_data.append((x, y, fish_type))
            except:
                continue
    
    grid_size = 100
    cell_size = 100000 // grid_size
    
    # Initialize grid
    M = [[0] * grid_size for _ in range(grid_size)]
    S = [[0] * grid_size for _ in range(grid_size)]
    
    # Count fish per cell
    for x, y, ftype in fish_data:
        if ftype > 0:
            cx, cy = min(x // cell_size, grid_size - 1), min(y // cell_size, grid_size - 1)
            M[cy][cx] += 1
        else:
            cx, cy = min(x // cell_size, grid_size - 1), min(y // cell_size, grid_size - 1)
            S[cy][cx] += 1
    
    # Build prefix sums
    P_M = [[0] * (grid_size + 1) for _ in range(grid_size + 1)]
    P_S = [[0] * (grid_size + 1) for _ in range(grid_size + 1)]
    
    for r in range(grid_size):
        for c in range(grid_size):
            P_M[r + 1][c + 1] = P_M[r][c + 1] + P_M[r + 1][c] - P_M[r][c] + M[r][c]
            P_S[r + 1][c + 1] = P_S[r][c + 1] + P_S[r + 1][c] - P_S[r][c] + S[r][c]
    
    total_M = P_M[grid_size][grid_size]
    total_S = P_S[grid_size][grid_size]
    
    return {
        "total_mackerels": total_M,
        "total_sardines": total_S,
        "grid_size": grid_size,
        "cell_size": cell_size,
        "prefix_sums_P_M": P_M,
        "prefix_sums_P_S": P_S
    }
