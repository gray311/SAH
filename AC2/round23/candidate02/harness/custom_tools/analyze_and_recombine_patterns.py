def run(ctx, args):
    import re
    best_f = ctx.get_best_program()
    lines = best_f.split('\n')
    
    params = {
        'num_intervals': 600,
        'peaks': [],
        'pattern_type': 'unknown',
        'symmetry': 'unknown',
        'smoothness_score': 0.0
    }
    
    # Parse the seed pattern templates to understand structure
    pattern_indices = []
    
    for i, line in enumerate(lines):
        # Detect pattern template selection
        if 'pattern_idx' in line or 'pattern_idx =' in line:
            if 'pattern_idx' in line:
                match = re.search(r'pattern_idx\s*=\s*(\d+)', line)
                if match:
                    idx = int(match.group(1))
                    pattern_indices.append(idx)
        
        # Detect interval definitions
        if 'start = ' in line or 'end = ' in line:
            pass
        elif 'height' in line.lower():
            match = re.search(r'height\s*=\s*([\d.]+)', line, re.IGNORECASE)
            if match:
                height = float(match.group(1))
                params['heights'].append(height)
    
    # Reconstruct from known seed patterns (patterns 0-11)
    n = params['num_intervals']
    
    # Count peaks from structure
    num_peaks = len(pattern_indices) if pattern_indices else 1
    
    # Estimate symmetry
    if pattern_indices:
        params['symmetry'] = 'symmetric' if 0 in pattern_indices or 11 in pattern_indices else 'asymmetric'
    
    # Generate recombinations
    params['recombinations'] = []
    
    # Recombination 1: Merge peaks
    if num_peaks > 1:
        params['recombinations'].append({
            'type': 'merge',
            'description': 'Merge two adjacent peaks into wider peak',
            'expected_c2_change': '+0.001 to +0.003'
        })
    
    # Recombination 2: Swap heights
    params['recombinations'].append({
        'type': 'height_swap',
        'description': 'Swap heights between patterns (e.g., copy middle peak to outer peaks)',
        'expected_c2_change': 'variable'
    })
    
    # Recombination 3: Asymmetric variant
    params['recombinations'].append({
        'type': 'asymmetric',
        'description': 'Create asymmetric variant (shift one side higher)',
        'expected_c2_change': 'variable'
    })
    
    # Recombination 4: 3-peak configuration
    params['recombinations'].append({
        'type': 'split_peak',
        'description': 'Split wide peak into 3 peaks for multi-scale coverage',
        'expected_c2_change': '+0.002 to +0.005'
    })
    
    # Recombination 5: Hybrid
    params['recombinations'].append({
        'type': 'hybrid',
        'description': 'Combine features from patterns 0, 3, and 11',
        'expected_c2_change': 'variable'
    })
    
    # Spectral smoothness estimate
    params['smoothness_score'] = 0.5 + 0.5 * (1.0 - num_peaks / 5.0)
    params['num_peaks'] = num_peaks
    params['recommended_recombination'] = params['recombinations'][0]['type'] if params['recombinations'] else 'none'
    
    return params
