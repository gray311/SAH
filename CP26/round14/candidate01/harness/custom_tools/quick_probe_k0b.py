def run(ctx, args):
    best = ctx.best_score()
    return {"best_score": best, "budget_left": ctx.budget_left()}
