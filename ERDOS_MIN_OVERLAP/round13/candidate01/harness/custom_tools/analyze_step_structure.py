def run(ctx, args):
    import numpy as np
    best_h = ctx.get_best_program()
    # Parse the best program to extract key parameters
    N = 800
    # Read input sample to understand structure
    try:
        best_score = ctx.best_score()
        # Suggest parameter adjustments based on current score
        if best_score < 0.380923 * 0.98:
            return {"suggestion": "Current solution promising, try fewer restarts to refine", "params": {"num_restarts": 10, "num_steps": 5000}}
        elif best_score < 0.380923 * 0.9:
            return {"suggestion": "Solution improving, try step function instead of smooth", "params": {"num_intervals": 50, "activation": "tanh"}}
        elif best_score < 0.380923:
            return {"suggestion": "Significant improvement, commit and refine", "params": {"num_restarts": 5, "num_steps": 10000, "penalty_strength": 30}}
        else:
            return {"suggestion": "Excellent progress, try to refine further", "params": {"num_intervals": 200, "num_restarts": 3}}
    except:
        return {"suggestion": "No best score available, try structural changes", "params": {"num_intervals": 50, "num_restarts": 5, "penalty_strength": 10}}