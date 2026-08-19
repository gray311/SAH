def run(ctx, args):
    import random
    config = args
    num_steps = config.get("num_steps", random.randint(3, 5))
    symmetric = config.get("symmetric", True)
    base_height = config.get("base_height", 1.0)
    peak_position = config.get("peak_position", 0.0)
    
    # Generate structured step configuration
    if symmetric:
        # Symmetric step function centered at peak_position
        half_width = random.uniform(0.3, 0.5)
        # Inner height (main plateau)
        inner_height = base_height * random.uniform(1.0, 1.5)
        # Outer heights (wings)
        outer_height = base_height * random.uniform(0.5, 0.8)
        
        intervals = [
            (-half_width - random.uniform(0.1, 0.2), -half_width + random.uniform(0.1, 0.2), outer_height),
            (-half_width + random.uniform(0.1, 0.2), half_width - random.uniform(0.1, 0.2), inner_height),
            (half_width - random.uniform(0.1, 0.2), half_width + random.uniform(0.1, 0.2), outer_height)
        ]
        
        # Add optional outer wings if more steps needed
        if num_steps >= 4:
            wing_width = random.uniform(0.15, 0.25)
            wing_height = base_height * random.uniform(0.3, 0.5)
            intervals = [
                (-half_width - wing_width - random.uniform(0.1, 0.15), -half_width - wing_width + random.uniform(0.1, 0.15), wing_height),
                (-half_width - random.uniform(0.1, 0.2), -half_width + random.uniform(0.1, 0.2), outer_height),
                (-half_width + random.uniform(0.1, 0.2), half_width - random.uniform(0.1, 0.2), inner_height),
                (half_width - random.uniform(0.1, 0.2), half_width + random.uniform(0.1, 0.2), outer_height),
                (half_width + random.uniform(0.1, 0.15), half_width + wing_width - random.uniform(0.1, 0.15), wing_height)
            ]
        
        return {
            "type": "symmetric",
            "intervals": intervals,
            "num_steps": len(intervals),
            "params": {
                "inner_height": inner_height,
                "outer_height": outer_height,
                "wing_height": wing_height if num_steps >= 4 else None,
                "half_width": half_width
            },
            "peak_position": peak_position
        }
    else:
        # Asymmetric step function with peak at peak_position
        step_width = random.uniform(0.12, 0.18)
        centers = []
        heights = []
        
        # Create 2-4 asymmetric peaks
        if num_steps == 2:
            # Single asymmetric peak
            center = peak_position + random.uniform(-0.3, 0.3)
            height = base_height * random.uniform(1.0, 1.5)
            centers.append(center)
            heights.append(height)
        elif num_steps == 3:
            # Three peaks
            base_center = peak_position
            offsets = [-0.25, 0.0, 0.25]
            for offset in offsets:
                c = base_center + offset
                h = base_height * random.uniform(0.8, 1.4)
                centers.append(c)
                heights.append(h)
        elif num_steps == 4:
            # Four peaks with main peak at center
            centers = [peak_position - 0.35, peak_position - 0.15, peak_position + 0.15, peak_position + 0.35]
            heights = [base_height * 0.7, base_height * 1.3, base_height * 1.3, base_height * 0.7]
        else:
            # 5 steps: bimodal
            centers = [peak_position - 0.4, peak_position - 0.2, peak_position + 0.2, peak_position + 0.4]
            heights = [base_height * 0.8, base_height * 1.2, base_height * 1.2, base_height * 0.8]
        
        intervals = [(c - step_width, c + step_width, h) for c, h in zip(centers, heights)]
        
        return {
            "type": "asymmetric",
            "intervals": intervals,
            "num_steps": len(intervals),
            "params": {
                "centers": centers,
                "heights": heights,
                "step_width": step_width
            },
            "peak_position": peak_position
        }
