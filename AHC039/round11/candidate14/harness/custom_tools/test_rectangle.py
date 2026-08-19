def run(ctx, args):
    min_x = args.get("min_x", 0)
    max_x = args.get("max_x", 100000)
    min_y = args.get("min_y", 0)
    max_y = args.get("max_y", 100000)
    
    program = ctx.get_program()
    mackerels = []
    sardines = []
    
    for line in program.split('\n'):
        line = line.strip()
        if 'mackerel' in line.lower() or 'x_' in line:
            try:
                parts = line.split()
                if len(parts) >= 2:
                    x, y = int(parts[0]), int(parts[1])
                    mackerels.append((x, y))
            except:
                pass
        elif 'sardine' in line.lower() or 'x_{N' in line:
            try:
                parts = line.split()
                if len(parts) >= 2:
                    x, y = int(parts[0]), int(parts[1])
                    sardines.append((x, y))
            except:
                pass
    
    m_count = sum(1 for (x,y) in mackerels if min_x <= x <= max_x and min_y <= y <= max_y)
    s_count = sum(1 for (x,y) in sardines if min_x <= x <= max_x and min_y <= y <= max_y)
    
    score = max(0, m_count - s_count + 1)
    
    return {
        "min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y,
        "mackerels": m_count, "sardines": s_count, "score": score
    }
