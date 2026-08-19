def run(ctx, args):
    best_prog = ctx.get_best_program()
    lines = best_prog.split('\n')
    
    struct = {
        'peak_width': 0.0,
        'edge_positions': [],
        'smoothness_estimate': 0.0,
        'dominant_scale': 1.0,
        'num_peaks': 1
    }
    
    import re
    # Extract interval patterns and infer structure
    in_interval = False
    peaks = []
    edges = []
    
    for i, line in enumerate(lines):
        if 'start =' in line or 'int(' in line:
            if '0.' in line or 'int(' in line:
                try:
                    match = re.search(r'[0-9.]+', line)
                    if match:
                        pos = float(match.group()) / 100.0
                        edges.append(pos)
                except:
                    pass
        
        if 'height' in line.lower():
            try:
                match = re.search(r'[0-9.]+', line)
                if match:
                    h = float(match.group())
                    peaks.append(h)
            except:
                pass
    
    struct['edge_positions'] = edges[:5] if edges else [0.25, 0.75]
    struct['smoothness_estimate'] = 0.9 if len(edges) < 4 else 0.5
    
    if peaks:
        struct['dominant_scale'] = max(peaks)
        struct['num_peaks'] = len([p for p in peaks if p > struct['dominant_scale'] * 0.9])
    
    if len(edges) >= 2:
        spread = max(edges) - min(edges) if edges else 0.5
        struct['peak_width'] = spread * 0.6 if spread > 0 else 0.3
    
    return struct
