def run(ctx, args):
    centers = ctx.get_program()
    # Simple heuristic: check center distribution and suggest pattern type
    lines = centers.split('\n')
    pattern_hints = []
    overlap_notes = []
    # Look for hexagonal clues (angle references)
    if 'hexagonal' in centers.lower() or 'triangular' in centers.lower():
        pattern_hints.append("Consider hexagonal lattice with spacing ~0.557")
    if 'ring' in centers.lower() or 'shell' in centers.lower():
        pattern_hints.append("Adjust ring spacing; try 0.4, 0.6, 0.8, 1.0 for 16-circle outer ring")
    if 'spiral' in centers.lower():
        pattern_hints.append("Increase spiral density; use tighter parameter b")
    # Check for symmetry (multiples of 8, 16)
    if len(centers.split()) in [26, 8, 16, 9, 25]:
        overlap_notes.append("Edge effects often break perfect symmetry")
    # General recommendation
    if not pattern_hints:
        pattern_hints.append("Try hexagonal lattice or layered shells with asymmetric offsets")
    return {"hints": pattern_hints, "notes": overlap_notes}
