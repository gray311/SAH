def run(ctx, args):
    import math
    
    region_focus = args.get("region_focus", "global")
    num_candidates = args.get("num_candidates", 10)
    
    # Get program to access program state
    program = ctx.get_program()
    
    result = {
        "analysis": "KD-tree query-based analysis recommended",
        "candidates": [],
        "method": "rect_random_sampling"
    }
    
    # Suggest rectangle corners based on coordinate ranges
    # The solver should use actual KD-tree queries for exact scoring
    result["note"] = "Use this for initial candidate generation only. Score candidates with KD-tree queries."
    
    return result
