def run(ctx, args):
    import random
    random.seed(42)
    
    best_pattern_idx = args.get('best_pattern', 0)
    base_height = args.get('base_height', 1.5)
    
    proposals = []
    
    # Variant 1: Widen support
    proposals.append({
        'variant': 'wider_support',
        'description': f'Widen {best_pattern_idx} support by +3%',
        'edit': 'shift boundaries outward by 3%',
        'rationale': 'Wider support increases L2 more than sup'
    })
    
    # Variant 2: Height increase
    proposals.append({
        'variant': 'height_increase',
        'description': f'Increase height by +0.1',
        'edit': f'change height from {base_height} to {base_height+0.1}',
        'rationale': 'Higher peak may improve ratio if L2 scales better'
    })
    
    # Variant 3: Asymmetric mirror
    proposals.append({
        'variant': 'asymmetric_mirror',
        'description': f'Mirror {best_pattern_idx} with slight asymmetry',
        'edit': 'adjust left/right boundaries by ±1%',
        'rationale': 'Asymmetry creates interference patterns'
    })
    
    # Variant 4: Add edge plateau
    proposals.append({
        'variant': 'add_edge_plateau',
        'description': f'Add small edge plateau to {best_pattern_idx}',
        'edit': 'add [int(0.02*n):int(0.05*n)].set(0.3)',
        'rationale': 'Edge plateaus smooth convolution tails'
    })
    
    # Variant 5: Combine with pattern 0
    proposals.append({
        'variant': 'hybrid_pattern',
        'description': f'Combine {best_pattern_idx} with pattern 0',
        'edit': 'take left 40% of pattern 0, right 60% of best_pattern',
        'rationale': 'Hybrid may balance different properties'
    })
    
    # Variant 6: Height decrease
    proposals.append({
        'variant': 'height_decrease',
        'description': f'Decrease height by -0.1',
        'edit': f'change height from {base_height} to {base_height-0.1}',
        'rationale': 'Lower peak may reduce sup more than L2'
    })
    
    # Variant 7: Narrow support
    proposals.append({
        'variant': 'narrower_support',
        'description': f'Narrow {best_pattern_idx} support by -3%',
        'edit': 'shift boundaries inward by 3%',
        'rationale': 'Narrower support may concentrate L2'
    })
    
    # Variant 8: Multi-height variant
    proposals.append({
        'variant': 'multi_height',
        'description': f'Create two-height variant of {best_pattern_idx}',
        'edit': 'split main plateau into high/low regions',
        'rationale': 'Multi-height may create better convolution structure'
    })
    
    return {
        'variants': proposals,
        'note': 'These are targeted edits of pattern {}'.format(best_pattern_idx),
        'usage': 'Use probe_solution on all variants before full evaluation'
    }
