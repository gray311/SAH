def run(ctx, args):
    max_vertices = args.get('max_vertices', 1000)
    max_perimeter = args.get('max_perimeter', 400000)
    top_k = args.get('top_k', 5)
    
    # Generate default rectangles as candidates
    candidates = []
    for i in range(top_k):
        x_scale = 10000 * (i + 1)
        y_scale = 10000 * (i % 2 + 1)
        if x_scale + y_scale > max_perimeter:
            continue
        pts = [(0, 0), (x_scale, 0), (x_scale, y_scale), (0, y_scale)]
        if len(pts) <= max_vertices:
            candidates.append(pts)
    
    return {"candidates": candidates}
