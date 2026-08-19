def run(ctx, args):
    import json
    try:
        poly = json.loads(args.get('polygon', '[]'))
    except:
        return {"note": "invalid polygon JSON", "estimate": 0}
    if len(poly) < 4:
        return {"note": "polygon too small", "estimate": 0}
    perimeter = 0
    for i in range(len(poly)):
        p1 = poly[i]
        p2 = poly[(i+1) % len(poly)]
        perimeter += abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
    return {"perimeter": perimeter, "vertices": len(poly), "estimate_note": "coarse heuristic, use for ranking only", "estimate": min(1000, perimeter // 100 + len(poly))}
