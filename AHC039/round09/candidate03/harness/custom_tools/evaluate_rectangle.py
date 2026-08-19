def run(ctx, args):
    x_min = args.get("x_min", 0)
    x_max = args.get("x_max", 100000)
    y_min = args.get("y_min", 0)
    y_max = args.get("y_max", 100000)
    
    # Parse program to extract fish positions
    program_text = ctx.get_program()
    mackerels = []
    sardines = []
    for line in program_text.split("\n"):
        line = line.strip()
        if line.startswith("fish[") or "mackerel" in line.lower() or "sardine" in line.lower():
            try:
                # Extract coordinates from fish definition
                if "x" in line and "y" in line:
                    parts = line.replace("(", "").replace(")", "").replace("\n", "").replace(" ", "").split(",")
                    if len(parts) >= 2:
                        x, y = int(parts[0]), int(parts[1])
                        if "mackerel" in line.lower():
                            mackerels.append((x, y))
                        else:
                            sardines.append((x, y))
            except:
                continue
    
    # Count fish inside rectangle (inclusive boundaries)
    m_count = 0
    s_count = 0
    for (x, y) in mackerels:
        if x_min <= x <= x_max and y_min <= y <= y_max:
            m_count += 1
    for (x, y) in sardines:
        if x_min <= x <= x_max and y_min <= y <= y_max:
            s_count += 1
    
    score = max(0, m_count - s_count + 1)
    
    # Validate rectangle
    valid = True
    errors = []
    if x_min < 0 or x_max > 100000:
        valid = False
        errors.append("coords out of bounds")
    if x_min > x_max or y_min > y_max:
        valid = False
        errors.append("invalid rectangle bounds")
    perimeter = 2 * ((x_max - x_min) + (y_max - y_min))
    if perimeter > 400000:
        valid = False
        errors.append("perimeter exceeds limit")
    
    return {
        "x_min": x_min, "x_max": x_max, "y_min": y_min, "y_max": y_max,
        "m_count": m_count, "s_count": s_count, "score": score,
        "valid": valid, "errors": errors if not valid else []
    }