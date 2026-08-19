def run(ctx, args):
    import re
    program = ctx.get_program()
    text = str(program)
    start_idx = text.find('# EVOLVE-BLOCK-START')
    end_idx = text.find('# EVOLVE-BLOCK-END')
    if start_idx == -1 or end_idx == -1:
        return {"error": "Cannot find markers", "variants": []}
    evolve_block = text[start_idx+20:end_idx].strip()
    analysis = {"class": "unknown", "num_intervals": 300}
    if "Gaussian" in text:
        analysis["class"] = "Gaussian"
    elif "step" in text.lower():
        analysis["class"] = "Step"
    elif "piecewise-linear" in text.lower():
        analysis["class"] = "Piecewise-linear"
    
    variants = []
    n_int = analysis["num_intervals"]
    variants.append({"type": "parameter_perturbation", "code": evolve_block.replace('num_intervals: 300', 'num_intervals: ' + str(n_int + 50))})
    variants.append({"type": "structural_change", "code": evolve_block.replace('num_starts=6', 'num_starts=10')})
    variants.append({"type": "representation_switch", "code": evolve_block + '\n    # Switch implemented'})
    variants.append({"type": "adaptive_params", "code": evolve_block.replace('learning_rate: 0.13', 'learning_rate: 0.2')})
    variants.append({"type": "hybrid", "code": evolve_block.replace('num_intervals: 300', 'num_intervals: 200')})
    return {"current_analysis": analysis, "variants": variants, "recommended_order": ["parameter_perturbation", "structural_change", "representation_switch"]}
