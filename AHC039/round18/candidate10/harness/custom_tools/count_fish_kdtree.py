def run(ctx, args):
    import json
    
    min_x = args.get("rect_min_x", 0)
    max_x = args.get("rect_max_x", 100000)
    min_y = args.get("rect_min_y", 0)
    max_y = args.get("rect_max_y", 100000)
    
    # The C++ program already has KD-tree built and query_kdtree_rectangle
    # This probe tool simulates the logic - actual counting happens in C++
    
    # Placeholder - in C++: query_kdtree_rectangle(root, min_x, max_x, min_y, max_y, indices)
    # Then count by type
    
    m = 0
    s = 0
    
    return {"rect": (min_x, max_x, min_y, max_y), "m": m, "s": s, "score": max(0, m - s + 1)}
