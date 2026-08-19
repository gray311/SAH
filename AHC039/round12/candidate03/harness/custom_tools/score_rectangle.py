def run(ctx, args):
    min_x = args.get("min_x", 0)
    min_y = args.get("min_y", 0)
    max_x = args.get("max_x", 100000)
    max_y = args.get("max_y", 100000)
    
    # Clamp to valid range
    min_x = max(0, min_x)
    min_y = max(0, min_y)
    max_x = min(100000, max_x)
    max_y = min(100000, max_y)
    
    if min_x > max_x or min_y > max_y:
        return {"error": "invalid rectangle", "mackerel_count": 0, "sardine_count": 0, "net_score": 0}
    
    # Parse fish data from program
    program_text = ctx.get_program()
    fish_data = []
    for line in program_text.split('\n'):
        line = line.strip()
        if line.startswith('fish[') or 'mackerel' in line.lower() or 'sardine' in line.lower():
            try:
                if '[' in line and ']' in line:
                    parts = line.replace('fish[', '').replace(']', '').split(',')
                    if len(parts) >= 2:
                        x_str, y_str = parts[0].strip(), parts[1].strip()
                        x, y = int(x_str), int(y_str)
                        # Determine type
                        if 'mackerel' in line.lower():
                            fish_type = 1
                        elif 'sardine' in line.lower():
                            fish_type = -1
                        else:
                            continue
                        fish_data.append((x, y, fish_type))
            except:
                continue
    
    # Build grid and prefix sums
    grid_size = 200
    cell_size = 100000 // grid_size
    
    grid_m = [[0] * grid_size for _ in range(grid_size)]
    grid_s = [[0] * grid_size for _ in range(grid_size)]
    
    for x, y, ftype in fish_data:
        cx = x // cell_size
        cy = y // cell_size
        if 0 <= cx < grid_size and 0 <= cy < grid_size:
            if ftype == 1:
                grid_m[cy][cx] += 1
            else:
                grid_s[cy][cx] += 1
    
    # Compute prefix sums
    pref_m = [[0] * (grid_size + 1) for _ in range(grid_size + 1)]
    pref_s = [[0] * (grid_size + 1) for _ in range(grid_size + 1)]
    
    for i in range(grid_size):
        for j in range(grid_size):
            pref_m[i + 1][j + 1] = pref_m[i][j + 1] + pref_m[i + 1][j] - pref_m[i][j] + grid_m[i][j]
            pref_s[i + 1][j + 1] = pref_s[i][j + 1] + pref_s[i + 1][j] - pref_s[i][j] + grid_s[i][j]
    
    # Clamp rectangle to grid
    grid_min_x = min_x // cell_size
    grid_min_y = min_y // cell_size
    grid_max_x = max(0, (max_x // cell_size + 1) - 1)
    grid_max_y = max(0, (max_y // cell_size + 1) - 1)
    
    grid_min_x = max(0, min(grid_min_x, grid_size - 1))
    grid_min_y = max(0, min(grid_min_y, grid_size - 1))
    grid_max_x = max(0, min(grid_max_x, grid_size - 1))
    grid_max_y = max(0, min(grid_max_y, grid_size - 1))
    
    if grid_min_x > grid_max_x or grid_min_y > grid_max_y:
        return {"mackerel_count": 0, "sardine_count": 0, "net_score": 0}
    
    # Query prefix sums
    m_count = pref_m[grid_max_y + 1][grid_max_x + 1] - pref_m[grid_min_y][grid_max_x + 1] - pref_m[grid_max_y + 1][grid_min_x] + pref_m[grid_min_y][grid_min_x]
    s_count = pref_s[grid_max_y + 1][grid_max_x + 1] - pref_s[grid_min_y][grid_max_x + 1] - pref_s[grid_max_y + 1][grid_min_x] + pref_s[grid_min_y][grid_min_x]
    
    net_score = m_count - s_count + 1
    
    return {"mackerel_count": m_count, "sardine_count": s_count, "net_score": net_score}
