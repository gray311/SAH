def run(ctx, args):
    """Analyze current best program and provide guidance."""
    best = ctx.get_best_program()
    if best is None:
        return {"note": "no best program yet"}
    
    # Look for pattern indicators
    lines = best.split('\n')
    integral_ok = 'integral=1.0' in best or 'sum(h)*dx' in best
    
    # Count pattern types mentioned
    pattern_keywords = ['golomb', 'bipartite', 'tri-modal', 'threshold', 'random']
    patterns_found = [p for p in pattern_keywords if p in best.lower()]
    
    return {
        "has_best_program": best is not None,
        "best_lines": len(lines),
        "patterns_in_seed": patterns_found,
        "recommendation": f"Use diverse patterns including: {patterns_found}"
    }
