def run(ctx, args):
    import re
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"note": "no evolve block"}
    
    # Extract current heights from patterns like f.at[...].set(1.40)
    heights = re.findall(r'\.set\((\d+\.?\d*)\)', prog)
    heights = [float(h) for h in heights if h]
    
    # Extract interval positions
    intervals = re.findall(r'int\((\d+\.?\d*)\*n\)', prog)
    intervals = [float(i) for i in intervals]
    
    if not heights:
        return {"note": "could not parse heights", "proposals": []}
    
    max_h = max(heights)
    min_h = min(heights)
    avg_h = sum(heights) / len(heights)
    
    # Get pattern index from current best
    pattern_idx = re.search(r'pattern_idx = (\d+)', prog)
    pattern_idx = int(pattern_idx.group(1)) if pattern_idx else 0
    
    proposals = []
    
    # Variations strategy:
    # 1. Small height tweaks on all steps
    # 2. Height tweak on central peak only
    # 3. Width adjustments (shift boundaries)
    # 4. Combined small changes
    
    for i, h in enumerate(heights):
        h_new = h + 0.05
        if h_new <= 2.5:
            proposals.append({
                "name": f"height_tweak_{i}",
                "description": f"Increase step {i} height by 0.05",
                "heights": list(heights),
                "changes": [i]
            })
    
    for i, h in enumerate(heights):
        h_new = h - 0.03
        if h_new >= 0.5:
            proposals.append({
                "name": f"height_reduce_{i}",
                "description": f"Decrease step {i} height by 0.03",
                "heights": list(heights),
                "changes": [i]
            })
    
    if len(heights) >= 2:
        mid = len(heights) // 2
        proposals.append({
            "name": "peak_focus",
            "description": f"Boost central peak, reduce sides",
            "heights": heights[:],
            "changes": [mid]
        })
        proposals[-1]["heights"][mid] += 0.08
        for j in range(len(heights)):
            if j != mid:
                proposals[-1]["heights"][j] -= 0.02
    
    proposals.append({
        "name": "random_small",
        "description": "Random small adjustments to 2-3 steps",
        "heights": heights[:],
        "changes": []
    })
    import random
    random.seed(42)
    idxs = random.sample(range(len(heights)), min(3, len(heights)))
    for idx in idxs:
        proposals[-1]["heights"][idx] += random.uniform(-0.08, 0.08)
    
    return {
        "pattern_idx": pattern_idx,
        "current_heights": heights,
        "avg_height": avg_h,
        "proposals": proposals
    }
