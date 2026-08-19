def run(ctx, args):
    import re
    
    mutation_type = args.get('mutation_type', '')
    proposed_change = args.get('proposed_change', '')
    
    prog = ctx.get_program()
    
    # Check if we have an EVOLVE-BLOCK
    if '# EVOLVE-BLOCK' not in prog:
        return {"error": "No EVOLVE-BLOCK found in program", "verified_code": None}
    
    # Parse current heights from the program
    height_matches = re.findall(r'f\.at\([^)]+\)\.set\((\d+\.\d+)\)', prog)
    height_matches += re.findall(r'set\((\d+\.\d+)\)', prog)
    current_heights = [float(h) for h in height_matches if h and re.match(r'^\d+\.\d+$', h)]
    
    if not current_heights:
        return {"error": "Could not parse current pattern heights", "verified_code": None}
    
    # Validate mutation type
    valid_types = ['height_perturbation', 'width_expansion', 'center_shift', 'asymmetric_variation', 
                  'intermediate_adjustment']
    if mutation_type not in valid_types:
        return {"error": f"Invalid mutation type: {mutation_type}. Use one of: {valid_types}", 
                "verified_code": None}
    
    # Check if proposed change is meaningful (>5% of parameter range)
    num_heights = len(current_heights)
    height_range = max(current_heights) - min(current_heights)
    min_meaningful_change = 0.01 * height_range if height_range > 0 else 0.01
    
    try:
        proposed_change_float = float(proposed_change) if '.' in proposed_change else float(proposed_change) / 100.0
    except ValueError:
        return {"error": f"Cannot parse proposed_change: {proposed_change}", "verified_code": None}
    
    if abs(proposed_change_float) < min_meaningful_change:
        return {"error": f"Proposed change {proposed_change_float:.4f} is too small (must be >5% of height range). "
                       f"Current range: {height_range:.3f}, min meaningful: {min_meaningful_change:.3f}",
                "verified_code": None}
    
    # Generate the actual SEARCH/REPLACE code based on mutation type
    if mutation_type == 'height_perturbation':
        if current_heights:
            peak_idx = current_heights.index(max(current_heights))
            old_val = current_heights[peak_idx]
            new_val = old_val + proposed_change_float
            if new_val < 0:
                return {"error": "Proposed new height would be negative", "verified_code": None}
            
            # Find the corresponding line in the program
            search_pattern = rf'f\.at\([^)]+\)\.set\({re.escape(str(old_val))}\)'
            replacement = f'f.at[^)]+\.set({new_val:.2f})'
            
            if search_pattern in prog:
                verified_code = f"search_pattern = r'{search_pattern}'\nreplacement = f'f.at[^)]+.set({new_val:.2f})'\n\nedits = [search_replace(mutation='height_perturbation', search=search_pattern, replacement=replacement, prog=prog)]"
                return {"verified_code": verified_code}
            else:
                return {"error": f"Could not find pattern to replace: {search_pattern}", "verified_code": None}
        else:
            return {"error": "No heights found to perturb", "verified_code": None}
    
    elif mutation_type == 'width_expansion':
        width_change = proposed_change_float  # Already a percentage like 0.08
        if width_change > 0.15:
            return {"error": f"Width expansion {width_change*100:.1f}% is too large. Use 3-10%.", "verified_code": None}
        
        verified_code = f"width_expansion_fraction = {width_change:.3f}\n\nedits = [search_replace(mutation='width_expansion', factor=1 + {width_change:.3f}, prog=prog)]"
        return {"verified_code": verified_code}
    
    elif mutation_type == 'center_shift':
        shift = proposed_change_float  # e.g., 0.01 for 1%
        if shift > 0.05:
            return {"error": f"Center shift {shift*100:.1f}% is too large. Use 1-3%.", "verified_code": None}
        
        verified_code = f"shift_fraction = {shift:.3f}\n\nedits = [shift_all_boundaries(fraction={shift:.3f}, prog=prog)]"
        return {"verified_code": verified_code}
    
    elif mutation_type == 'asymmetric_variation':
        if current_heights:
            verified_code = f"asymmetry_magnitude = {abs(proposed_change_float):.3f}\n\nedits = [apply_asymmetric_variation(magnitude={abs(proposed_change_float):.3f}, prog=prog)]"
            return {"verified_code": verified_code}
        
        return {"error": "Not enough heights for asymmetric variation", "verified_code": None}
    
    elif mutation_type == 'intermediate_adjustment':
        if len(current_heights) >= 4:
            verified_code = f"adjustment_magnitude = {abs(proposed_change_float):.3f}\n\nedits = [adjust_intermediate_levels(magnitude={abs(proposed_change_float):.3f}, prog=prog)]"
            return {"verified_code": verified_code}
        else:
            return {"error": f"Need at least 4 heights for intermediate adjustment, found {len(current_heights)}", "verified_code": None}
    
    return {"error": "Unknown mutation type", "verified_code": None}
