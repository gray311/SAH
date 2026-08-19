def run(ctx, args):
    best = ctx.best_score()
    left = ctx.budget_left()
    return {"best_score": best, "budget_left": left}


def analyze_progress(ctx, args):
    """Additional analysis: compare current vs best configuration."""
    best_score = ctx.best_score()
    budget = ctx.budget_left()
    
    # Provide strategic guidance based on state
    guidance = []
    if best_score is not None and best_score < 2.6:
        guidance.append("CURRENT SCORE BELOW ALPHAevOLVE RECORD (2.635)")
        guidance.append("CONSIDER: hexagonal packing, asymmetric zones, or rotated lattice")
    if budget < 10:
        guidance.append("LOW BUDGET: make final edit countable, then finish")
    
    return {
        "best_score": best_score,
        "budget_left": budget,
        "guidance": guidance
    }
