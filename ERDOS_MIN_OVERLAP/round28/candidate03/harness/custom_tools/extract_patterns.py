def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    patterns = {
        "pattern_12_golomb": {
            "marks": [0.0, 0.4, 0.8, 1.2, 1.6],
            "width": 0.1,
            "height": 4.0,
            "offset": -2.0,
            "key_features": ["Golomb ruler", "5 marks", "equally spaced"],
            "mutation_suggestions": [
                "Try 4 marks: [0.0, 0.5, 1.0, 1.5]",
                "Try 6 marks: [0.0, 0.33, 0.67, 1.0, 1.33, 1.67]",
                "Adjust spacing: [0.0, 0.45, 0.9, 1.35, 1.8]",
                "Narrower marks: width=0.06 instead of 0.1"
            ],
            "est_c5": 0.372
        },
        "pattern_14_tri_modal": {
            "peaks": [0.4, 1.0, 1.6],
            "width": 0.12,
            "height": 4.0,
            "offset": -1.9,
            "key_features": ["Tri-modal", "3 narrow peaks", "symmetric"],
            "mutation_suggestions": [
                "Shift peaks left: [0.3, 0.9, 1.5]",
                "Shift peaks right: [0.5, 1.1, 1.7]",
                "Wider peaks: width=0.18",
                "Asymmetric peaks: [0.35, 1.0, 1.65]",
                "Different heights: peak heights [3.0, 3.5, 3.0]"
            ],
            "est_c5": 0.375
        },
        "pattern_13_bipartite": {
            "threshold": 0.5,
            "high_val": 3.0,
            "low_val": -3.0,
            "key_features": ["Bipartite", "single threshold", "two-level"],
            "mutation_suggestions": [
                "Move threshold: 0.4, 0.6, 0.7",
                "Asymmetric heights: high=4.0, low=-2.0",
                "Multi-threshold: add second threshold at 1.0"
            ],
            "est_c5": 0.380
        },
        "pattern_11_wide_region": {
            "region": [0.25, 1.75],
            "high_val": 2.5,
            "low_val": -2.5,
            "key_features": ["Wide region", "central plateau", "symmetric"],
            "mutation_suggestions": [
                "Narrower region: [0.3, 1.7]",
                "Wider region: [0.2, 1.8]",
                "Offset region: [0.2, 1.6]"
            ],
            "est_c5": 0.382
        },
        "pattern_10_middle": {
            "region": [0.5, 1.0],
            "high_val": 3.0,
            "low_val": -1.0,
            "key_features": ["Middle region", "asymmetric heights"],
            "mutation_suggestions": [
                "Wider middle: [0.4, 1.1]",
                "Narrower middle: [0.55, 0.95]",
                "Shifted middle: [0.6, 1.2]"
            ],
            "est_c5": 0.383
        },
        "pattern_0_random": {
            "key_features": ["Random normal baseline", "Gaussian distributed"],
            "mutation_suggestions": [
                "Scaled random: multiply by 1.2, 1.5, 2.0",
                "Shifted random: add constant offset",
                "Combine with sinusoidal: add sin/cos components"
            ],
            "est_c5": 0.385
        }
    }
    
    result = {}
    pattern_names = sorted(patterns.keys())
    
    if args.get("focus_pattern"):
        for name, data in patterns.items():
            if name.startswith(args["focus_pattern"]):
                result[name] = data
    else:
        result = patterns
    
    analysis = []
    for p in result:
        analysis.append({
            "pattern": p,
            "est_c5": patterns[p]["est_c5"],
            "features": patterns[p]["key_features"],
            "mutations": patterns[p]["mutation_suggestions"]
        })
    
    return {"patterns": analysis, "pattern_count": len(analysis)}
