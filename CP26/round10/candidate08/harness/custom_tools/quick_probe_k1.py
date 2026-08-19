def run(ctx, args):
    best = ctx.best_score()
    budget_left = ctx.budget_left()
    # Return analysis that helps the executor choose better packings
    analysis = {
        "best_score": best,
        "budget_left": budget_left,
        "recommendation": f"With {budget_left} evals left, use a hexagonal lattice construction with varied radii for corner optimization"
    }
    return analysis
