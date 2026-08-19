def run(ctx, args):
    best = ctx.best_score()
    budget = ctx.budget_left()
    # Force structural rewrite: replace random-greedy with deterministic geometric constructor
    # Target: place center + hex ring + corners + edges + fill remaining with explicit positions
    # This beats random-greedy which wastes budget on unproductive searches
    return {"best_score": best, "budget_left": budget, "strategy": "deterministic_geometric"}
