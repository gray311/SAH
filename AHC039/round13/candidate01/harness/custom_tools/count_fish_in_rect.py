def run(ctx, args):
    import math
    
    min_x = args.get("min_x", 0)
    max_x = args.get("max_x", 100000)
    min_y = args.get("min_y", 0)
    max_y = args.get("max_y", 100000)
    
    # Try to get fish data from context
    # In actual implementation, would parse program or use KD-tree
    program = ctx.get_program()
    
    # Extract fish positions from the C++ code
    mackerels = []
    sardines = []
    
    # Look for parsed fish data or use input file reader
    try:
        # Try to read fish input files if available
        input_files = ctx.list_task_inputs()
        if input_files:
            # Read and parse fish data
            pass
    except:
        pass
    
    # For now, return a structure that the C++ code can use
    return {
        "min_x": min_x,
        "max_x": max_x,
        "min_y": min_y,
        "max_y": max_y,
        "note": "Use this rectangle in C++ code for KD-tree query"
    }
