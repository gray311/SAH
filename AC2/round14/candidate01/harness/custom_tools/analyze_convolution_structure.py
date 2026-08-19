def run(ctx, args):
    best_score = ctx.best_score()
    if best_score is None or best_score <= 1.02:
        return {"note": "evaluate solution first to get combined_score"}
    
    # Return structured convolution analysis
    return {
        "current_score": best_score,
        "structural_insights": [
            "Concentrated convolution peaks favor high C₂",
            "Check for symmetry: asymmetry may reduce destructive interference",
            "Tail decay rate affects ||f★f||_∞ significantly",
            "Height concentration at convolution peaks improves L2/L∞ ratio"
        ],
        "recommended_mutations": [
            {"type": "height_concentration", "description": "Increase highest step by 0.08-0.12, decrease others"},
            {"type": "width_expansion", "description": "Expand core width by 5-8% to increase L2 more than L∞"},
            {"type": "symmetry_break", "description": "Make heights asymmetric: e.g., 1.40, 1.48, 1.32"},
            {"type": "local_bump", "description": "Add bump at 35-40% with height 0.3-0.5, width 8-15 intervals"}
        ],
        "next_steps": "Generate mutations based on top recommendation, then probe ALL variants"
    }
