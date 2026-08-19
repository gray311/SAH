def run(ctx, args):
    """Report best score and budget."""
    return {"best_score": ctx.best_score(), "budget_left": ctx.budget_left()}
