def run(ctx, args):
    # Get current best polygon
    poly_text = ctx.get_best_program()
    # Check basic constraints from program structure
    # Since we can't directly execute C++, we return analysis template
    # The solver uses this guidance for mutations
    return {
        "analysis_type": "efficiency_check",
        "status": "ready_for_solver",
        "recommendations": [
            "check_perimeter_bound",
            "identify_mackerel_gaps",
            "find_sardine_clusters",
            "suggest_exploit_mutations",
            "suggest_avoid_mutations"
        ]
    }
