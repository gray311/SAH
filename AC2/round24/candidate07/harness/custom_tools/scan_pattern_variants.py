def run(ctx, args):
    indices = args.get('pattern_indices', list(range(12)))
    results = []
    for idx in indices:
        pattern_names = [
            "high_peak_single", "higher_peak", "narrow_peak", "multi_level_m",
            "three_level_asymmetric", "two_high_steps", "four_level", "narrow_high_wings",
            "staircase", "novel_asymmetric", "wide_base_narrow_peak", "three_distinct_peaks"
        ]
        pattern_descs = [
            "Single high peak at center (height 1.40)", "Higher peak (height 1.50)",
            "Narrow high peak (height 1.60)", "Multi-level with high middle (0.90,1.90,0.90)",
            "Three-level asymmetric (1.10,2.30,1.40)", "Two high steps (1.50 each)",
            "Four-level function (0.70,1.30,1.70,1.00)", "Narrow high peak with wings",
            "Staircase pattern (0.60,1.00,1.50,1.20)", "Novel asymmetric (0.80,1.60,2.00,1.40,0.90)",
            "Wide base with narrow high peak (1.20,2.80)", "Three distinct peaks (1.50,2.50,1.50)"
        ]
        result = {
            "pattern_idx": idx,
            "pattern_name": pattern_names[idx],
            "description": pattern_descs[idx],
            "complexity": 10 + idx,
            "recommended_optimizer": "JAX gradient ascent on pattern parameters"
        }
        results.append(result)
    return {"scanned_patterns": results, "total_scanned": len(results)}
