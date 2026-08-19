def run(ctx, args):
    best_program = ctx.get_best_program()
    import re
    params = {"num_intervals": 800, "base_learning_rate": 0.0053, "num_steps": 59000, 
             "penalty_strength": 1370.0, "num_restarts": 3}
    
    # Extract penalty strength
    penalty_match = re.search(r'penalty_strength:\s*([\d.]+)', best_program)
    if penalty_match:
        params["penalty_strength"] = float(penalty_match.group(1))
    
    # Extract learning rate
    lr_match = re.search(r'base_learning_rate:\s*([\d.]+)', best_program)
    if lr_match:
        params["base_learning_rate"] = float(lr_match.group(1))
    
    # Extract num_intervals
    intervals_match = re.search(r'num_intervals:\s*(\d+)', best_program)
    if intervals_match:
        params["num_intervals"] = int(intervals_match.group(1))
    
    analysis = {"current_params": params, "recommendations": []}
    
    # Suggestions based on best-known bound
    if params["penalty_strength"] > 5000:
        analysis["recommendations"].append("Consider reducing penalty_strength if optimizer is stuck")
    elif params["penalty_strength"] < 500:
        analysis["recommendations"].append("Increase penalty_strength to enforce integral constraint")
    
    if params["num_intervals"] < 400:
        analysis["recommendations"].append("Increase num_intervals for finer discretization")
    
    if params["base_learning_rate"] < 0.001:
        analysis["recommendations"].append("Increase learning rate for faster convergence")
    elif params["base_learning_rate"] > 0.1:
        analysis["recommendations"].append("Decrease learning rate for stable optimization")
    
    analysis["suggested_improvements"] = [
        "Try AdamW optimizer for better weight decay handling",
        "Consider learning rate scheduling (linear decay over num_steps)",
        "Explore num_intervals in [1600, 3200] for better function representation"
    ]
    
    return analysis
