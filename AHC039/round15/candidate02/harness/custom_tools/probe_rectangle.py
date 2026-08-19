def run(ctx, args):
    import json
    
    xmin = args.get("xmin", 0)
    ymin = args.get("ymin", 0)
    xmax = args.get("xmax", 100000)
    ymax = args.get("ymax", 100000)
    
    # Parse input to get fish coordinates from C++ program context
    program = ctx.get_program()
    
    # Since we cannot directly access input files in probe tool
    # we return a placeholder indicating the need for proper setup
    return {
        "xmin": xmin,
        "ymin": ymin,
        "xmax": xmax,
        "ymax": ymax,
        "note": "probe_rectangle provides quick rectangle scoring. In practice this tool requires input data access. Use for ranking box candidates."
    }
