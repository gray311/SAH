def run(ctx, args):
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"note": "no evolve block", "heights": []}
    import re
    # Extract .set(height) patterns
    heights = re.findall(r'\.set\((\d+\.?\d*)\)', prog)
    heights = [float(h) for h in heights]

    # Extract interval markers for positions
    positions = re.findall(r'int\((\d+\.?\d*)\*n\)', prog)
    positions = [float(p) for p in positions]

    # Identify pattern class
    num_heights = len(heights)
    pattern_type = "multi-level" if num_heights > 3 else "single-level" if num_heights == 1 else "multi-level"

    # Suggest divergent patterns
    suggestions = []
    suggestions.append(f"Pattern type: {pattern_type}, {num_heights} steps")
    suggestions.append(f"Current heights: {[round(h, 2) for h in heights[:5]]}")
    suggestions.append(f"Position fractions: {[round(p, 2) for p in positions[:5]]}")

    # Generate specific pattern suggestions
    suggestions.append("Try ultra-narrow peak: f.at[int(0.35*n):int(0.65*n)].set(2.5)")
    suggestions.append("Try triple plateau: heights 1.2, 1.8, 1.2 at 0.1-0.3, 0.3-0.7, 0.7-0.9")
    suggestions.append("Try asymmetric twin: peak1 at 0.18-0.35 (height 2.0), peak2 at 0.65-0.82 (height 1.5)")
    suggestions.append("Try wide plateau: f.at[int(0.20*n):int(0.80*n)].set(1.5)")

    return {
        "heights": heights,
        "positions": positions,
        "pattern_type": pattern_type,
        "suggestions": "\n".join(suggestions[:6])
    }
