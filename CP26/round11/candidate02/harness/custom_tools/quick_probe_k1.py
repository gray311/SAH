def run(ctx, args):
    best = ctx.best_score()
    left = ctx.budget_left()
    return {"best_score": best, "budget_left": left}
