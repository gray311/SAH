def run(ctx, args):
    import numpy as np
    configs = [
        {"num_intervals": 400, "base_learning_rate": 0.01, "num_steps": 59000, "penalty_strength": 50, "num_restarts": 3, "seed_start": 0},
        {"num_intervals": 800, "base_learning_rate": 0.01, "num_steps": 100000, "penalty_strength": 30, "num_restarts": 5, "seed_start": 0},
        {"num_intervals": 1200, "base_learning_rate": 0.003, "num_steps": 200000, "penalty_strength": 100, "num_restarts": 3, "seed_start": 0},
        {"num_intervals": 1600, "base_learning_rate": 0.05, "num_steps": 59000, "penalty_strength": 61, "num_restarts": 3, "seed_start": 0},
        {"num_intervals": 400, "base_learning_rate": 0.1, "num_steps": 20000, "penalty_strength": 200, "num_restarts": 10, "seed_start": 0},
        {"num_intervals": 800, "base_learning_rate": 0.05, "num_steps": 200000, "penalty_strength": 10, "num_restarts": 5, "seed_start": 0}
    ]
    return {"configs": configs, "num_configs": 6}
