def run(ctx, args):
    import random
    num_vars = args.get("num_variants", 3)
    variants = []
    for i in range(min(2, num_vars)):
        num_locs = random.randint(2, 5)
        locs = sorted([random.uniform(0, 1) for _ in range(num_locs)])
        heights = [random.uniform(0.1, 1.0) for _ in range(num_locs + 1)]
        variants.append(("piecewise", locs, [max(0, h) for h in heights]))
    for i in range(min(1, num_vars)):
        freqs = [random.choice([0.5, 1.0, 1.5, 2.0])]
        amplitudes = [random.uniform(0.1, 0.5) for _ in freqs]
        variants.append(("fourier", freqs, amplitudes, [random.uniform(0, 6) for _ in freqs]))
    return {"variants": variants}
