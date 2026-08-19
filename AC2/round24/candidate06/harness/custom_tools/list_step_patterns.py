def run(ctx, args):
    patterns = [
        {"idx": 0, "name": "single_step", "heights": [1.40], "ranges": [[0.25, 0.75]], "peaks": 1, "symmetric": True},
        {"idx": 1, "name": "higher_peak", "heights": [1.50], "ranges": [[0.27, 0.73]], "peaks": 1, "symmetric": True},
        {"idx": 2, "name": "narrow_peak", "heights": [1.60], "ranges": [[0.30, 0.70]], "peaks": 1, "symmetric": True},
        {"idx": 3, "name": "multi_level_sym", "heights": [0.90, 1.90, 0.90], "ranges": [[0.15, 0.25], [0.25, 0.75], [0.75, 0.85]], "peaks": 1, "symmetric": True},
        {"idx": 4, "name": "asymmetric_tri", "heights": [1.10, 2.30, 1.40], "ranges": [[0.11, 0.21], [0.21, 0.49], [0.49, 0.71]], "peaks": 1, "symmetric": False},
        {"idx": 5, "name": "two_steps", "heights": [1.50, 1.50], "ranges": [[0.22, 0.38], [0.52, 0.82]], "peaks": 2, "symmetric": True},
        {"idx": 6, "name": "four_level", "heights": [0.70, 1.30, 1.70, 1.00], "ranges": [[0.06, 0.20], [0.20, 0.34], [0.34, 0.64], [0.64, 0.94]], "peaks": 1, "symmetric": False},
        {"idx": 7, "name": "narrow_with_wings", "heights": [0.60, 1.20, 2.20, 1.20, 0.60], "ranges": [[0.12, 0.18], [0.18, 0.28], [0.28, 0.72], [0.72, 0.82], [0.82, 0.88]], "peaks": 1, "symmetric": True},
        {"idx": 8, "name": "staircase", "heights": [0.60, 1.00, 1.50, 1.20], "ranges": [[0.06, 0.24], [0.24, 0.44], [0.44, 0.64], [0.64, 0.94]], "peaks": 1, "symmetric": False},
        {"idx": 9, "name": "wide_base_narrow_peak", "heights": [1.20, 2.80], "ranges": [[0.10, 0.90], [0.35, 0.65]], "peaks": 1, "symmetric": True},
        {"idx": 10, "name": "three_peaks", "heights": [1.50, 2.50, 1.50], "ranges": [[0.15, 0.30], [0.30, 0.40], [0.40, 0.50]], "peaks": 3, "symmetric": True},
        {"idx": 11, "name": "multi_peak_asy", "heights": [2.50, 2.50], "ranges": [[0.30, 0.40], [0.50, 0.60]], "peaks": 2, "symmetric": True}
    ]
    return {"patterns": patterns, "total": 12, "note": "Use these for HYBRIDIZATION: mix heights from different patterns"}