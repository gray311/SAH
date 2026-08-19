def run(ctx, args):
    import math
    
    seed_x = args.get("seed_x", 0)
    seed_y = args.get("seed_y", 0)
    expansion_range = args.get("expansion_range", 2000)
    
    # Parse program to get fish coordinates
    program_text = ctx.get_program()
    mackerels = []
    sardines = []
    
    lines = program_text.split('\n')
    fish_count = 0
    for line in lines:
        line = line.strip()
        # Look for fish coordinate patterns in CPP_CODE
        import re
        matches = re.findall(r'fish\[[^\]]+\]', line)
        if not matches:
            # Try to parse structured data
            try:
                idx = line.index('fish[')
                data_str = line[idx+5:].split(']')[0].strip()
                parts = data_str.split(',')
                if len(parts) >= 2:
                    x_str, y_str = parts[0], parts[1]
                    # Extract numbers
                    x_parts = re.findall(r'-?\d+', x_str)
                    y_parts = re.findall(r'-?\d+', y_str)
                    if x_parts and y_parts:
                        x = int(x_parts[0])
                        y = int(y_parts[0])
                        # Determine type from context (mackerel first, then sardine)
                        # This is approximate; actual type needs tracking
                        fish_count += 1
                        if fish_count <= 5000:
                            mackerels.append((x, y))
                        else:
                            sardines.append((x, y))
            except:
                continue
    
    # If we couldn't parse, use approximation around seed
    if not mackerels or not sardines:
        # Fallback: generate candidate corners around seed
        candidates = []
        for dx in [0, expansion_range, expansion_range//2, expansion_range//4]:
            for dy in [0, expansion_range, expansion_range//2, expansion_range//4]:
                for corner_type in ['tl', 'tr', 'bl', 'br']:
                    if corner_type == 'tl':
                        c_x = seed_x - dx
                        c_y = seed_y + dy
                    elif corner_type == 'tr':
                        c_x = seed_x + dx
                        c_y = seed_y + dy
                    elif corner_type == 'bl':
                        c_x = seed_x - dx
                        c_y = seed_y - dy
                    else:  # br
                        c_x = seed_x + dx
                        c_y = seed_y - dy
                    
                    c_x = max(0, min(100000, c_x))
                    c_y = max(0, min(100000, c_y))
                    
                    if c_x != seed_x or c_y != seed_y:
                        candidates.append((c_x, c_y))
        
        return {
            "seed": (seed_x, seed_y),
            "expansion_range": expansion_range,
            "candidates": candidates[:20],
            "note": "approximate - actual fish coords not parsed"
        }
    
    # Actually compute mackerel-sardine balance around seed
    # Find bounding box that contains this mackerel
    min_x, max_x, min_y, max_y = seed_x, seed_x, seed_y, seed_y
    
    # Expand to include nearby mackerels
    for mx, my in mackerels[:1000]:  # Sample first 1000 mackerels
        if abs(mx - seed_x) < expansion_range and abs(my - seed_y) < expansion_range:
            min_x = min(min_x, mx)
            max_x = max(max_x, mx)
            min_y = min(min_y, my)
            max_y = max(max_y, my)
    
    # Clamp to valid range
    min_x = max(0, min_x)
    max_x = min(100000, max_x)
    min_y = max(0, min_y)
    max_y = min(100000, max_y)
    
    # If collapsed, expand
    if min_x == max_x and min_y == max_y:
        min_x -= expansion_range
        min_y -= expansion_range
    
    min_x = max(0, min_x)
    max_x = min(100000, max_x)
    min_y = max(0, min_y)
    max_y = min(100000, max_y)
    
    if min_x > max_x or min_y > max_y:
        min_x, max_x = 0, 100000
        min_y, max_y = 0, 100000
    
    candidates = [
        (min_x, min_y), (max_x, min_y), (min_x, max_y), (max_x, max_y)
    ]
    
    return {
        "seed": (seed_x, seed_y),
        "bounding_box": (min_x, min_y, max_x, max_y),
        "candidates": candidates,
        "mackerel_count": len(mackerels),
        "sardine_count": len(sardines)
    }
