def run(ctx, args):
    return {
        "patterns": [
            {"name": "single_interval", "code": "h=1 for x in [0,1], 0 elsewhere", "integral": 1.0},
            {"name": "uniform", "code": "h=0.5 everywhere", "integral": 1.0},
            {"name": "two_bumps", "code": "h=1 for x in [0,0.5] U [1,1.5]", "integral": 1.0},
            {"name": "centered_scaled", "code": "h=2/3 for x in [0.25,1.75]", "integral": 1.0},
            {"name": "four_sections", "code": "h=0.5 on four quarters", "integral": 1.0}
        ],
        "count": 5
    }
