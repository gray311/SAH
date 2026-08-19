def run(ctx, args):
    import numpy as np
    num_intervals = args.get("num_intervals", 800)
    pattern_type = args.get("pattern_type", "two_step")
    seed = args.get("seed", 42)
    N = num_intervals
    dx = 2.0 / N
    key = np.random.RandomState(seed)

    h = np.zeros(N)

    if pattern_type == "two_step":
        # h=1 on [0, 1], h=0 elsewhere (exact integral=1)
        mid = int(1.0 / dx)
        h[:mid] = 1.0

    elif pattern_type == "three_step_symmetric":
        # h=1 on [0,0.5] and [1.5,2], 0 elsewhere -> integral=1
        left_end = int(0.5 / dx)
        right_start = int(1.5 / dx)
        h[:left_end] = 1.0
        h[right_start:] = 1.0

        # Verify integral and constrain to [0,1]
        integral = np.sum(h) * dx
        if integral != 1.0:
            scale = 1.0 / integral
            h = np.clip(h * scale, 0, 1)

    elif pattern_type == "five_step":
        # h = 1 on [0,0.5] and [1,1.5], 0 elsewhere -> integral=1
        block1_end = int(0.5 / dx)
        block2_start = int(1.0 / dx)
        block2_end = int(1.5 / dx)
        h[:block1_end] = 1.0
        h[block2_start:block2_end] = 1.0

        integral = np.sum(h) * dx
        if integral != 1.0:
            scale = 1.0 / integral
            h = np.clip(h * scale, 0, 1)

    elif pattern_type == "waveform":
        # Sinusoidal pattern through sigmoid
        x = np.linspace(0, 2, N)
        freq = 2 * np.pi
        phase = 0.5
        base = 1.0 + 0.5 * np.sin(freq * x + phase)
        base = np.clip(base, 0.1, 2.0)
        h = 1.0 / (1.0 + np.exp(-(base - 1.0) / 0.5))

        # Scale to satisfy integral=1
        integral = np.sum(h) * dx
        if integral != 1.0 and integral > 0:
            h = np.clip(h / integral, 0, 1)

    elif pattern_type == "concentrated":
        # Two narrow peaks of height 1
        peak_width = int(0.25 / dx)
        h[0:peak_width] = 1.0
        h[N//2:N//2 + peak_width] = 1.0

        integral = np.sum(h) * dx
        if integral != 1.0 and integral > 0:
            scale = 1.0 / integral
            h = np.clip(h * scale, 0, 1)

    # Final constraint check: clip to [0,1]
    h = np.clip(h, 0.0, 1.0)

    # Ensure integral is exactly 1 (rescale if needed)
    integral = np.sum(h) * dx
    if integral > 0 and abs(integral - 1.0) > 1e-6:
        scale = 1.0 / integral
        h = np.clip(h * scale, 0, 1)

    return {"h": h.tolist(), "integral": float(np.sum(h) * dx),
            "pattern_type": pattern_type, "num_intervals": N}