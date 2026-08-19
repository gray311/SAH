def run(ctx, args):
    import random
    random.seed(args.get("seed", 42))
    
    current = ctx.get_best_program()
    best_score = ctx.best_score()
    n_intervals = None
    
    for line in current.split('\n'):
        if 'num_intervals:' in line:
            n_intervals = int(line.split(':')[1].strip())
            break
    
    if n_intervals is None:
        return {"error": "Could not find num_intervals", "code": current}
    
    new_n = n_intervals
    if args["change_type"] == "reduce_intervals":
        new_n = max(50, int(n_intervals * (1 - args["magnitude"] / 100)))
    elif args["change_type"] == "increase_intervals":
        new_n = min(300, int(n_intervals * (1 + args["magnitude"] / 100)))
    
    modified = current.replace(
        f'num_intervals: int = {n_intervals}',
        f'num_intervals: int = {new_n}'
    )
    
    # If we changed intervals significantly, also adjust learning rate and steps
    modified = modified.replace(
        'learning_rate: float = 0.005',
        'learning_rate: float = 0.005'
    )
    modified = modified.replace(
        'num_steps: int = 20000',
        f'num_steps: int = {new_n * 100}'
    )
    
    # Probe the modified version
    ctx.stage_edit(modified)
    probe_result = ctx.probe(subsample=500)
    
    return {
        "code": modified,
        "change": f"num_intervals: {n_intervals} -> {new_n}",
        "probe_score": probe_result.get("c5_bound", "unknown")
    }
