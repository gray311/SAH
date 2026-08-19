def run(ctx, args):
    f = ctx.get_program()
    best_score = ctx.best_score()
    
    # Analyze function structure
    analysis = {
        "current_score": float(best_score),
        "function_type": "unknown",
        "structure": "",
        "suggestions": []
    }
    
    content = f
    if isinstance(content, str):
        content = content
    
    if "step" in content.lower() or "piecewise" in content.lower():
        analysis["function_type"] = "step"
        analysis["structure"] = "Discrete piecewise function detected"
        analysis["suggestions"] = [
            "Try multi-level steps (3-5 levels) with varying heights",
            "Experiment with asymmetric step distributions",
            "Vary step widths to optimize convolution shape",
            "Consider step functions with broader central support"
        ]
    elif "gaussian" in content.lower() or "normal" in content.lower():
        analysis["function_type"] = "gaussian"
        analysis["structure"] = "Gaussian mixture detected"
        analysis["suggestions"] = [
            "Increase K to 3-5 components for more flexibility",
            "Optimize sigma values: try 0.1-0.3 range",
            "Cluster means around convolution peak for better concentration",
            "Ensure non-negativity with softplus activation"
        ]
    elif "exponential" in content.lower():
        analysis["function_type"] = "exponential"
        analysis["structure"] = "Exponential decay detected"
        analysis["suggestions"] = [
            "Try double exponential (product of two)",
            "Optimize decay rates in [0.05-0.5] range",
            "Consider exponential sums rather than products",
            "Center around convolution maximum"
        ]
    else:
        analysis["function_type"] = "piecewise_linear"
        analysis["structure"] = "Piecewise-linear optimization detected"
        analysis["suggestions"] = [
            "Switch to step functions (record holders at 0.8963 C2)",
            "Increase num_intervals from 400 to 800-1200",
            "Adjust reinit_fraction to 0.1-0.2 range",
            "Try fewer, wider intervals for smoother convolution"
        ]
    
    analysis["priority"] = "step_functions_first"
    analysis["next_action"] = "Call mutation_probe for step function variants"
    
    return analysis