def run(ctx, args):
    import json
    import re
    
    # Extract fish positions from the C++ code
    program = ctx.get_program()
    
    # Pattern to find coordinate assignments from input
    # Look for lines like: cin >> x >> y; or similar parsing patterns
    coords = []
    
    # Alternative: look for hardcoded coordinate arrays
    match = re.search(r"fish_data\s*=\s*\{([^}]*)}", program, re.DOTALL)
    if match:
        block = match.group(1)
        # Parse coordinate pairs
        coord_pattern = re.compile(r"(\d+)\s*,\s*(\d+)")
        for m in coord_pattern.finditer(block):
            coords.append((int(m.group(1)), int(m.group(2))))
    
    # If no fish data found in code, the solver should read from input
    # This tool is informational - the main strategy reads from stdin
    
    return {
        "note": "Read fish from stdin in C++ code, not from tool",
        "clusters": [],
        "instruction": "In your C++ edit_solution, read all 2N coordinates from input:\n                  - First N lines (after N): mackerels\n                  - Next N lines: sardines\n                  Use spatial hashing with resolution 100 to cluster mackerels"
    }