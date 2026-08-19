def run(ctx, args):
    best_det = ctx.best_score()
    return {
        "best_det": float(best_det),
        "stuck_flag": False,
        "recommended_action": "Try different cooling schedule or higher initial temperature"
    }