def run(ctx, args):
    import random
    h_best = ctx.get_best_program()
    
    suggestions = {
        "coarse-to-fine": (
            "Coarse-to-Fine Architecture:\n"
            "1. Start with 10-15 intervals, define h as simple step function\n"
            "2. Optimize positions and heights with simple local search\n"
            "3. Gradually increase to 50, 100, 200 intervals\n"
            "4. Use simulated annealing or hill climbing at each stage\n"
            "Code: main() with N=10, h as list of (position, height) pairs\n"
            "Optimization loop increases N and refines.\n"
            "Constraint: sum(heights) = 1 (for unit integral over [0,2])."
        ),
        "explicit-plateaus": (
            "Explicit Plateau Architecture:\n"
            "Define h(x) as sum of N rectangular plateaus:\n"
            "h(x) = sum_i h_i * I(p_i <= x < p_i + w_i)\n"
            "Variables: positions p_i (sorted), widths w_i, heights h_i\n"
            "Constraints: sum(h_i * w_i) = 1, all h_i in [0,1]\n"
            "Use simple hill climbing on (p_i, h_i)\n"
            "Start with N=3-5 plateaus, gradually increase."
        ),
        "sparse-peaks": (
            "Sparse Peaks Architecture:\n"
            "h(x) has only 3-5 narrow peaks at strategic positions.\n"
            "Example: peaks at x = 0.33, 1.0, 1.66 (roughly 1/3, 1, 5/3)\n"
            "Each peak: narrow width, height close to 1, small overlap region\n"
            "Benefits: Simple structure, easy constraint verification,\n"
            "natural separation between peaks reduces self-overlap."
        ),
        "symmetric-pattern": (
            "Symmetric Around Center Architecture:\n"
            "h(x) symmetric around x=1: h(x) = h(2-x)\n"
            "Define h for x in [0,1], then mirror to [1,2]\n"
            "Optimize only the left half\n"
            "Ensure integral over [0,2] equals 1\n"
            "Benefits: Regular structure, easier optimization."
        )
    }
    
    chosen_key = random.choice(list(suggestions.keys()))
    return {
        "architecture": chosen_key,
        "description": suggestions[chosen_key],
        "next_step": "Implement this architecture in edit_solution"
    }
