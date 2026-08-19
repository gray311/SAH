def run(ctx, args):
    import math
    
    polygon = args.get("polygon", {"vertices": []})
    simplify = args.get("simplify", False)
    vertices = polygon.get("vertices", [])
    
    if len(vertices) < 4:
        return {"error": "Invalid polygon"}
    
    program = ctx.get_program()
    fish_data = []
    for line in program.split('\n'):
        line = line.strip()
        if 'mackerel' in line.lower() or 'sardine' in line.lower():
            if '[' in line and ']' in line:
                try:
                    coords = line.split('[')[1].split(']')[0].split(',')
                    if len(coords) >= 2:
                        x, y = int(coords[0]), int(coords[1])
                        fish_type = 1 if 'mackerel' in line.lower() else -1
                        fish_data.append((x, y, fish_type))
                except:
                    continue
    
    def point_in_polygon(point, poly):
        x, y = point
        inside = False
        n = len(poly)
        for i in range(n):
            x1, y1 = poly[i]
            x2, y2 = poly[(i+1) % n]
            if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
                inside = not inside
        return inside, point != poly[i]
    
    mackerels = 0
    sardines = 0
    for x, y, ftype in fish_data:
        inside, _ = point_in_polygon((x, y), vertices)
        if inside:
            if ftype == 1:
                mackerels += 1
            else:
                sardines += 1
    
    score = max(0, mackerels - sardines + 1)
    return {"mackerels": mackerels, "sardines": sardines, "score": score}
