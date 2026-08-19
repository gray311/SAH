def run(ctx, args):
    import random
    current = args.get("current_config", {})
    lr = current.get("learning_rate", 0.22)
    num_int = current.get("num_intervals", 400)
    num_steps = current.get("num_steps", 37000)
    warmup = current.get("warmup_steps", 3700)
    
    # Suggest small perturbations based on current values
    if random.random() < 0.4:
        # Tweak learning rate
        delta = 0.02 if lr < 0.24 else -0.02
        return {
            "parameter_name": "learning_rate",
            "current_value": lr,
            "suggested_value": round(lr + delta, 4),
            "reason": f"Adjusting LR by {delta:+.2f} to find optimal gradient step size"
        }
    elif random.random() < 0.4:
        # Tweak number of intervals
        delta = 20 if num_int < 420 else -20
        return {
            "parameter_name": "num_intervals",
            "current_value": num_int,
            "suggested_value": max(300, min(500, num_int + delta)),
            "reason": f"Changing discretization to {num_int + delta} for finer/coarser search"
        }
    else:
        # Tweak num_steps
        delta = 3000 if num_steps < 40000 else -3000
        return {
            "parameter_name": "num_steps",
            "current_value": num_steps,
            "suggested_value": max(20000, min(50000, num_steps + delta)),
            "reason": f"Extending/shortening optimization to {num_steps + delta} steps"
        }
    return {"error": "Failed to generate suggestion"}
