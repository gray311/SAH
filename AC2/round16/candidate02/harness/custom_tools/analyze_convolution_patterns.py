def run(ctx, args):
    best_f = ctx.get_best_program()
    if best_f is None:
        return {"note": "No best program found, analyzing seed"}
    # Parse program to extract function parameters
    import re
    # Look for key parameters in the EVOLVE-BLOCK
    height_matches = re.findall(r'heights?\s*=\s*jnp\.array\(\[([^\]]+)\]\)', best_f)
    level_matches = re.findall(r'levels?\s*=\s*jnp\.array\(\[([^\]]+)\]\)', best_f)
    width_matches = re.findall(r'(?:left|right|interval|width|start|end)\s*=\s*int\(([^.]+)\s*\*\s*n\)', best_f)
    
    # Extract numeric values
    params = {}
    if height_matches:
        params['heights'] = [float(x) for x in re.findall(r'([\d.]+)', height_matches[0])]
    if level_matches:
        params['levels'] = [float(x) for x in re.findall(r'([\d.]+)', level_matches[0])]
    if width_matches:
        params['widths'] = [float(x) for x in width_matches]
    
    # Compute structural metrics
    structure = {}
    if 'heights' in params and len(params['heights']) >= 2:
        left_h, right_h = params['heights'][:2]
        structure['edge_symmetry'] = abs(left_h - right_h) / max(left_h, right_h) if max(left_h, right_h) > 0 else 0.0
        structure['height_diff'] = left_h - right_h
    
    if 'levels' in params:
        levels = params['levels']
        if len(levels) >= 1:
            structure['height_variance'] = float((sum((h - sum(levels)/len(levels))**2 for h in levels) / len(levels)) ** 0.5)
    
    structure['recommended_mutations'] = []
    if structure.get('edge_symmetry', 0) < 0.1:
        structure['recommended_mutations'].append('asymmetric_heights')
    if len(params.get('levels', [])) < 3:
        structure['recommended_mutations'].append('multi_level')
    if structure.get('height_variance', 0) < 0.1:
        structure['recommended_mutations'].append('localized_bumps')
    
    return {
        "best_program_sample": best_f[:500],
        "structure": structure,
        "note": "Use recommended_mutations to guide your next edits. Focus on step-function patterns."
    }
