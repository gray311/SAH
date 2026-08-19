def run(ctx, args):
    import re
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"note": "no evolve block", "proposals": []}
    
    # Extract height values
    height_matches = re.findall(r'\.set\((\d+\.\d+)\)', prog)
    height_matches += re.findall(r'set\((\d+\.\d+)\)', prog)
    heights = [float(h) for h in height_matches if h]
    
    if not heights:
        return {"note": "could not parse heights", "proposals": []}
    
    # Categorize current pattern
    num_levels = len(heights)
    avg_h = sum(heights) / len(heights)
    max_h = max(heights)
    min_h = min(heights)
    
    proposals = []
    
    # Proposal 1: Height scaling (multiply all by factor)
    scale_factor = 1.12 if num_levels < 6 else 1.08
    proposals.append({
        "mutation_type": "height_scaling",
        "description": f"Scale all heights by {scale_factor:.2f}x",
        "changes": {
            "operation": "multiply_all_heights",
            "factor": scale_factor,
            "affected_levels": "all"
        },
        "rationale": "Scaling all heights proportionally can improve the L2/∞ ratio by changing the relative weighting"
    })
    
    # Proposal 2: Width scaling on core interval
    core_indices = [1, 2] if num_levels >= 3 else [0, 1]
    expansion = 0.22
    proposals.append({
        "mutation_type": "width_scaling",
        "description": f"Expand core interval(s) by {expansion*100:.0f}%",
        "changes": {
            "operation": "expand_intervals",
            "expansion_fraction": expansion,
            "target": "core_intervals"
        },
        "rationale": "Wider intervals increase convolution overlap, boosting L2 norm"
    })
    
    # Proposal 3: Level count change (add/remove a level)
    if num_levels <= 7:
        level_change = 1
        proposals.append({
            "mutation_type": "level_addition",
            "description": f"Add {level_change} level(s) to create {num_levels + level_change}-level pattern",
            "changes": {
                "operation": "add_level",
                "new_level_count": num_levels + level_change,
                "strategy": "split_middle_interval"
            },
            "rationale": "More levels allow finer control over the convolution shape"
        })
    else:
        proposals.append({
            "mutation_type": "level_reduction",
            "description": f"Reduce to {num_levels - 1} level(s) by merging adjacent levels",
            "changes": {
                "operation": "merge_adjacent_levels",
                "new_level_count": num_levels - 1,
                "strategy": "merge_middle"
            },
            "rationale": "Fewer levels with higher amplitudes may improve the ratio"
        })
    
    # Proposal 4: Symmetry breaking type 2 (different from just making asymmetric)
    # Shift heights in a non-uniform way
    proposals.append({
        "mutation_type": "symmetry_breaking_gradient",
        "description": "Create gradient-like height asymmetry: left side higher, right side lower",
        "changes": {
            "operation": "gradient_asymmetry",
            "strategy": "left_high_right_low",
            "scale": 0.12
        },
        "rationale": "Gradient asymmetry breaks perfect symmetry differently than random asymmetry"
    })
    
    # Proposal 5: Multi-peaked variant (if not already multi-peaked)
    if num_levels <= 3:
        proposals.append({
            "mutation_type": "multi_peaked_creation",
            "description": "Convert to 4-level multi-peaked pattern with two distinct peaks",
            "changes": {
                "operation": "create_two_peaks",
                "new_level_count": 4,
                "strategy": "add_wings"
            },
            "rationale": "Two distinct peaks can create a different convolution profile"
        })
    else:
        proposals.append({
            "mutation_type": "narrow_peak_creation",
            "description": "Add a very narrow, high peak in the center",
            "changes": {
                "operation": "add_narrow_peak",
                "peak_height": max_h * 1.15,
                "peak_width_fraction": 0.05
            },
            "rationale": "A narrow high peak increases ||f★f||₂² significantly without increasing ||f★f||∞ proportionally"
        })
    
    return {
        "analysis": {
            "current_levels": num_levels,
            "avg_height": avg_h,
            "height_range": max_h - min_h
        },
        "proposals": proposals
    }
