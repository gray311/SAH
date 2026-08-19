def run(ctx, args):
    configs = [
        {
            "pattern_subset": [0, 1, 2, 3],
            "lrs": [0.01, 0.001],
            "penalties": [500, 5000],
            "num_steps": 59000
        },
        {
            "pattern_subset": [5, 6, 7, 8],
            "lrs": [0.02, 0.001, 0.0001],
            "penalties": [1000, 5000, 10000],
            "num_steps": 59000
        },
        {
            "pattern_subset": [9, 10, 11],
            "lrs": [0.015, 0.0005],
            "penalties": [3000, 8000],
            "num_steps": 59000
        },
        {
            "pattern_subset": [0, 1, 4, 5, 8],
            "lrs": [0.01, 0.001, 0.0001],
            "penalties": [1000, 5000, 15000],
            "num_steps": 59000
        }
    ]
    return {"configs": configs, "note": "Use with adaptive scheduler in edit_solution"}
