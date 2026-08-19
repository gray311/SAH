def run(ctx, args):
    max_coords = args.get("max_coords", 200)
    
    # Get program and parse fish positions
    program = ctx.get_program()
    
    # Parse mackerel coordinates from the code
    mackerels = []
    sardines = []
    
    lines = program.split('\n')
    for line in lines:
        line = line.strip()
        # Look for fish positions in input parsing
        if 'mackerel' in line.lower() and 'x' in line and 'y' in line:
            try:
                import re
                match = re.search(r'x\s*=\s*(\d+).*?y\s*=\s*(\d+)', line)
                if match:
                    x = int(match.group(1))
                    y = int(match.group(2))
                    mackerels.append((x, y))
            except:
                pass
        elif 'sardine' in line.lower() and 'x' in line and 'y' in line:
            try:
                import re
                match = re.search(r'x\s*=\s*(\d+).*?y\s*=\s*(\d+)', line)
                if match:
                    x = int(match.group(1))
                    y = int(match.group(2))
                    sardines.append((x, y))
            except:
                pass
    
    if not mackerels:
        return {"error": "no mackerels found", "note": "extract coordinates from input"}
    
    # Extract unique coordinates
    unique_x = sorted(set(x for x, y in mackerels))[:max_coords]
    unique_y = sorted(set(y for x, y in mackerels))[:max_coords]
    
    if not unique_x or not unique_y:
        return {"error": "invalid coordinates", "note": "ensure mackerels parsed"}
    
    # Build prefix sum grids (simplified - actual implementation would be in C++)
    # For this tool, return the candidate rectangles
    candidates = []
    for x1 in unique_x:
        for x2 in unique_x:
            if x1 <= x2:
                for y1 in unique_y:
                    for y2 in unique_y:
                        if y1 <= y2:
                            # Check perimeter constraint
                            perimeter = 2 * ((x2 - x1) + (y2 - y1))
                            if perimeter <= 400000:
                                candidates.append({
                                    'x1': x1, 'y1': y1,
                                    'x2': x2, 'y2': y2,
                                    'perimeter': perimeter
                                })
    
    # Return top candidates (in real implementation, would score them)
    return {
        "num_candidates": len(candidates),
        "max_coords": max_coords,
        "unique_x_count": len(unique_x),
        "unique_y_count": len(unique_y),
        "note": f"Found {len(candidates)} valid rectangles with perimeter <= 400000"
    }
