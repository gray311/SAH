def run(ctx, args):
    import math
    import random
    
    code = ctx.get_program()
    
    # Extract current parameters from seed structure
    current_params = {
        'num_intervals': 400,
        'learning_rate': 0.22,
        'num_steps': 37000,
        'warmup_steps': 3700,
        'reinit_fraction': 0.18,
        'reinit_std': 0.028,
        'reinit_interval': 180,
    }
    
    # Get base heights from pattern initialization (approximate from seed)
    if args.get('base_heights') is None:
        base_heights = [1.0, 1.5, 2.0]  # Default multi-level heights
    else:
        base_heights = args['base_heights']
    
    num_levels = args.get('num_levels', 3)
    exploration_depth = args.get('exploration_depth', 3)
    
    variations = []
    
    # Generate systematic variations
    for i in range(exploration_depth + 1):
        variation = {
            'description': f'Variation {i}',
            'param_changes': {},
            'height_mods': list(base_heights),
            'strategy': f'Systematic level {i}'
        }
        
        # Vary key parameters systematically
        if i == 0:
            # Baseline - small tweaks
            variation['param_changes']['num_intervals'] = min(600, max(300, current_params['num_intervals'] + random.randint(-50, 50)))
            variation['param_changes']['learning_rate'] = round(current_params['learning_rate'] + random.uniform(-0.05, 0.05), 2)
        elif i == 1:
            # Wider intervals, slower learning
            variation['param_changes']['num_intervals'] = min(500, max(350, current_params['num_intervals'] - 50))
            variation['param_changes']['learning_rate'] = round(current_params['learning_rate'] - 0.05, 2)
        elif i == 2:
            # Narrower, faster learning
            variation['param_changes']['num_intervals'] = min(600, max(400, current_params['num_intervals'] + 50))
            variation['param_changes']['learning_rate'] = round(current_params['learning_rate'] + 0.05, 2)
        elif i == 3:
            # Different reinit strategy
            variation['param_changes']['reinit_fraction'] = round(current_params['reinit_fraction'] + 0.05, 2)
            variation['param_changes']['reinit_std'] = round(current_params['reinit_std'] + 0.01, 3)
        elif i == 4:
            # Asymmetric pattern
            variation['strategy'] = 'Asymmetric multi-level'
            variation['height_mods'] = [0.8, 1.5, 2.2, 1.2, 0.7]
        elif i == 5:
            # Higher peaks
            variation['strategy'] = 'Higher peak exploration'
            variation['height_mods'] = [1.2, 2.0, 2.8]
        elif i == 6:
            # Lower, wider
            variation['strategy'] = 'Lower wider pattern'
            variation['height_mods'] = [0.6, 1.0, 1.4]
        elif i == 7:
            # Very aggressive reinit
            variation['param_changes']['reinit_fraction'] = round(current_params['reinit_fraction'] + 0.1, 2)
            variation['param_changes']['reinit_std'] = round(current_params['reinit_std'] * 2, 3)
        
        variations.append(variation)
    
    # Add some height-focused variations
    for mod_factor in [0.9, 1.1, 1.25, 1.5]:
        h_mods = [h * mod_factor for h in base_heights]
        variations.append({
            'description': f'Height scaled by {mod_factor:.2f}',
            'height_mods': h_mods,
            'strategy': 'Height scaling'
        })
    
    return {
        'variations': variations,
        'recommendation': 'Start with variation 0 (baseline tweaks), probe 5 variants, evaluate best',
        'next_steps': ['Call edit_solution with chosen variation', 'Call probe_solution on 3-5 variants', 'Call evaluate_solution on best probe']
    }
