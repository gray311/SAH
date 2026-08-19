def run(ctx, args):
    center_x = args.get("center_x", 0)
    center_y = args.get("center_y", 0)
    radius = args.get("radius", 200)
    
    # Parse fish positions from program
    fish = {"mackerel": [], "sardine": []}
    program = ctx.get_program()
    
    for line in program.split('\n'):
        line = line.strip()
        if 'fish' in line and '[' in line:
            try:
                # Extract coordinate
                if 'mackerel' in line.lower():
                    parts = line.split(',')
                    if len(parts) >= 2:
                        fish["mackerel"].append((int(parts[0]), int(parts[1])))
                elif 'sardine' in line.lower():
                    parts = line.split(',')
                    if len(parts) >= 2:
                        fish["sardine"].append((int(parts[0]), int(parts[1])))
            except:
                continue
    
    # Count fish in radius
    def in_radius(pt, cx, cy, r):
        return (pt[0] - cx)**2 + (pt[1] - cy)**2 <= r**2
    
    m_count = sum(1 for p in fish["mackerel"] if in_radius(p, center_x, center_y, radius))
    s_count = sum(1 for p in fish["sardine"] if in_radius(p, center_x, center_y, radius))
    
    return {
        "mackerel_count": m_count,
        "sardine_count": s_count,
        "density": m_count - s_count,
        "total_count": m_count + s_count
    }
