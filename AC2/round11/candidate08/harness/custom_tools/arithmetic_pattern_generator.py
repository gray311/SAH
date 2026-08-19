def run(ctx, args):
    import math

    n_intervals = 450
    phi = (1 + math.sqrt(5)) / 2

    recipes = []

    # Recipe 1: Golden-Ratio Symmetric Pattern
    heights1 = [0.25, 0.55, 1.00, 0.55, 0.25]
    pos1 = [int(0.191 * n_intervals), int(0.382 * n_intervals), 
             int(0.500 * n_intervals), int(0.618 * n_intervals),
             int(0.809 * n_intervals)]
    recipes.append({
        "name": "golden_symmetric",
        "description": "Symmetric 5-level pattern with golden ratio positioning and peak height 1.0",
        "heights": [0.25, 0.55, 1.00, 0.55, 0.25],
        "positions": pos1,
        "rationale": "Golden section positioning optimizes convolution properties"
    })

    # Recipe 2: Arithmetic Progression Heights
    k = 5
    base = 1.0
    alpha = 0.6
    ap_heights = [base * (1 + i * alpha) for i in range(k)]
    ap_positions = [int((0.2 + 0.1 * i) * n_intervals) for i in range(k)]
    recipes.append({
        "name": "arithmetic_progression",
        "description": "5-level pattern with heights in arithmetic progression",
        "heights": [round(h, 2) for h in ap_heights],
        "positions": ap_positions,
        "rationale": "Arithmetic progression in heights may create favorable convolution profile"
    })

    # Recipe 3: Geometric Sequence Heights
    r = 1.5
    geoms = []
    for i in range(-3, 4):
        geoms.append(r ** i)
    geoms = [0.15 * h for h in geoms]
    geoms = [max(0.1, min(2.0, h)) for h in geoms]
    geom_positions = [int((0.1 + 0.2 * abs(i)) * n_intervals) for i in range(-3, 4)]
    recipes.append({
        "name": "geometric_sequence",
        "description": "Asymmetric 7-level pattern with geometric height sequence",
        "heights": [round(h, 2) for h in geoms],
        "positions": geom_positions,
        "rationale": "Geometric sequences may exploit scale invariance in convolution properties"
    })

    # Recipe 4: Fibonacci-Ratio Pattern
    fib_ratios = [0.5, 1.0, 2.0, 1.5, 1.0]
    fib_heights = [round(h * 0.8, 2) for h in fib_ratios]
    fib_positions = [int((0.06 + 0.2 * i) * n_intervals) for i in range(len(fib_ratios))]
    recipes.append({
        "name": "fibonacci_ratios",
        "description": "5-level pattern with heights based on Fibonacci ratios",
        "heights": fib_heights,
        "positions": fib_positions,
        "rationale": "Fibonacci ratios appear in natural optimization"
    })

    # Recipe 5: Exponential Decay Pattern
    peak_h = 1.8
    decay_rate = 0.3
    exp_heights = [peak_h * (1 - decay_rate * (i - 2)) for i in range(6)]
    exp_heights = [max(0.1, h) for h in exp_heights]
    exp_positions = [int((0.0 + 0.2 * i) * n_intervals) for i in range(6)]
    recipes.append({
        "name": "exponential_decay",
        "description": "6-level asymmetric pattern with exponential decay from peak",
        "heights": [round(h, 2) for h in exp_heights],
        "positions": exp_positions,
        "rationale": "Exponential decay may better model natural functions"
    })

    return {
        "recipes": recipes,
        "note": "Implement each recipe exactly as specified. Use exact heights and positions."
    }
