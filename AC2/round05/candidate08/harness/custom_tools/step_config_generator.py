def run(ctx, args):
    import random
    config = args
    num_steps = config.get("num_steps", random.randint(3, 6))
    symmetric = config.get("symmetric", True)
    base_height = config.get("base_height", 1.0)
    
    # Generate step intervals centered around 0
    half_width = random.uniform(0.3, 0.6)
    step_width = 0.15 * random.uniform(0.8, 1.2)
    
    if symmetric:
        # Create symmetric step function
        # Pattern: [-half_width, 0]: left_height, [0, half_width]: right_height
        left_height = base_height * random.uniform(0.8, 1.2)
        right_height = base_height * random.uniform(0.8, 1.2)
        intervals = [
            (-half_width, 0, left_height),
            (0, half_width, right_height)
        ]
        if num_steps == 4:
            # Add outer wings
            outer_width = step_width * 2
            outer_height = base_height * 0.5
            intervals = [
                (-half_width - outer_width, -half_width, outer_height),
                (-half_width, 0, left_height),
                (0, half_width, right_height),
                (half_width, half_width + outer_width, outer_height)
            ]
        elif num_steps == 3:
            # Add single outer region
            intervals = [
                (-half_width, half_width + step_width, base_height)
            ] + intervals
        return {
            "type": "symmetric",
            "intervals": intervals,
            "num_steps": len(intervals),
            "params": {"left_height": left_height, "right_height": right_height, 
                     "half_width": half_width}
        }
    else:
        # Create asymmetric step function
        centers = [random.uniform(-0.5, 0.5) for _ in range(num_steps)]
        heights = [base_height * random.uniform(0.8, 1.5) for _ in range(num_steps)]
        step_width = 0.15
        intervals = [(c - step_width, c + step_width, h) for c, h in zip(centers, heights)]
        return {
            "type": "asymmetric",
            "intervals": intervals,
            "num_steps": len(intervals),
            "params": {"centers": centers, "heights": heights}
        }
