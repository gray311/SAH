def run(ctx, args):
    max_distance = args.get("max_distance", 10000)
    
    # Get program and extract fish coordinates
    program = ctx.get_program()
    lines = program.split('\n')
    
    mackerels = []
    sardines = set()
    
    # Parse mackerels and sardines from program
    for i, line in enumerate(lines):
        line = line.strip()
        if i < 5000:  # N=5000
            # Look for patterns like mackerels[i] = {x: ..., y: ...}
            # or direct coordinate assignments
            if 'mackerel' in line.lower() or i < 5000:
                try:
                    # Extract coordinates from various formats
                    x_match = line.split('=')[1].split(':')[0].strip() if '=' in line else line
                    if 'x' in line and 'y' in line:
                        # Try to extract x, y
                        pass
                except:
                    pass
    
    # Since we can't reliably parse the C++ program, return a note
    # The actual implementation must be in the EVOLVE-BLOCK
    return {"note": "Use point-level clustering with distance threshold ~10000, compute tight BBoxes per cluster, expand to exclude sardines"}
