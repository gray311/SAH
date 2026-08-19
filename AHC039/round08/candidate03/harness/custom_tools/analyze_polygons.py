def run(ctx, args):
    cell_size = 200
    grid_size = 500
    # Build spatial hash and analyze fish distribution
    # Return top clusters for polygon seeding
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no task inputs found", "clusters": []}
    
    # Parse task inputs to get fish positions (mackerels and sardines)
    # For this task, fish are in standard input, not files
    # We'll use ctx.get_program() to access the current program state
    
    # Create grid and populate with fish counts
    grid = [[{'m': 0, 's': 0} for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Note: Actual fish data comes from stdin in C++ program
    # This tool provides guidance for C++ implementation
    return {
        "grid_size": grid_size,
        "cell_size": cell_size,
        "recommendation": "Build 500x500 hash grid in C++, count M and S per cell, find top 10 clusters by (M-S) score",
        "note": "Use this guidance to implement analyze_polygons in C++ code"
    }
