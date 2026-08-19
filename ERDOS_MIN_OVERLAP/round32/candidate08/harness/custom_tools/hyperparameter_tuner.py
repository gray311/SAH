def run(ctx, args):
    import re
    prog = ctx.get_best_program()
    if not prog or prog == "":
        return {"suggestions": ["Run baseline first"]}
    
    patterns = [
        (r'num_intervals:\s*(\d+)', 'num_intervals'),
        (r'base_learning_rate:\s*([\d.]+)', 'base_learning_rate'),
        (r'penalty_strength:\s*([\d.]+)', 'penalty_strength'),
        (r'num_steps:\s*(\d+)', 'num_steps'),
        (r'num_restarts:\s*(\d+)', 'num_restarts'),
    ]
    
    params = {}
    for pat, name in patterns:
        m = re.search(pat, prog)
        if m:
            val = m.group(1)
            params[name] = float(val) if '.' in val else int(val)
    
    suggestions = []
    
    if "penalty_strength" in params and params["penalty_strength"] < 80:
        suggestions.append({
            "parameter": "penalty_strength",
            "current": params["penalty_strength"],
            "suggested_value": 100.0,
            "reason": "Increase for better constraint enforcement"
        })
    elif "penalty_strength" in params and params["penalty_strength"] < 120:
        suggestions.append({
            "parameter": "penalty_strength",
            "current": params["penalty_strength"],
            "suggested_value": 120.0,
            "reason": "Try penalty_strength=120"
        })
    
    if "num_intervals" in params and params["num_intervals"] < 800:
        suggestions.append({
            "parameter": "num_intervals",
            "current": params["num_intervals"],
            "suggested_value": 1000,
            "reason": "Increase resolution"
        })
    elif "num_intervals" in params and params["num_intervals"] > 1200:
        suggestions.append({
            "parameter": "num_intervals",
            "current": params["num_intervals"],
            "suggested_value": 800,
            "reason": "Reduce resolution"
        })
    
    if not suggestions:
        suggestions.append({
            "parameter": "penalty_strength",
            "current": params.get("penalty_strength", 61.0),
            "suggested_value": 100.0,
            "reason": "Systematic: try penalty_strength=100"
        })
    
    return {"current_hyperparams": params, "suggestions": suggestions}
