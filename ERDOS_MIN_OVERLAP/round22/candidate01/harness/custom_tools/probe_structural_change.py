def run(ctx, args):
    import re
    program = ctx.get_program()
    
    # Check if edit was made (basic validation)
    edit_desc = args.get("edit_desc", "")
    if not edit_desc:
        return {"valid": False, "note": "No edit description provided"}
    
    # Validate program structure is intact
    if program.find("# EVOLVE-BLOCK-START") == -1:
        return {"valid": False, "note": "Missing EVOLVE-BLOCK-START marker"}
    if program.find("EVOLVE-BLOCK-END") == -1:
        return {"valid": False, "note": "Missing EVOLVE-BLOCK-END marker"}
    
    # Extract current c5_bound if available
    current_c5 = args.get("current_c5", float('inf'))
    
    # For structural changes, we need at least one pattern variation in the code
    # to have the threshold/marks/peaks pattern
    if "jnp.where" not in program and "jnp.array" not in program:
        return {"valid": False, "note": "Pattern code not found in EVOLVE-BLOCK"}
    
    # Compute approximate c5 from best program available
    best_program = ctx.get_best_program() if ctx.has_best() else None
    if best_program:
        # Check if it's different from current program
        if best_program != program:
            # This is a new program, we need to evaluate it
            # But for probe, we return approximate metrics
            return {
                "valid": True,
                "approximate_c5": current_c5 * 1.05,  # Conservative estimate
                "integral_check": "pending",
                "note": "Structural edit detected. Will need full evaluation."
            }
    
    return {
        "valid": False,
        "note": "No improvement detected. Full evaluation required."
    }
