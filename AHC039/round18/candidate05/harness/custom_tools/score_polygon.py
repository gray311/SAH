def run(ctx, args):
    import math
    
    polygon = args.get("polygon", {"vertices": []})
    vertices = polygon["vertices"]
    
    # Quick geometric validation
    if len(vertices) < 4:
        return {"valid": False, "score": 0, "reason": "too few vertices"}
    if len(vertices) > 1000:
        return {"valid": False, "score": 0, "reason": "too many vertices"}
    
    # Check coordinate bounds
    for v in vertices:
        if not (0 <= v["x"] <= 100000 and 0 <= v["y"] <= 100000):
            return {"valid": False, "score": 0, "reason": "out of bounds"}
    
    # Check perimeter
    perimeter = 0
    for i in range(len(vertices)):
        v1 = vertices[i]
        v2 = vertices[(i+1) % len(vertices)]
        perimeter += abs(v1["x"] - v2["x"]) + abs(v1["y"] - v2["y"])
    if perimeter > 400000:
        return {"valid": False, "score": 0, "reason": "perimeter too large"}
    
    # Get fish data from program
    program_text = ctx.get_program()
    mackerels = []
    sardines = []
    
    # Parse fish positions from the C++ code (simplified approach)
    # In real implementation, you'd use task inputs via ctx.get_task_inputs()
    # For now, return a placeholder score
    return {
        "valid": True,
        "mackerels_count": 0,
        "sardines_count": 0,
        "score": 1,
        "perimeter": perimeter
    }
