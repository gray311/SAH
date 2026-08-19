def run(ctx, args):
    prog = ctx.get_program()
    best = ctx.get_best_program()
    
    result = {
        "support_hint": "[-3, 3] (default seed range)",
        "num_steps_hint": "Check interval boundaries in code",
        "peak_hint": "Central peak around index 0.4-0.6*n",
        "tail_hint": "Tails decay to zero at boundaries",
        "recommendation": "Try extended support [-4, 4] or asymmetric tails",
        "note": "Use this to guide generate_candidates with different tail modes"
    }
    return result
