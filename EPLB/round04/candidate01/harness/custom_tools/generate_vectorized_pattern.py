def run(ctx, args):
    pattern_type = args.get("pattern_type", "rank-assignment")
    
    patterns = {
        "rank-assignment": "Vectorized rank assignment pattern using simple division. Returns pack_idx and rank computed via torch.div and modulo operations. Eliminates all Python loops.",
        "weight-scatter": "Weight-aware scatter assignment pattern using sorted indices. Uses torch.sort with descending=True then assigns based on sorted positions. Better for skewed loads.",
        "bin-exhaustion": "Bin-exhaustion pattern that fills each pack to capacity before moving to next. Uses tensor masks for assignment. Good for uniform loads."
    }
    
    if pattern_type in patterns:
        return {"pattern_type": pattern_type, "pattern_desc": patterns[pattern_type]}
    else:
        return {"error": "Unknown pattern_type", "pattern_type": "rank-assignment", "pattern_desc": patterns["rank-assignment"]}
