def run(ctx, args):
    import json
    import math

    program_text = ctx.get_program()
    mackerels = []
    for line in program_text.split('\n'):
        if 'mackerel' in line.lower() and '[' in line:
            try:
                coords = line.split('[')[1].split(']')[0].split(',')
                if len(coords) >= 2:
                    x, y = int(coords[0].strip()), int(coords[1].strip())
                    mackerels.append((x, y))
            except:
                continue

    if not mackerels:
        return {"clusters": []}

    clusters = []
    assigned = [False] * len(mackerels)

    for i, (x0, y0) in enumerate(mackerels):
        if assigned[i]:
            continue

        cluster = [(x0, y0)]
        assigned[i] = True

        for j in range(i + 1, len(mackerels)):
            if assigned[j]:
                continue
            x1, y1 = mackerels[j]
            dist = math.sqrt((x0 - x1)**2 + (y0 - y1)**2)
            if dist <= 5000:
                cluster.append(mackerels[j])
                assigned[j] = True

        if cluster:
            min_x = min(p[0] for p in cluster)
            max_x = max(p[0] for p in cluster)
            min_y = min(p[1] for p in cluster)
            max_y = max(p[1] for p in cluster)
            clusters.append({
                "points": cluster,
                "bbox": (min_x, min_y, max_x, max_y),
                "size": len(cluster)
            })

    return {"clusters": clusters}
