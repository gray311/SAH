def run(ctx, args):
    from collections import defaultdict
    
    program_text = ctx.get_program()
    mackerels = []
    sardines = []
    
    lines = program_text.split('\n')
    for line in lines:
        line_lower = line.lower()
        if 'mackerel' in line_lower:
            try:
                if '(' in line and ')' in line:
                    parts = line.split('(')[-1].split(')')[0].split(',')
                    if len(parts) >= 2:
                        x = int(parts[0].strip())
                        y = int(parts[1].strip())
                        mackerels.append((x, y))
            except:
                pass
        elif 'sardine' in line_lower:
            try:
                if '(' in line and ')' in line:
                    parts = line.split('(')[-1].split(')')[0].split(',')
                    if len(parts) >= 2:
                        x = int(parts[0].strip())
                        y = int(parts[1].strip())
                        sardines.append((x, y))
            except:
                pass
    
    bucket_size = 500
    mackerel_buckets = defaultdict(list)
    
    for x, y in mackerels:
        bx, by = (x // bucket_size, y // bucket_size)
        mackerel_buckets[(bx, by)].append((x, y))
    
    clusters = []
    for (bx, by), points in mackerel_buckets.items():
        if len(points) >= 5:
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            clusters.append({
                'type': 'mackerel',
                'bucket': (bx, by),
                'count': len(points),
                'center_x': sum(xs) // len(xs),
                'center_y': sum(ys) // len(ys),
                'coverage': (bx + 1) * bucket_size * (by + 1) * bucket_size
            })
    
    clusters.sort(key=lambda c: c['count'], reverse=True)
    
    return {
        'mackerel_clusters': clusters[:50],
        'total_mackerels': len(mackerels),
        'total_sardines': len(sardines)
    }
