def run(ctx, args):
    # Get all mackerel positions from input
    names = ctx.list_task_inputs()
    if not names:
        return {"candidates": []}
    
    # Read input data
    # Format: first N lines are mackerels, next N are sardines
    # We need to parse the C++ program's fish data
    
    # For now, return a placeholder that the C++ code should implement
    # The scanner should extract unique x,y coords from mackerels
    # and generate all valid rectangles
    
    return {
        "note": "rectangle_scanner: C++ code should implement coordinate quantization",
        "strategy": "Extract unique sorted x and y from mackerels, generate all 4-point combinations"
    }
