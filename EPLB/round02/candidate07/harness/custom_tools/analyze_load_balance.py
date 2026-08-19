def run(ctx, args):
    import math
    program = ctx.get_program()
    # Since we can't execute Python here, we return a template response
    # The actual analysis should be done by the evaluator
    return {
        "note": "Run evaluate_solution first to get combined_score, then use this to diagnose",
        "recommended_action": "Analyze the score components (balance vs efficiency) in the evaluator output"
    }
