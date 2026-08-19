def run(ctx, args):
    code = ctx.get_program()
    return {
        "note": "Seed uses step-function optimization with FFT-based convolution.",
        "recommendation": "Understand the discretization (n_intervals=600) and pattern structure",
        "key_insight": "Step functions are LOCAL optima; orthogonal families (smooth, oscillatory) likely unexplored"
    }
