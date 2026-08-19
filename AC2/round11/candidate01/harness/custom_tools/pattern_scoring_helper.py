def run(ctx, args):
    n_patterns = args.get("n_patterns", 10)
    patterns = args.get("pattern_types", [])
    
    scores = []
    for i in range(n_patterns):
        pattern_type = patterns[i] if i < len(patterns) else f"variant_{i}"
        
        score = 0.0
        penalties = []
        
        if pattern_type in ["asymmetric", "smooth", "irregular"]:
            score += 0.3
        else:
            penalties.append("standard step pattern less likely to improve")
        
        if "smooth" in pattern_type.lower():
            score += 0.2
        
        if "asymmetric" in pattern_type.lower():
            score += 0.15
        
        if pattern_type in ["high_peak", "pyramid"]:
            penalties.append("high peaks may inflate L_inf norm")
            score -= 0.05
        
        scores.append({
            "variant": f"pattern_{i}",
            "type": pattern_type,
            "heuristic_score": score,
            "penalties": penalties,
            "recommendation": "probe" if score > 0.4 else "skip"
        })
    
    return {
        "pre_filter_results": scores,
        "recommendation": "Focus on variants with heuristic_score > 0.4"
    }
