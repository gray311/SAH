def run(ctx, args):
    poly_text = ctx.get_program()
    # Find vertex definition (look for arrays/vectors of points)
    import re
    # Extract vertex coordinates
    poly_section = ctx.scratch_read("poly_analysis")
    # Report basic stats for debugging
    return {
        "diagnosis": "search_not_improving",
        "recommendation": "check if vertex modification operators are active",
        "note": "examine main search loop, ensure it runs for ~1.8s"
    }