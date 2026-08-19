def run(ctx, args):
    grid_x = args.get("grid_x", [])
    grid_y = args.get("grid_y", [])
    k = args.get("k", 5)
    shape = args.get("shape", "rectangle")
    
    candidates = []
    
    # Normalize to integers
    grid_x = [item if isinstance(item, int) else item.get(0) if isinstance(item, dict) else int(item) for item in grid_x[:k]] if grid_x else []
    grid_y = [item if isinstance(item, int) else item.get(0) if isinstance(item, dict) else int(item) for item in grid_y[:k]] if grid_y else []
    
    if len(grid_x) < 2 or len(grid_y) < 2:
        return {"note": "Need at least 2 grid lines in each dimension", "candidates": []}
    
    min_x, max_x = min(grid_x), max(grid_x)
    min_y, max_y = min(grid_y), max(grid_y)
    
    # Candidate 1: Bounding rectangle
    poly_rect = [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]
    perim_rect = 2*(max_x-min_x) + 2*(max_y-min_y)
    candidates.append({
        "name": "bounding_rect",
        "vertices": poly_rect,
        "perimeter": perim_rect,
        "valid": perim_rect <= 400000,
        "shape_type": "rectangle",
        "description": "Single rectangle enclosing all mackerels"
    })
    
    # Candidate 2: L-shape
    split_x1, split_x2 = sorted(grid_x)[:2]
    lshape_poly = [(min_x, min_y), (split_x1, min_y), (split_x1, max_y), (min_x, max_y)]
    perim_l = sum(abs(lshape_poly[i][0]-lshape_poly[i+1][0]) + abs(lshape_poly[i][1]-lshape_poly[i+1][1]) for i in range(3))
    candidates.append({
        "name": "lshape",
        "vertices": lshape_poly,
        "perimeter": perim_l,
        "valid": perim_l <= 400000 and len(lshape_poly) >= 4,
        "shape_type": "lshape",
        "description": "L-shape using vertical split at grid_x[1]"
    })
    
    # Candidate 3: Two-rectangle union
    poly1 = [(grid_x[0], grid_y[0]), (grid_x[1], grid_y[0]), (grid_x[1], grid_y[1]), (grid_x[0], grid_y[1])]
    poly2 = [(grid_x[1], grid_y[1]), (grid_x[1], grid_y[2] if len(grid_y)>2 else grid_y[1]), (grid_x[2] if len(grid_x)>2 else grid_x[1], grid_y[2] if len(grid_y)>2 else grid_y[1]), (grid_x[1], grid_y[1])]
    candidates.append({
        "name": "two_rect_union",
        "rectangles": [poly1, poly2],
        "valid": len(poly1) >= 4,
        "shape_type": "union",
        "description": "Union of two rectangles at dense grid lines"
    })
    
    return {
        "grid_x_used": grid_x[:k],
        "grid_y_used": grid_y[:k],
        "candidates": candidates
    }
