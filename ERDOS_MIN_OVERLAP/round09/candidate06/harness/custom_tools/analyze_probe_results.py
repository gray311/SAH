def run(ctx, args):
    results = args.get("probe_results", [])
    if not results:
        return {"note": "No results to analyze"}
    sorted_results = sorted(results, key=lambda x: x.get("probe_score", 0), reverse=True)
    top3 = sorted_results[:3]
    best_lrs = [r["lr"] for r in top3]
    best_penalties = [r["penalty"] for r in top3]
    best_steps = [r["steps"] for r in top3]
    aggressive = any(r["lr"] > 0.01 for r in top3)
    low_penalty = any(r["penalty"] < 2000 for r in top3)
    long_steps = any(r["steps"] > 30000 for r in top3)
    return {
        "top3": top3,
        "patterns": {
            "has_aggressive_lr": aggressive,
            "has_low_penalty": low_penalty,
            "has_long_steps": long_steps
        },
        "recommendation": "Try full eval on top3 if probe_score > 0.9998"
    }
