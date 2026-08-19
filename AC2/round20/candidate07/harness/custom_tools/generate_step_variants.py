def run(ctx, args):
    import random
    random.seed(42)
    variants = []
    
    # Get current best to understand structure
    program = ctx.get_best_program()
    
    # Variant 1: Shift boundaries up by 2%
    variants.append({
        "name": "boundary_shift_up",
        "description": "Shift all step boundaries up by 2% of their position",
        "modification": "boundaries_shifted_up_2pct",
        "rationale": "Test if wider/fatter steps improve C2"
    })
    
    # Variant 2: Shift boundaries down by 2%
    variants.append({
        "name": "boundary_shift_down",
        "description": "Shift all step boundaries down by 2% of their position",
        "modification": "boundaries_shifted_down_2pct",
        "rationale": "Test if narrower/tighter steps improve C2"
    })
    
    # Variant 3: Height perturbation
    variants.append({
        "name": "height_perturb",
        "description": "Increase heights by +0.1, decrease by -0.1 alternately",
        "modification": "alt_heights_perturbed",
        "rationale": "Test if different height ratios improve C2"
    })
    
    # Variant 4: Asymmetric variation
    variants.append({
        "name": "asymmetric_variant",
        "description": "Create asymmetric version with reversed structure",
        "modification": "asymmetric_reversed",
        "rationale": "Test if asymmetry helps C2"
    })
    
    # Variant 5: More intervals (if feasible)
    variants.append({
        "name": "more_intervals",
        "description": "Increase intervals by 10% for finer resolution",
        "modification": "intervals_increased_10pct",
        "rationale": "Test if finer resolution captures optimal shape"
    })
    
    return {"variants": variants, "note": "Use probe_solution to rank before full eval"}
