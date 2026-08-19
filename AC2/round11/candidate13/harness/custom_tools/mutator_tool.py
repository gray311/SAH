def run(ctx, args):
    import re
    recent_c2 = args.get("recent_best_c2", ctx.best_score()) if args else ctx.best_score()
    force_div = args.get("force_diversity", False) if args else False
    
    # Generate diverse pattern architectures
    patterns = []
    
    # Always include some baseline diversity
    patterns.append({
        "name": "asymmetric_tall_peak",
        "heights": [0.8, 1.3, 2.2, 1.4, 0.9, 0.6],
        "intervals": [0.08, 0.18, 0.32, 0.52, 0.72, 0.88],
        "rationale": "Single dominant peak with asymmetric shoulders"
    })
    
    patterns.append({
        "name": "irregular_multi_step",
        "heights": [0.65, 1.15, 1.85, 1.25, 1.75, 0.95],
        "intervals": [0.06, 0.22, 0.42, 0.60, 0.78, 0.92],
        "rationale": "Non-uniform spacing with varying height profile"
    })
    
    patterns.append({
        "name": "tripod_asymmetric",
        "heights": [0.7, 1.9, 2.4, 1.5, 0.8],
        "intervals": [0.10, 0.26, 0.44, 0.64, 0.82],
        "rationale": "Three peaks with central dominance"
    })
    
    patterns.append({
        "name": "smoothed_step_variant",
        "heights": [0.85, 1.45, 2.05, 1.65, 1.25],
        "intervals": [0.12, 0.28, 0.48, 0.68, 0.86],
        "rationale": "Gradual height progression"
    })
    
    if force_div:
        # Add more extreme variants
        patterns.append({
            "name": "extreme_asymmetry",
            "heights": [0.5, 1.1, 2.8, 1.0, 0.5],
            "intervals": [0.05, 0.20, 0.45, 0.70, 0.90],
            "rationale": "Very high central peak, minimal wings"
        })
    
    # Build the complete method code
    code_lines = ["    def _create_step_initializer(self, n, pattern_idx):",
                 '        """Create step function with {} patterns""".format(len(patterns))',
                 "        f = jnp.zeros(n)",
                 "        n_divisions = int(0.94 * n)"]
    
    for i, pattern in enumerate(patterns):
        code_lines.append("        if pattern_idx == {}:".format(i))
        interval_lines = []
        for j, (height, interval) in enumerate(zip(pattern["heights"], pattern["intervals"])):
            interval_lines.append("            f = f.at[int({:.2f}*n):int({:.2f}*n)].set({})".format(interval, interval, height))
        code_lines.append("            f = f.at[0:].set(0.0)")
        for il in interval_lines:
            code_lines.append(il)
        code_lines.append("")
    
    code_lines.append("        return f")
    
    # Pad if needed to ensure diversity
    while len(patterns) < 8:
        patterns.append({
            "name": "generated_{}".format(len(patterns)),
            "heights": [0.5 + 0.3 * i for i in range(6)],
            "intervals": [0.1 + 0.15 * i for i in range(6)],
            "rationale": "Generated variant"
        })
        # Regenerate code
        code_lines = ["    def _create_step_initializer(self, n, pattern_idx):",
                     '        """Create step function with {} patterns""".format(len(patterns))',
                     "        f = jnp.zeros(n)",
                     "        n_divisions = int(0.94 * n)"]
        for i, pattern in enumerate(patterns):
            code_lines.append("        if pattern_idx == {}:".format(i))
            interval_lines = []
            for j, (height, interval) in enumerate(zip(pattern["heights"], pattern["intervals"])):
                interval_lines.append("            f = f.at[int({:.2f}*n):int({:.2f}*n)].set({})".format(interval, interval, height))
            code_lines.append("            f = f.at[0:].set(0.0)")
            for il in interval_lines:
                code_lines.append(il)
            code_lines.append("")
        code_lines.append("        return f")
    
    return {
        "patterns": patterns,
        "code": "\n".join(code_lines),
        "num_patterns": len(patterns),
        "note": "Diverse step pattern generator. Each pattern_idx (0-{}) creates a different architecture.".format(len(patterns)-1)
    }
