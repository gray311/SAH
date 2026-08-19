def run(ctx, args):
    import re
    best_code = ctx.get_best_program()
    
    # Extract key parameters from seed structure
    lines = best_code.split('\n')
    num_intervals = 600
    
    def make_step(f, start, end, height):
        return f.at[start:end].set(height)
    
    def make_multi_step(f, ranges, heights):
        for (start, end), height in zip(ranges, heights):
            f = make_step(f, start, end, height)
        return f
    
    patterns = []
    
    # Pattern 1: Widen peak by 8%
    start = int(0.22 * num_intervals)
    end = int(0.78 * num_intervals)
    f = ctx.stage_edit(best_code)
    # Modify the step pattern to be wider
    patterns.append({
        'name': 'wider_peak',
        'edit': f"start = int(0.22 * n)\nend = int(0.78 * n)\nf = f.at[start:end].set(1.45)"
    })
    
    # Pattern 2: Two-peak configuration
    patterns.append({
        'name': 'two_peaks',
        'edit': f"start1 = int(0.28 * n)\nend1 = int(0.38 * n)\nheight1 = 1.80\nstart2 = int(0.62 * n)\nend2 = int(0.72 * n)\nheight2 = 1.80\nf = f.at[start1:end1].set(height1)\nf = f.at[start2:end2].set(height2)"
    })
    
    # Pattern 3: Asymmetric peaks
    patterns.append({
        'name': 'asymmetric',
        'edit': f"start1 = int(0.20 * n)\nend1 = int(0.35 * n)\nheight1 = 2.00\nstart2 = int(0.65 * n)\nend2 = int(0.80 * n)\nheight2 = 1.70\nf = f.at[start1:end1].set(height1)\nf = f.at[start2:end2].set(height2)"
    })
    
    # Pattern 4: Concentrated energy
    patterns.append({
        'name': 'concentrated',
        'edit': f"start = int(0.30 * n)\nend = int(0.70 * n)\nf = f.at[start:end].set(2.20)"
    })
    
    return {"patterns": patterns, "num_intervals": num_intervals}
