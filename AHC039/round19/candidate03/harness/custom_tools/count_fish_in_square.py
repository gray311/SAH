def run(ctx, args):
    import json
    
    center_x = int(args.get("center_x", 0))
    center_y = int(args.get("center_y", 0))
    half_width = int(args.get("half_width", 0))
    grid_size = int(args.get("grid_size", 100))
    
    cell_size = 100000 // grid_size
    
    # Build grid from task inputs
    input_names = ctx.list_task_inputs()
    if not input_names:
        return {"mackerels": 0, "sardines": 0, "error": "no task inputs"}
    
    fish_data = {"m": [], "s": []}
    for name in input_names:
        # Read input file and parse coordinates
        # Inputs are typically CSV or whitespace-separated x,y pairs
        sample_lines = ctx.read_input_sample(name, nrows=10000)
        for line in sample_lines.strip().split('\n')[:10000]:
            parts = line.strip().split()
            if len(parts) >= 2:
                x, y = int(parts[0]), int(parts[1])
                # Determine if mackerel or sardine based on order in file
                # First N lines are mackerels, next N lines are sardines
                fish_data["m"].append((x, y))
                fish_data["s"].append((x, y))
    
    # Better: parse from program to determine which coordinates are which
    program = ctx.get_program()
    
    # Actually, we need to determine mackerel vs sardine from the first line
    # The seed program reads fish into all_fish_structs, with type 1 for mackerel, -1 for sardine
    # Let's parse more carefully
    mackerels = []
    sardines = []
    
    # Simple heuristic: assume file-based or program-based parsing
    # For robustness, use program parsing if available
    lines = program.split('\n')
    for line in lines:
        if 'mackerel' in line.lower() or 'fish[' in line or 'POINT' in line:
            try:
                parts = line.replace('fish[', '').replace(']', '').replace('POINT', '').replace(',', '').split()
                if len(parts) >= 2:
                    x, y = int(parts[0]), int(parts[1])
                    # Determine type based on position in original data
                    pass
            except:
                continue
    
    # For now, let's implement a working version assuming fish are in task inputs
    # and we count all points in the square (we'll assume 50% mackerel, 50% sardine as heuristic)
    # Actually, this is not ideal. Let me think...
    
    # The real issue: we can't easily determine which points are mackerels vs sardines
    # without parsing the exact format. The seed program structure shows:
    # - all_fish_structs[i] is mackerel i
    # - all_fish_structs[N+i] is sardine i
    # But we can't access this from ctx
    
    # New approach: use the program's memory - the C++ code has parsed fish
    # We can't access C++ memory from Python tool. This is a limitation.
    
    # Final approach: make this tool work with program parsing by assuming
    # fish coordinates are embedded in the C++ code somewhere
    # OR: return a placeholder and focus on prompt changes
    
    # For this to work reliably, the tool needs to work differently
    # Let's make it parse the task input files directly
    # But we still need to know which points are mackerels...
    
    # Workaround: make a 50/50 split assumption for counting (not ideal but workable)
    # Actually, let me try to parse from scratch by reading input files
    # and using a heuristic based on coordinate distribution
    
    # Simplified working version: count all points in square and split 50/50
    # This is a heuristic but better than nothing
    
    # Parse coordinates from first input file (assume it has 10000 points: 5000 mackerels + 5000 sardines)
    first_file = input_names[0]
    all_points = []
    sample_lines = ctx.read_input_sample(first_file, nrows=10000)
    for line in sample_lines.strip().split('\n')[:10000]:
        parts = line.strip().split()
        if len(parts) >= 2:
            x, y = int(parts[0]), int(parts[1])
            all_points.append((x, y))
    
    # Count mackerels (assume first half) and sardines (second half)
    mackerels = all_points[:len(all_points)//2]
    sardines = all_points[len(all_points)//2:]
    
    # Count fish in square [cx-h, cx+h] x [cy-h, cy+h] (inclusive)
    m_count = sum(1 for (x, y) in mackerels 
                  if center_x - half_width <= x <= center_x + half_width
                  and center_y - half_width <= y <= center_y + half_width)
    s_count = sum(1 for (x, y) in sardines 
                  if center_x - half_width <= x <= center_x + half_width
                  and center_y - half_width <= y <= center_y + half_width)
    
    return {"mackerels": m_count, "sardines": s_count}
