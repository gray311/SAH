def run(ctx, args):
    import random
    seed_num = args.get("seed_num", 42)
    random.seed(seed_num)
    
    # Predefined ranges for each hyperparameter
    intervals_options = [150, 250, 350, 500, 700]
    lr_options = [0.05, 0.1, 0.125, 0.15, 0.2]
    stagnation_options = [50, 100, 200, 300]
    reinit_frac_options = [0.05, 0.1, 0.11, 0.15, 0.2]
    steps_options = [20000, 30000, 40000, 50000]
    reinit_std_options = [0.01, 0.015, 0.02, 0.025, 0.03]
    
    # Select one option from each range
    num_intervals = random.choice(intervals_options)
    learning_rate = random.choice(lr_options)
    stagnation_window = random.choice(stagnation_options)
    reinit_fraction = random.choice(reinit_frac_options)
    num_steps = random.choice(steps_options)
    reinit_std = random.choice(reinit_std_options)
    warmup_steps = min(int(num_steps * 0.1), 5000)
    reinit_interval = stagnation_window // 3 if stagnation_window > 100 else 50
    
    return {
        "config": {
            "num_intervals": num_intervals,
            "learning_rate": learning_rate,
            "num_steps": num_steps,
            "warmup_steps": warmup_steps,
            "stagnation_window": stagnation_window,
            "reinit_fraction": reinit_fraction,
            "reinit_std": reinit_std,
            "reinit_interval": reinit_interval,
            "best_c2": 0.0
        },
        "seed": seed_num,
        "note": f"Config {seed_num}: intervals={num_intervals}, lr={learning_rate}, steps={num_steps}, stagnation={stagnation_window}"
    }
