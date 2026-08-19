def run(ctx, args):
    import random

    current = args.get('current_params', {})
    notes = args.get('notes', '')

    mutations = []

    # Always suggest reinit boost for escape
    reinit_frac = current.get('reinit_fraction', 0.18)
    reinit_std = current.get('reinit_std', 0.028)
    reinit_interval = current.get('reinit_interval', 180)

    mutations.append({
        'name': 'aggressive_reinit',
        'description': 'Boost reinitialization to escape local optima',
        'changes': {
            'reinit_fraction': reinit_frac + 0.15 if reinit_frac < 0.30 else reinit_frac + 0.05,
            'reinit_std': min(0.08, reinit_std * 1.5),
            'reinit_interval': reinit_interval * 1.2
        },
        'reasoning': f'Current reinit_fraction={reinit_frac} may be too low for escape. '
                    f'Increasing to force larger, more frequent resets.'
    })

    # Suggest interval increase
    n_int = current.get('num_intervals', 400)
    if n_int < 600:
        mutations.append({
            'name': 'finer_discretization',
            'description': 'Increase num_intervals for finer step structures',
            'changes': {'num_intervals': n_int + 200},
            'reasoning': f'Current intervals={n_int} may limit structural complexity. '
                        f'Increasing to {n_int + 200} for more detailed steps.'
        })

    # Suggest height adjustments
    mutations.append({
        'name': 'extreme_heights',
        'description': 'Try more extreme step heights for better C2',
        'changes': {'height_range': '1.8-2.2 instead of 1.42-1.72'},
        'reasoning': 'Current step heights may be suboptimal. Test with more extreme values.'
    })

    # Suggest longer optimization
    n_steps = current.get('num_steps', 37000)
    mutations.append({
        'name': 'extended_optimization',
        'description': 'Run more optimization steps for refinement',
        'changes': {'num_steps': min(55000, n_steps + 8000)},
        'reasoning': f'Current steps={n_steps} may not allow full convergence. '
                    f'Increasing to allow more refinement.'
    })

    random.shuffle(mutations)
    return {'mutations': mutations[:5]}
