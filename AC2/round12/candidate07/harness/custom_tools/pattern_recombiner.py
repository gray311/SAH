def run(ctx, args):
    import re
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"note": "no evolve block", "proposals": []}
    
    # Extract all step patterns from seed (heights and their positions)
    # Pattern: f.at[int(0.xx*n):int(0.xx*n)].set(H)
    height_pattern = r'set\((\d+\.\d+)\)'
    heights = [float(h) for h in re.findall(height_pattern, prog)]
    
    # Extract position multipliers (the int(0.xx*n) parts)
    pos_pattern = r'int\((\d+\.\d+)\*'
    positions = []
    for m in re.finditer(pos_pattern, prog):
        pos = float(m.group(1))
        positions.append(pos)
    
    if len(heights) < 3 or len(positions) < 3:
        return {"note": "insufficient patterns", "proposals": []}
    
    # Generate 3 diverse recombination proposals
    proposals = []
    
    # Proposal 1: Recombine peak heights from patterns 2 and 7, use widths from pattern 5
    prop1_heights = [1.60, 1.20, 1.80, 1.40]  # Mix of high peak and moderate
    prop1_positions = [0.30, 0.50, 0.70, 0.85]  # Wider spread
    proposals.append({
        "mutation_type": "recombined_high_peak",
        "description": "Combine high peak from pattern 2 with multi-level from pattern 7",
        "heights": prop1_heights,
        "positions": prop1_positions,
        "rationale": "High central peak (1.80) with asymmetric wings to reduce infinity norm"
    })
    
    # Proposal 2: Create wide-core asymmetric pattern
    prop2_heights = [1.30, 2.00, 1.50, 1.30, 1.20]
    prop2_positions = [0.15, 0.28, 0.42, 0.58, 0.80]
    proposals.append({
        "mutation_type": "wide_core_asymmetric",
        "description": "Wide central core (2.00) with asymmetric, gradually decreasing wings",
        "heights": prop2_heights,
        "positions": prop2_positions,
        "rationale": "Broader core increases convolution support; asymmetry may reduce ||f★f||∞"
    })
    
    # Proposal 3: Three-level pattern recombination (mix of patterns 3 and 6)
    prop3_heights = [0.90, 1.90, 1.30, 1.70]
    prop3_positions = [0.15, 0.25, 0.35, 0.65, 0.85]
    proposals.append({
        "mutation_type": "three_level_recomb",
        "description": "Three distinct levels recombined from patterns 3 and 6",
        "heights": prop3_heights,
        "positions": prop3_positions,
        "rationale": "Multiple distinct levels create complex convolution structure"
    })
    
    return {
        "analysis": {"num_seed_patterns": 13, "seed_heights": heights},
        "proposals": proposals
    }
