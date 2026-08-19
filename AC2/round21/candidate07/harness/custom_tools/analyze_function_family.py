def run(ctx, args):
    best_f = ctx.get_best_program()
    import re
    f_text = best_f
    family_type = 'unknown'
    num_params = 10
    continuity = 'discontinuous'
    
    # Detect step function pattern
    if 'start =' in f_text or 'end =' in f_text:
        family_type = 'steps'
        # Count intervals
        starts = len(re.findall(r'start\s*=\s*\d+', f_text))
        ends = len(re.findall(r'end\s*=\s*\d+', f_text))
        num_params = max(starts, ends) + len(re.findall(r'height\s*=\s*[\d.]+', f_text))
        continuity = 'discontinuous'
    # Detect spline/basis pattern
    elif 'basis' in f_text.lower() or 'knot' in f_text.lower() or 'coeff' in f_text.lower():
        family_type = 'splines'
        num_params = len(re.findall(r'\d+\.?\d*', f_text)) // 3
        continuity = 'C2'
    # Detect polynomial pattern
    elif 'polynomial' in f_text.lower() or 'segment' in f_text.lower():
        family_type = 'polynomials'
        segments = len(re.findall(r'segment\s*[\d]', f_text))
        num_params = segments * 2
        continuity = 'C1'
    # Detect exponential pattern
    elif 'exp(' in f_text or 'exponential' in f_text.lower() or 'decay' in f_text.lower():
        family_type = 'exponential'
        num_params = len(re.findall(r'(?:k|decay|rate)\s*=\s*[\d.]+', f_text))
        continuity = 'continuous'
    # Detect mixture pattern
    elif 'gaussian' in f_text.lower() or 'mixture' in f_text.lower() or 'sum.*exp' in f_text.lower():
        family_type = 'mixture'
        components = len(re.findall(r'exp\s*\(-\s*\d*\.?\d*\s*\*', f_text))
        num_params = components * 3
        continuity = 'smooth'
    
    # Default fallback
    if family_type == 'unknown':
        family_type = 'default_steps'
        num_params = 60
        continuity = 'discontinuous'
    
    return {
        'family_type': family_type,
        'num_parameters': num_params,
        'continuity': continuity,
        'note': f'Current best is {family_type} with {num_params} parameters'
    }