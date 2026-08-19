def run(ctx, args):
    best_f = ctx.get_best_program()
    variants = []
    heights = [0.80, 1.00, 1.20, 1.40, 1.60, 1.80, 2.00]
    pattern_configs = [{"peak_fraction": 0.25, "width_fraction": 0.5, "heights": h} for h in heights]
    for i, cfg in enumerate(pattern_configs[:15]):
        variants.append({"type": "single_peak", "peak_fraction": cfg["peak_fraction"], "width_fraction": cfg["width_fraction"], "heights": cfg["heights"], "num_intervals": 600})
    multi_peak_configs = [{"peaks": [(0.15, 1.20), (0.45, 2.00), (0.80, 1.30)], "num_intervals": 600}, {"peaks": [(0.10, 1.00), (0.35, 2.50), (0.50, 2.50), (0.65, 1.00), (0.90, 1.00)], "num_intervals": 600}, {"peaks": [(0.20, 0.90), (0.40, 2.80), (0.60, 0.90)], "num_intervals": 600}, {"peaks": [(0.15, 1.10), (0.30, 2.30), (0.49, 1.40), (0.70, 1.40), (0.85, 1.10)], "num_intervals": 600}]
    for i, cfg in enumerate(multi_peak_configs):
        height_multipliers = [0.9, 1.0, 1.1, 1.2]
        for hm in height_multipliers:
            new_peaks = [(h * hm, p) for h, p in cfg["peaks"]]
            variants.append({"type": "multi_peak", "peaks": new_peaks, "num_intervals": cfg["num_intervals"]})
    asym_configs = [{"left_height": 1.0, "right_height": 1.8, "split": 0.4, "num_intervals": 600}, {"left_height": 1.2, "right_height": 2.2, "split": 0.35, "num_intervals": 600}, {"left_height": 1.5, "right_height": 2.5, "split": 0.3, "num_intervals": 600}, {"left_height": 1.8, "right_height": 3.0, "split": 0.25, "num_intervals": 600}, {"left_height": 2.0, "right_height": 2.8, "split": 0.4, "num_intervals": 600}]
    for cfg in asym_configs:
        variants.append({"type": "asymmetric", "left_height": cfg["left_height"], "right_height": cfg["right_height"], "split": cfg["split"], "direction": "left_skewed", "num_intervals": cfg["num_intervals"]})
        variants.append({"type": "asymmetric", "left_height": cfg["right_height"], "right_height": cfg["left_height"], "split": cfg["split"], "direction": "right_skewed", "num_intervals": cfg["num_intervals"]})
    gaussian_configs = [{"peak_height": 2.0, "base_height": 0.8, "peak_width": 0.4}, {"peak_height": 1.8, "base_height": 0.6, "peak_width": 0.5}, {"peak_height": 2.2, "base_height": 0.7, "peak_width": 0.35}, {"peak_height": 2.5, "base_height": 0.5, "peak_width": 0.3}, {"peak_height": 1.6, "base_height": 0.9, "peak_width": 0.55}]
    for cfg in gaussian_configs:
        variants.append({"type": "gaussian_like", "peak_height": cfg["peak_height"], "base_height": cfg["base_height"], "peak_width": cfg["peak_width"], "num_intervals": 600})
    wide_base_configs = [{"base_height": 1.0, "peak_height": 2.5, "peak_width": 0.2}, {"base_height": 0.8, "peak_height": 2.8, "peak_width": 0.15}, {"base_height": 1.2, "peak_height": 2.3, "peak_width": 0.25}, {"base_height": 0.9, "peak_height": 3.0, "peak_width": 0.1}, {"base_height": 1.1, "peak_height": 2.6, "peak_width": 0.18}]
    for cfg in wide_base_configs:
        variants.append({"type": "wide_base", "base_height": cfg["base_height"], "peak_height": cfg["peak_height"], "peak_width": cfg["peak_width"], "num_intervals": 600})
    return {"variants": variants[:45], "note": "Generated 45 diverse step-function variants for internal enumeration"}
