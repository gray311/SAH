def run(ctx, args):
    import random, math
    
    max_clusters = args.get("max_clusters", 10)
    search_radius = args.get("search_radius", 5000)
    
    # Get fish data from program or context
    program = ctx.get_program()
    
    # In actual implementation:
    # 1. Parse all fish from input
    # 2. Build KD-tree if not already done
    # 3. Sample random points
    # 4. For each sample, query KD-tree for fish in radius
    # 5. Return cluster centers with fish counts
    
    return {
        "method": "KD-tree sampling",
        "max_clusters": max_clusters,
        "search_radius": search_radius,
        "note": "Sample points, expand to radius, count fish. Use in C++ with KD-tree."
    }
