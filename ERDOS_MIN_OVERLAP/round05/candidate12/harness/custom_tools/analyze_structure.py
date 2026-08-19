def run(ctx, args):
    program = ctx.get_best_program()
    analysis = {
        "program_extracted": False,
        "recommendations": []
    }
    
    try:
        # Extract hyperparameters from the program
        # Look for: num_intervals, base_learning_rate, num_steps, penalty_strength, num_restarts
        # Count initialization patterns in _get_best_initialization
        
        analysis["note"] = "Key parameters to check and improve:"
        analysis["checks"] = [
            "Number of initialization patterns in _get_best_initialization (current: 12)",
            "Base learning rate (current: 0.0053) - lower may help stability",
            "Penalty strength (current: 1370) - may be too restrictive",
            "Number of restarts (current: 3) - more diversity helps",
            "Num intervals (current: 800) - higher resolution may help"
        ]
        analysis["suggestions"] = [
            "Add asymmetric two-level patterns: h(x)=a for x<t, 1-a for x>t where t=2*(1-a)",
            "Increase patterns from 12 to 20-30 with structured asymmetric designs",
            "Try learning rates in range 0.001-0.003 for smoother optimization",
            "Consider reducing penalty_strength to 500-1000 for more flexibility",
            "Add patterns with transition at x=1/3 and x=2/3"
        ]
    except Exception as e:
        analysis["error"] = str(e)
    
    return analysis
