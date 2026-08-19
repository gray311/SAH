def run(ctx, args):
    best_f = ctx.get_best_program()
    lines = best_f.split('\n')
    
    num_intervals = 600
    heights = []
    intervals = []
    in_block = False
    
    for line in lines:
        if 'f = jnp.zeros' in line or 'f_values' in line:
            import re
            match = re.search(r'jnp\.zeros\s*\(\s*(\d+)\s*\)', line)
            if match:
                num_intervals = int(match.group(1))
        
        if '.set(' in line or '.at[' in line:
            match = re.search(r'\.set\s*\(\s*([\d.]+)\s*\)', line)
            if match:
                h = float(match.group(1))
                heights.append(h)
    
    unique_heights = sorted(list(set([round(h, 2) for h in heights])))
    peak_positions = []
    if len(heights) >= 2:
        max_h = max(heights)
        peaks = [i for i, h in enumerate(heights) if abs(h - max_h) < 0.1]
        if peaks:
            peak_positions.append(len(peaks))
    
    symmetry = "unknown"
    if len(heights) >= 10:
        left_half = heights[:len(heights)//2]
        right_half = heights[len(heights)//2:]
        if len(left_half) == len(right_half):
            left_avg = sum(left_half) / len(left_half)
            right_avg = sum(right_half) / len(right_half)
            if abs(left_avg - right_avg) < 0.1:
                symmetry = "symmetric"
            else:
                symmetry = "asymmetric"
    
    return {
        "num_intervals": num_intervals,
        "unique_heights": unique_heights,
        "peak_count": peak_positions[0] if peak_positions else 1,
        "symmetry": symmetry,
        "total_unique_values": len(unique_heights),
        "note": f"Analysis of {num_intervals}-interval function with {len(unique_heights)} unique heights, {symmetry}"
    }
