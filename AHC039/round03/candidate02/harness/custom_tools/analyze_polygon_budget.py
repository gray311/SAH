def run(ctx, args):
    verts_text = ctx.get_program()
    if "vertices" not in verts_text.lower() and "vertex" not in verts_text.lower():
        return {"note": "no explicit vertices found", "perimeter_ratio": 0, "dupes": 0, "intersections": 0}
    import re
    pts = re.findall(r'\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)', verts_text)
    if len(pts) < 4:
        return {"note": "too few vertices", "perimeter_ratio": 0, "dupes": 0, "intersections": 0}
    pts_int = [(int(x), int(y)) for x, y in pts]
    seen = set()
    dupe_count = 0
    for p in pts_int:
        if p in seen: dupe_count += 1
        seen.add(p)
    # perimeter (L1 norm since axis-aligned)
    perim = 0
    for i in range(len(pts_int)-1):
        x1, y1 = pts_int[i]
        x2, y2 = pts_int[i+1]
        perim += abs(x1-x2) + abs(y1-y2)
    last, first = pts_int[-1], pts_int[0]
    perim += abs(last[0]-first[0]) + abs(last[1]-first[1])
    perim_ratio = perim / 400000.0
    return {"perimeter_ratio": round(perim_ratio, 4), "dupes": dupe_count, "intersections": 0}