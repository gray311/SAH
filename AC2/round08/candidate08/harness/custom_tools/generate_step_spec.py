def run(ctx, args):
    import random
    import math
    random.seed(42)
    
    num_steps = random.choice(range(3, 9))
    symmetric = random.choice([True, False])
    
    # Generate boundaries as fixed fractions of domain [-10, 10]
    fractions = sorted([random.uniform(0.1, 0.9) for _ in range(num_steps - 1)])
    boundaries = [-10 + 20 * f for f in fractions]
    boundaries = [-10] + boundaries + [10]
    
    # Generate heights
    heights = [random.uniform(0.5, 2.5) for _ in range(num_steps)]
    
    # For symmetric case with even steps
    if symmetric and num_steps % 2 == 0:
        center = num_steps // 2
        heights = heights[:center+1] + heights[center-1::-1]
    
    return {
        "num_steps": num_steps,
        "symmetric": symmetric,
        "boundaries": boundaries,
        "heights": [round(h, 2) for h in heights[:num_steps]],
        "num_intervals": num_steps + 1
    }