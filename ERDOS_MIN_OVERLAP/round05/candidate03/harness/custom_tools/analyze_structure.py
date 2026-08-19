def run(ctx, args):
    # Read the current code to infer discretization
    program = ctx.get_program()
    
    # Extract num_intervals from code or use default
    num_intervals = 800  # Seed default
    domain_width = 2.0
    
    try:
        # Try to extract from code
        for line in program.split('\n'):
            if 'num_intervals' in line:
                import re
                match = re.search(r'num_intervals:\s*(\d+)', line)
                if match:
                    num_intervals = int(match.group(1))
                    break
    except:
        pass
    
    dx = domain_width / num_intervals
    
    # Return structure-aware parameters
    return {
        "num_intervals": num_intervals,
        "dx": float(dx),
        "domain_width": domain_width,
        "threshold_suggested": [i * dx for i in range(100, num_intervals, 50)],
        "pattern_diversity": "high",
        "convergence_hint": "Use multiple restarts with different structural patterns",
        "recommended_search": [
            "symmetric_threshold",
            "asymmetric_split",
            "double_pulse",
            "periodic_sin",
            "region_based"
        ]
    }
