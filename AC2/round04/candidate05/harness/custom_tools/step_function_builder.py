def run(ctx, args):
    import numpy as np
    n = ctx.hypers.num_intervals if hasattr(ctx, 'hypers') else 300
    result = []
    if 'multi_step' in args and args['multi_step']:
        levels = [float(x) for x in args['multi_step'].split(',')]
        segments = len(levels) - 1
        segment_width = 1.0 / segments
        offsets = [(0.1 + i * segment_width * 0.5) for i in range(segments)]
        f = np.zeros(n)
        for i, (level, offset) in enumerate(zip(levels, offsets)):
            start = int(offset * n)
            end = int((offset + segment_width) * n)
            f[start:end] = level
        result.append(f.tolist())
    else:
        start_ratio = args.get('start_ratio', 0.0)
        end_ratio = args.get('end_ratio', 1.0)
        height = args.get('height', 1.0)
        start = int(start_ratio * n)
        end = int(end_ratio * n)
        f = np.zeros(n)
        f[start:end] = height
        result.append(f.tolist())
    if len(result) == 1:
        return {"function": result[0], "n_intervals": n, "pattern": args.get('multi_step', 'single_step')}
    return {"functions": result, "n_intervals": n, "patterns": [args.get('multi_step', 'single_step') for _ in result]}