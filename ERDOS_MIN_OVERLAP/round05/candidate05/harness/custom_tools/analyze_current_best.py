def run(ctx, args):
    # Check if we have access to the program text
    try:
        prog = ctx.get_program()
        # Key analysis points for this task:
        # - Look for num_intervals (default 800 in seed)
        # - Look for optimization steps (default 59000 in seed)
        # - Look for initialization patterns (sigmoid of latent, etc.)
        # - Look for penalty strength (default 1370 in seed)
        analysis = {
            "program_length": len(prog),
            "strategy_detected": "gradient_descent_sigmoid",
            "suggestion": "Consider reducing intervals to 128-256, trying pattern-based initialization, or quantizing values. Current seed has 8000 intervals with 59000 steps - may be over-parameterized."
        }
        # Try to extract key hyperparameters
        import re
        num_intervals = re.search(r'num_intervals.*=.*(\d+)', prog)
        num_steps = re.search(r'num_steps.*=.*(\d+)', prog)
        penalty = re.search(r'penalty_strength.*=.*(\d+\.?\d*)', prog)
        if num_intervals:
            analysis["current_intervals"] = int(num_intervals.group(1))
        if num_steps:
            analysis["current_steps"] = int(num_steps.group(1))
        if penalty:
            analysis["current_penalty"] = float(penalty.group(1))
        return analysis
    except:
        return {"error": "Could not analyze program", "note": "Manual inspection recommended"}
