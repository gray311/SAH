def run(ctx, args):
    import re
    code = ctx.get_program()
    
    # Extract pattern initialization parameters
    heights = []
    widths = []
    positions = []
    
    # Find height assignments
    height_pattern = r'base_height\s*=\s*([\d.]+)|bump[12]\s*height\s*=\s*([\d.]+)'
    height_match = re.search(height_pattern, code)
    if height_match:
        heights = [float(g) for g in height_match.groups() if g]
    
    # Find width/interval parameters
    width_pattern = r'(left_width|right_width)\s*=\s*int\(([\d.]+)\s*\*\s*n\)'
    width_match = re.findall(width_pattern, code)
    widths = [float(g[1]) for g in width_match if g[1]]
    
    # Find position parameters
    pos_pattern = r'int\(([\d.]+)\s*\*\s*n\)'
    positions = [float(g) for g in re.findall(pos_pattern, code) if not g.startswith('0.')]
    
    # Analyze symmetry
    is_symmetric = abs(widths[0] - widths[-1]) < 0.05 if len(widths) >= 2 else True
    symmetric_heights = all(abs(heights[i] - heights[-1-i]) < 0.01 for i in range(len(heights)//2)) if len(heights) >= 2 else True
    
    # Generate mutation proposals
    mutations = []
    if is_symmetric:
        mutations.append({
            "type": "asymmetric_heights",
            "proposal": f"Change heights from symmetric to asymmetric: try [h-0.08, h+0.05, h-0.03]",
            "rationale": "Breaking symmetry can reduce ||f★f||_∞"
        })
    if len(widths) >= 1 and abs(widths[0] - widths[1]) < 0.02 if len(widths) >= 2 else False:
        mutations.append({
            "type": "non_uniform_spacing",
            "proposal": f"Make spacing non-uniform: try [{w-0.02, w+0.03, w-0.01}]",
            "rationale": "Clustering features can improve L2/∞ ratio"
        })
    
    # Add multi-scale proposal
    mutations.append({
        "type": "multi_scale_features",
        "proposal": "Add nested bump on top of largest existing bump",
        "rationale": "Captures finer convolution structure"
    })
    
    # Add tapering proposal
    mutations.append({
        "type": "boundary_tapering",
        "proposal": "Add linear ramp from base_height to 0 over last 5% of domain",
        "rationale": "Reduces edge artifacts in convolution"
    })
    
    return {
        "pattern_analysis": {
            "num_heights": len(heights),
            "num_widths": len(widths),
            "is_symmetric": is_symmetric,
            "heights": heights,
            "widths": widths,
            "positions": positions
        },
        "mutation_proposals": mutations,
        "note": "Use these proposals to generate concrete mutations via edit_solution, then rank with probe_solution"
    }
