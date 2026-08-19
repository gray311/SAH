def run(ctx, args):
    import numpy as np
    best_score = args.get("current_best_score", 0.999968)
    eval_count = args.get("eval_count", 0)
    best_c5 = 0.38092303510845016 / best_score
    
    current_best = ctx.get_best_program()
    if not current_best:
        return {"mutations": [{"mutation": "increase_intervals",
                               "new_value": 1000,
                               "reason": "Better FFT accuracy"}]}
    
    hints = []
    if best_c5 > 0.375:
        hints.append("Current best c5 > 0.375, try finer discretization")
    
    # Suggest hyperparameter changes based on results
    mutations = []
    
    if eval_count < 5:
        mutations.append({
            "mutation": "increase_intervals",
            "new_value": 1000,
            "reason": "Finer discretization for better c5 estimation"
        })
        mutations.append({
            "mutation": "increase_penalty",
            "new_value": 80.0,
            "reason": "Stronger integral constraint enforcement"
        })
    
    if eval_count < 10:
        mutations.append({
            "mutation": "increase_restarts",
            "new_value": 5,
            "reason": "More restarts to escape local minima"
        })
        mutations.append({
            "mutation": "reduce_steps",
            "new_value": 30000,
            "reason": "Faster convergence, try different LR"
        })
    
    if eval_count < 15:
        mutations.append({
            "mutation": "adjust_lr",
            "new_value": 0.004,
            "reason": "Lower learning rate for more precise optimization"
        })
        mutations.append({
            "mutation": "increase_width",
            "new_value": 2.5,
            "reason": "Wider domain might capture different patterns"
        })
    
    # Select top 3-5 mutations
    mutations = mutations[:5]
    
    return {"mutations": mutations,
            "hints": hints,
            "best_c5_found": best_c5,
            "recommendation": f"Try {len(mutations)} mutations: {', '.join([m['mutation'] for m in mutations])}"}
