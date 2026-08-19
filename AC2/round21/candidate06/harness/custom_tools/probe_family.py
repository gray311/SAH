def run(ctx, args):
    family = args.get('family_type', 'gaussian_mixture')
    seed = args.get('prototype_seed', 42)
    current_best = ctx.best_score() or 0.896
    result = ctx.probe(subsample=1000)
    approx_c2 = result.get('c2', 0.89)
    return {'family': family, 'approx_c2': approx_c2, 'probe_result': result.get('combined_score', 1.0), 'recommendation': 'promising' if approx_c2 > current_best else 'retry'}
