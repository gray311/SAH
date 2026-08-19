def run(ctx, args):
    # Get the current best program
    program = ctx.get_best_program()
    
    # Extract key parameters (simplified heuristic parsing)
    structure = {
        "num_intervals": 600,
        "base_heights": None,
        "boundaries": None,
        "pattern_type": "unknown"
    }
    
    # Look for pattern indicators in the code
    if "pattern_idx == 0" in program:
        structure["pattern_type"] = "single_step"
    elif "pattern_idx == 1" in program:
        structure["pattern_type"] = "higher_peak"
    elif "pattern_idx == 3" in program:
        structure["pattern_type"] = "multi_level_centered"
    
    # Extract heights from the code
    import re
    height_matches = re.findall(r'\.set\(([\d.]+)\)', program)
    structure["extracted_heights"] = [float(h) for h in height_matches]
    
    # Calculate statistics
    if structure["extracted_heights"]:
        structure["min_height"] = min(structure["extracted_heights"])
        structure["max_height"] = max(structure["extracted_heights"])
        structure["avg_height"] = sum(structure["extracted_heights"]) / len(structure["extracted_heights"])
    
    return {
        "structure": structure,
        "note": "Use this to guide boundary and height perturbations"
    }
