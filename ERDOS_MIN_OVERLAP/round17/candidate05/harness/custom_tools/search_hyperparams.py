def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    # Grid search over key hyperparameters
    configs = []
    
    # Config 1: Standard
    config1 = {
        "num_intervals": N,
        "base_learning_rate": 0.006,
        "penalty_strength": 60.0,
        "num_steps": 59000,
        "c5_estimate": 0.382
    }
    
    # Config 2: Higher penalty (sharper features)
    config2 = {
        "num_intervals": N,
        "base_learning_rate": 0.006,
        "penalty_strength": 120.0,
        "num_steps": 59000,
        "c5_estimate": 0.378
    }
    
    # Config 3: Lower penalty (smoother)
    config3 = {
        "num_intervals": N,
        "base_learning_rate": 0.006,
        "penalty_strength": 30.0,
        "num_steps": 59000,
        "c5_estimate": 0.381
    }
    
    # Config 4: Fewer intervals (coarser, faster)
    config4 = {
        "num_intervals": 400,
        "base_learning_rate": 0.01,
        "penalty_strength": 60.0,
        "num_steps": 59000,
        "c5_estimate": 0.379
    }
    
    # Config 5: More intervals (finer)
    config5 = {
        "num_intervals": 1200,
        "base_learning_rate": 0.004,
        "penalty_strength": 60.0,
        "num_steps": 59000,
        "c5_estimate": 0.380
    }
    
    candidates = [config1, config2, config3, config4, config5]
    return {"configs": candidates, "num_configs": len(candidates)}
