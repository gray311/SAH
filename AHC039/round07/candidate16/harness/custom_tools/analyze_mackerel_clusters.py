def run(ctx, args):
    # Get program to find mackerel positions
    prog = ctx.get_program()
    
    # This is a hint for the C++ code to analyze clusters
    # The C++ implementation should:
    # 1. Group mackerels by 50x50 grid cells
    # 2. Find cells with most mackerels
    # 3. Return cluster centers for candidate generation
    
    # For now, return a note guiding the C++ code
    return {
        "note": "C++ code should: 1) Group mackerels by 50x50 grid cells, 2) Find top dense cells, 3) Use their centers as rectangle candidates",
        "cluster_centers": [],
        "suggested_offsets": [-200, -150, -100, -50, 0, 50, 100, 150, 200]
    }
