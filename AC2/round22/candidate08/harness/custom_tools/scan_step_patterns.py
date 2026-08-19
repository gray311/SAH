def run(ctx, args):
    return {
        "note": "Step patterns 0-11 available in seed",
        "patterns": [
            {
                "index": i,
                "peak_count": 2 if i in [2, 3, 4, 7, 8, 9, 11] else 1,
                "approx_heights": [1.4, 1.5, 1.6, [0.9, 1.9, 0.9], [1.1, 2.3, 1.4], 1.5,
                                  [0.7, 1.3, 1.7, 1.0], [5, 1, 1, 1, 1], [0.6, 1.0, 1.5, 1.2],
                                  [0.8, 1.6, 2.0, 1.4, 0.9], [1.2, 2.8], [3, 1, 1, 1, 1, 1, 1]],
                "strategy": "high_narrow" if i in [2, 11] else ("multi_level" if i >= 3 else "standard")
            }
            for i in range(12)
        ]
    }