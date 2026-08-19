def run(ctx, args):
    code = ctx.get_program()
    search_str = "# EVOLVE-BLOCK-START"
    if search_str not in code:
        return {"error": "No EVOLVE-BLOCK found"}
    
    start = code.find(search_str)
    end = code.find("# EVOLVE-BLOCK-END", start)
    if end == -1:
        return {"error": "Missing END marker"}
    
    evolve_block = code[start+20:end]
    
    import re
    
    # Extract parameters
    m = re.search(r'num_intervals:\s*(\d+)', evolve_block)
    analysis = {
        "num_intervals": int(m.group(1)) if m else None,
        "base_learning_rate": None,
        "num_steps": None,
        "penalty_strength": None,
        "num_restarts": None,
        "suggested_changes": [],
        "analysis_note": "Extracted parameters and suggest experiments"
    }
    
    m = re.search(r'base_learning_rate:\s*([\d.]+)', evolve_block)
    if m:
        analysis["base_learning_rate"] = float(m.group(1))
    
    m = re.search(r'num_steps:\s*(\d+)', evolve_block)
    if m:
        analysis["num_steps"] = int(m.group(1))
    
    m = re.search(r'penalty_strength:\s*([\d.]+)', evolve_block)
    if m:
        analysis["penalty_strength"] = float(m.group(1))
    
    m = re.search(r'num_restarts:\s*(\d+)', evolve_block)
    if m:
        analysis["num_restarts"] = int(m.group(1))
    
    # Generate suggestions based on structure
    num_int = analysis["num_intervals"]
    penalty = analysis["penalty_strength"]
    
    if num_int is not None:
        if num_int < 200:
            analysis["suggested_changes"].append("Increase num_intervals to 300-500 for finer resolution")
        elif num_int > 1000:
            analysis["suggested_changes"].append("Reduce num_intervals to 300-500 - coarser steps may suffice")
    
    if penalty is not None:
        if penalty < 500:
            analysis["suggested_changes"].append("Increase penalty_strength to 1000-2000 for tighter constraint enforcement")
        elif penalty > 2000:
            analysis["suggested_changes"].append("Reduce penalty_strength to 500-1000 to avoid over-penalization")
    
    analysis["suggested_changes"].append("Try alternative initialization: uniform block function with 3-5 blocks")
    analysis["suggested_changes"].append("Add multi-restart with 5-10 diverse initializations")
    analysis["suggested_changes"].append("Experiment with learning_rate=0.008-0.012 instead of 0.0053")
    
    return analysis