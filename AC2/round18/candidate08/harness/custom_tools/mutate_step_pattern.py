def run(ctx, args):
    import math
    base = args.get('base_pattern', {})
    n = base.get('num_intervals', 600)
    pattern_idx = base.get('pattern_idx', 0)
    heights = base.get('heights', [1.0, 2.0, 1.0])
    positions = base.get('positions', [0.25, 0.5, 0.75])
    
    variants = []
    
    # Variant 1: Height perturbation
    if pattern_idx < len(heights):
        new_heights = list(heights)
        noise = [0.95, 1.0, 1.05]
        idx = pattern_idx % len(noise)
        new_heights[pattern_idx] = new_heights[pattern_idx] * noise[idx]
        new_positions = list(positions)
        variants.append({
            'type': 'height_mut', 'name': f'height_{noise[idx]:.2f}x',
            'heights': new_heights, 'positions': new_positions, 'pattern_idx': pattern_idx
        })
    
    # Variant 2: Position perturbation
    if len(positions) > 1:
        new_positions = list(positions)
        shift = 0.02 + 0.03 * (pattern_idx % 2)  # 0.02 or 0.03
        new_positions[pattern_idx % len(new_positions)] = min(0.85, max(0.15, new_positions[pattern_idx % len(new_positions)] + shift))
        variants.append({
            'type': 'pos_mut', 'name': f'pos_shift_{shift:.2f}',
            'heights': heights, 'positions': new_positions, 'pattern_idx': pattern_idx
        })
    
    # Variant 3: Asymmetry
    asym_heights = list(heights)
    asym_positions = list(positions)
    center = len(asym_heights) // 2
    if center > 0:
        asym_heights[center] = heights[center] * 1.08  # slightly higher center
        asym_positions[center] = positions[center] * 0.98  # slightly shifted
    variants.append({
        'type': 'asym_mut', 'name': 'asymmetry',
        'heights': asym_heights, 'positions': asym_positions, 'pattern_idx': pattern_idx + 2 if pattern_idx < 9 else pattern_idx
    })
    
    return {'variants': variants, 'note': 'Use edit_solution to implement each variant fully'}