def run(ctx, args):
    program = ctx.get_program()
    import re
    patterns = []
    
    # Extract all pattern definitions
    pattern_blocks = re.findall(r'elif pattern_idx == \d+:.*?f = f\.at\[int\(0\.[\d\.]+\*n\):int\(0\.[\d\.]+\*n\)\]\.set\(([\d.]+)\)', program, re.DOTALL)
    
    for idx, block in enumerate(pattern_blocks[:12]):
        heights = re.findall(r'set\(([\d.]+)\)', block)
        if heights:
            height = float(heights[0])
            start_pct = re.search(r'int\(0\.(\d+)\*n\)', block)
            end_pct = re.search(r'int\(0\.(\d+)\*n\)', block)
            start = float(start_pct.group(1)) if start_pct else 0.0
            end = float(end_pct.group(1)) if end_pct else 1.0
            support_width = end - start
            patterns.append({
                'pattern_idx': idx,
                'height': height,
                'support_width': support_width,
                'description': f"Pattern {idx}: height={height}, support=[{start:.2f},{end:.2f}]"
            })
    
    return {
        'patterns': patterns,
        'note': 'Analyzed step patterns. Use generate_variants to create targeted edits on best pattern.'
    }
