def run(ctx, args):
    import json
    try:
        poly = json.loads(args.get('polygon', '[]'))
        op = args.get('operation', 'expand')
        direction = args.get('direction', 'diagonal')
    except:
        return {"error": "invalid input"}
    if len(poly) < 4:
        return {"note": "too few vertices to transform"}
    new_poly = [list(v) for v in poly]
    if op == 'expand':
        dx = 100 if direction in ['e', 'diagonal'] else 50
        dy = 100 if direction in ['n', 'diagonal'] else 50
        if direction == 'n':
            new_poly = [[v[0], v[1]+dy] for v in poly]
        elif direction == 's':
            new_poly = [[v[0], v[1]-dy] for v in poly]
        elif direction == 'e':
            new_poly = [[v[0]+dx, v[1]] for v in poly]
        elif direction == 'w':
            new_poly = [[v[0]-dx, v[1]] for v in poly]
        else:
            expanded = []
            for v in poly:
                expanded.append([v[0], v[1]])
                expanded.append([v[0]+dx, v[1]])
                expanded.append([v[0], v[1]+dy])
                expanded.append([v[0]-dx, v[1]])
                expanded.append([v[0], v[1]-dy])
            new_poly = list(set(tuple(v) for v in expanded))
            new_poly = sorted(new_poly, key=lambda p: (p[0], p[1]))
    elif op == 'contract':
        dx = 50
        dy = 50
        new_poly = [[max(0, v[0]-dx), max(0, v[1]-dy)] for v in poly]
        new_poly = sorted(new_poly, key=lambda p: (p[0], p[1]))
    elif op == 'rotate':
        cx = sum(v[0] for v in poly) / len(poly)
        cy = sum(v[1] for v in poly) / len(poly)
        new_poly = []
        for v in poly:
            rx = v[0] - cx
            ry = v[1] - cy
            nx = cx + rx - ry
            ny = cy + rx + ry
            new_poly.append([round(nx), round(ny)])
        new_poly = sorted(new_poly, key=lambda p: (p[0], p[1]))
    elif op == 'add_vertex':
        if len(poly) > 4:
            i = (len(poly) - 4) % len(poly)
            p1, p2 = poly[i], poly[(i+1)%len(poly)]
            mid_x = (p1[0] + p2[0]) // 2
            mid_y = (p1[1] + p2[1]) // 2
            new_poly = poly[:i+1] + [[mid_x, mid_y]] + poly[i+1:]
    elif op == 'remove_vertex':
        if len(poly) > 5:
            i = (len(poly) - 5) % len(poly)
            new_poly = poly[:i] + poly[i+1:]
        else:
            return {"note": "cannot remove vertex with too few vertices"}
    return {"new_polygon": new_poly, "operation": op, "direction": direction}
