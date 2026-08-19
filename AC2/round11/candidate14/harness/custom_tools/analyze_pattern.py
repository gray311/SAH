def run(ctx, args):
    import re
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"note": "no evolve block", "patterns": []}
    
    # Extract all .set(height) calls with their positions
    set_calls = re.findall(r'f\.at\((\d+\.?\d*\s*\*\s*\d+\.?\d*\s*\*)?\):(\d+\.?\d*\s*\*\s*\d+\.?\d*\s*\*)?\.set\((\d+\.?\d+)\)', prog)
    
    patterns = []
    height_groups = []
    
    # The seed has patterns 0-11 in _create_step_initializer
    # Extract heights and note their positions for recombination
    all_heights = []
    for match in re.finditer(r'f\.at\([^)]+\)\.set\((\d+\.?\d+)\)', prog):
        all_heights.append({
            "height": float(match.group(1)),
            "position": len([m for m in re.finditer(r'f\.at\([^)]+\)\.set', prog[:match.start()])])
        })
    
    # Identify the 13 pattern types and their key heights
    pattern_info = [
        {"id": 0, "key_heights": [1.40], "type": "single_peak"},
        {"id": 1, "key_heights": [1.50], "type": "higher_peak"},
        {"id": 2, "key_heights": [1.60], "type": "narrow_peak"},
        {"id": 3, "key_heights": [0.90, 1.90, 0.90], "type": "multi_level_symmetric"},
        {"id": 4, "key_heights": [1.10, 2.30, 1.40], "type": "asymmetric_multi"},
        {"id": 5, "key_heights": [1.50, 1.50], "type": "two_steps"},
        {"id": 6, "key_heights": [0.70, 1.30, 1.70, 1.00], "type": "four_level"},
        {"id": 7, "key_heights": [0.80, 2.00, 0.80], "type": "central_peak_wings"},
        {"id": 8, "key_heights": [0.60, 1.00, 1.50, 1.20], "type": "staircase"},
        {"id": 9, "key_heights": [1.70], "type": "very_high_peak"},
        {"id": 10, "key_heights": [1.65], "type": "high_peak_variant"},
        {"id": 11, "key_heights": [0.70, 1.50, 2.10, 1.50, 0.70], "type": "pyramid"},
        {"id": 12, "key_heights": [0.60, 1.30, 2.00, 1.30, 0.60], "type": "ultra_stretched_pyramid"}
    ]
    
    return {
        "pattern_count": 13,
        "patterns": pattern_info,
        "all_heights": all_heights,
        "analysis": "Use heights from different patterns to create recombination candidates"
    }
