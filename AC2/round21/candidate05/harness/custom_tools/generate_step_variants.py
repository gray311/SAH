def run(ctx, args):
    import random
    best_f = ctx.get_best_program()
    lines = best_f.split('\n')
    
    variants = []
    base_patterns = [0, 3, 4, 9, 10]  # diverse seed patterns
    
    # Vary interval counts
    for num_intervals in [200, 400, 800, 1200]:
        for pattern_idx in base_patterns:
            # Create variant with modified pattern
            mod_pattern = pattern_idx
            if random.random() < 0.3:
                mod_pattern = (pattern_idx + 1) % 12
            
            # Optionally invert or shift
            if random.random() < 0.2:
                mod_pattern = 11 - pattern_idx
            
            variant_key = (num_intervals, mod_pattern)
            if variant_key not in variants:
                variants.append(variant_key)
    
    # If still need more, add multi-peak constructions
    if len(variants) < 4:
        variants.append((1200, 11))  # multi-peak pattern
        variants.append((800, 6))   # four-level pattern
        if len(variants) < 4:
            variants.append((400, 2))  # narrow high peak
    
    # Return variant descriptions for editing
    return {
        "num_variants": min(len(variants), 6),
        "variants": [
            f"Pattern {v[1]} with {v[0]} intervals" if v[1] < 11 
            else f"Multi-peak pattern with {v[0]} intervals" 
            for v in variants
        ],
        "instruction": "Replace num_intervals and pattern selection in _create_step_initializer"
    }
