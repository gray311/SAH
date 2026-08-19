def run(ctx, args):
    import random
    random.seed(42)
    n = ctx.get_program().count('_create_step_initializer')
    if not n:
        n = 400
    population = []
    heights = [0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]
    base_widths = [0.2, 0.3, 0.4, 0.5, 0.6]
    
    for i in range(8):
        center = random.uniform(0.2, 0.8)
        width = random.choice(base_widths)
        height = random.choice(heights)
        height += random.uniform(-0.3, 0.3)
        
        # Multi-level pattern
        n_levels = random.randint(2, 4)
        pattern = []
        current_h = height
        for _ in range(n_levels):
            pattern.append((random.uniform(0, 1), current_h))
            current_h *= random.uniform(0.5, 0.8)
        
        pattern.sort(key=lambda x: x[0])
        population.append(pattern)
    
    return {"population": population, "num_patterns": len(population)}
