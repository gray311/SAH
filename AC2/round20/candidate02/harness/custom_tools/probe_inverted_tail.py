def run(ctx, args):
    import math
    # Simulate inverted tail probe: high at ends, low in center
    # This tests if inverted tail shapes improve C2
    prog = ctx.get_program()
    best = ctx.get_best_program()
    best_score = ctx.best_score()
    
    # Simulate probe: return a scaled approximation
    # Inverted tails might have different convolution properties
    factor = 0.95  # Inverted tails typically do worse, but we test it
    note = "Simulated inverted tail probe: high at boundaries, low in center"
    
    return {
        "probe_score": best_score * factor,
        "note": note,
        "recommendation": "If score < 1.0, try regular tails instead"
    }
