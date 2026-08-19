def run(ctx, args):
    import random
    # Generate architectural parameters for a NEW step function
    params = {
        'num_intervals': args.get('num_intervals', 600),
        'symmetry': args.get('symmetry', 'asymmetric'),
        'num_levels': args.get('num_levels', 4),
        'target_peak_height': args.get('target_peak_height', 2.2)
    }
    
    # Generate new architecture
    num_int = params['num_intervals']
    n_levels = params['num_levels']
    
    # Generate interval boundaries based on symmetry
    if params['symmetry'] == 'even':
        # Symmetric around center
        boundaries = [0.0]
        for i in range(1, n_levels // 2 + 1):
            w = 0.2 * i / (n_levels // 2)
            boundaries.extend([0.5 - w, 0.5 + w])
        boundaries.append(1.0)
        boundaries = sorted(set(boundaries))
    elif params['symmetry'] == 'odd':
        # Odd symmetry (antisymmetric peaks)
        boundaries = [0.0, 0.25, 0.75, 1.0]
    elif params['symmetry'] == 'asymmetric':
        # Random asymmetric partition
        import random
        r = sorted([random.random() for _ in range(n_levels + 1)])
        boundaries = [0.0] + r + [1.0]
    else:
        # Uniform partition
        boundaries = [i / n_levels for i in range(n_levels + 1)]
    
    # Generate height levels (non-negative, varying)
    heights = []
    base_height = 0.6
    peak_height = params['target_peak_height']
    
    # Assign heights with variation
    for i in range(n_levels):
        if i == n_levels // 2:  # Middle level is peak
            heights.append(peak_height)
        else:
            # Random base with small noise
            heights.append(base_height + random.uniform(-0.2, 0.3))
    
    # Generate the step function code structure
    return {
        'architecture': 'step_function',
        'num_intervals': num_int,
        'boundaries': boundaries,
        'heights': heights,
        'symmetry': params['symmetry'],
        'levels': n_levels,
        'note': f'Generated new architecture with {n_levels} levels, {params["symmetry"]} symmetry'
    }
