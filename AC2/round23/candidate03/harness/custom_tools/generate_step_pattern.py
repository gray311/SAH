def run(ctx, args):
    import random
    random.seed(ctx.get_best_program() or 42)
    num_levels = random.randint(2, 5)
    peak_positions = sorted([random.uniform(0.2, 0.8) for _ in range(2 + num_levels - 2)])
    heights = [round(random.uniform(0.8, 2.5), 2) for _ in range(num_levels)]
    base_width = round(random.uniform(0.3, 0.7), 2)
    n_intervals = 600
    # Build step pattern
    intervals = []
    current = 0
    for i, pos in enumerate(peak_positions):
        start = int(n_intervals * peak_positions[i-1]) if i > 0 else 0
        end = int(n_intervals * peak_positions[i+1]) if i+1 < len(peak_positions) else int(n_intervals)
        height = heights[i % len(heights)]
        intervals.append((start, end, height))
    return {"num_levels": num_levels, "intervals": intervals, "base_width": base_width}
