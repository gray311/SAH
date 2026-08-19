def run(ctx, args):
    import math
    current_score = args.get('current_score', 0)
    recent_scores = args.get('recent_scores', [])
    current_method = args.get('current_method', 'paley')
    
    if len(recent_scores) < 3:
        return {
            "plateau_detected": False,
            "note": "Need 3+ recent scores to detect plateau",
            "recommended_next_method": current_method
        }
    
    improvements = []
    for i in range(1, len(recent_scores)):
        prev = recent_scores[i-1]
        curr = recent_scores[i]
        if prev > 0:
            imp = (curr - prev) / prev
            improvements.append(imp)
    
    avg_improvement = sum(improvements) / len(improvements) if improvements else 0
    plateau_threshold = -0.01
    plateau_detected = avg_improvement < plateau_threshold and len(improvements) >= 3
    
    if plateau_detected:
        if current_method == 'paley':
            recommended = 'random_start'
        else:
            recommended = 'paley'
        return {
            "plateau_detected": True,
            "avg_improvement": avg_improvement,
            "recommended_next_method": recommended,
            "suggested_changes": [
                f"Switch from {current_method} to {recommended}",
                "Try alternative cooling schedule",
                "Increase iterations to 30,000",
                "Try perturbation refinement on current best"
            ]
        }
    else:
        return {
            "plateau_detected": False,
            "avg_improvement": avg_improvement,
            "recommended_next_method": current_method,
            "suggested_changes": [
                "Continue current method",
                "Refine cooling schedule parameters"
            ]
        }
