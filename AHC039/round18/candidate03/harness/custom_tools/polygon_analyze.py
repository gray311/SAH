def run(ctx, args):
    import math
    
    polygon = args.get("polygon", [])
    
    if len(polygon) < 4:
        return {
            "error": "Polygon must have at least 4 vertices",
            "vertex_count": 0,
            "perimeter": 0,
            "suggestion": "Add more vertices"
        }
    
    # Extract vertices
    if len(polygon) % 2 != 0:
        return {
            "error": "Polygon vertex list must have even length",
            "vertex_count": 0,
            "perimeter": 0
        }
    
    vertices = []
    for i in range(0, len(polygon), 2):
        x, y = int(polygon[i]), int(polygon[i+1])
        vertices.append((x, y))
    
    # Calculate perimeter
    perimeter = 0
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i+1) % len(vertices)]
        perimeter += abs(x2 - x1) + abs(y2 - y1)
    
    # Calculate bounding box
    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    # Calculate bounding box area
    bbox_area = (max_x - min_x) * (max_y - min_y)
    
    # Check self-intersection for axis-aligned polygon
    def check_self_intersection(n, verts):
        for i in range(n):
            for j in range(i+2, n):  # skip adjacent vertices
                if i == j + 1:
                    continue
                x1, y1 = verts[i]
                x2, y2 = verts[(i+1) % n]
                x3, y3 = verts[j]
                x4, y4 = verts[(j+1) % n]
                
                # Check if edges intersect (excluding endpoints)
                def ccw(A, B, C):
                    return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])
                
                def intersect(a, b, c, d):
                    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)
                
                if intersect((x1,y1), (x2,y2), (x3,y3), (x4,y4)):
                    return True
        return False
    
    self_intersect = check_self_intersection(len(vertices), vertices)
    
    # Check for distinct vertices
    has_duplicates = len(vertices) != len(set(v for v in vertices))
    
    # Check coordinate bounds
    coords_valid = all(0 <= x <= 100000 and 0 <= y <= 100000 for x, y in vertices)
    
    # Analyze vertex density and suggest improvements
    vertex_spacing = []
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i+1) % len(vertices)]
        dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        vertex_spacing.append(dist)
    
    avg_spacing = sum(vertex_spacing) / len(vertex_spacing)
    
    suggestions = []
    
    if perimeter > 400000:
        suggestions.append("PERIMETER_EXCEEDED: Reduce perimeter")
    
    if self_intersect:
        suggestions.append("SELF_INTERSECT: Polygon has self-intersection")
    
    if has_duplicates:
        suggestions.append("DUPLICATE_VERTICES: Remove duplicate vertices")
    
    if not coords_valid:
        suggestions.append("OUT_OF_BOUNDS: Some coordinates outside [0,100000]")
    
    # Estimate potential score based on bbox coverage (very rough)
    # Get fish coordinates from scratchpad
    scratch = ctx.scratch_read("fish_coords")
    if scratch:
        try:
            lines = scratch.strip().split('\n')
            # First half are mackerels, second half are sardines
            half = len(lines) // 2
            
            # Use a simple approximation: count fish in bbox using ray-casting logic
            m_in_bbox = 0
            s_in_bbox = 0
            
            for i in range(len(lines)):
                line = lines[i].strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    fx, fy = int(parts[0]), int(parts[1])
                    if min_x <= fx <= max_x and min_y <= fy <= max_y:
                        # This fish is in bbox (and thus in polygon for convex case)
                        if i < half:
                            m_in_bbox += 1
                        else:
                            s_in_bbox += 1
            
            estimated_score = max(0, m_in_bbox - s_in_bbox + 1)
        except:
            estimated_score = -1
    else:
        estimated_score = -1
    
    # Generate suggestions for refinement
    if avg_spacing > 5000:  # Vertices too sparse
        suggestions.append(f"SPARSE: Average vertex spacing {avg_spacing:.0f}, try adding vertices")
    elif avg_spacing < 100:  # Vertices too dense
        suggestions.append(f"DENSE: Average vertex spacing {avg_spacing:.0f}, consider simplifying")
    
    suggestions.append(f"Vertices: {len(vertices)}, Perimeter: {perimeter}, BBox: [{min_x},{min_y}] to [{max_x},{max_y}]")
    
    return {
        "vertex_count": len(vertices),
        "perimeter": perimeter,
        "min_x": min_x,
        "max_x": max_x,
        "min_y": min_y,
        "max_y": max_y,
        "bbox_area": bbox_area,
        "self_intersecting": self_intersect,
        "has_duplicates": has_duplicates,
        "coords_valid": coords_valid,
        "estimated_score": estimated_score,
        "suggestions": suggestions
    }
