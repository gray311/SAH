def run(ctx, args):
    import numpy as np
    
    h = ctx.get_program()
    
    N = 800
    domain = 2.0
    dx = domain / N
    
    analysis = {}
    
    if "golomb" in h.lower() or "marks = np.array" in h:
        marks = [0.0, 0.4, 0.8, 1.2, 1.6]
        analysis = {
            "type": "golomb_rule",
            "current_marks": marks,
            "suggested_mutation": "Perturb marks: [0.0, 0.38, 0.75, 1.15, 1.58]",
            "rationale": "Slightly irregular spacing can reduce correlation peaks"
        }
    elif "tri" in h.lower() or "peak" in h.lower():
        peaks = [0.4, 1.0, 1.6]
        analysis = {
            "type": "tri_modal",
            "current_peaks": peaks,
            "suggested_mutation": "Shift peaks: [0.42, 1.0, 1.58], bw=0.12",
            "rationale": "Narrow/wide peaks can reduce overlap"
        }
    elif "bipartite" in h.lower() or "threshold" in h.lower():
        analysis = {
            "type": "bipartite",
            "current_threshold": 0.5,
            "suggested_mutation": "Shift threshold to 0.45 or 0.55",
            "rationale": "Asymmetric bipartition may reduce overlap"
        }
    else:
        analysis = {
            "type": "unknown",
            "suggested_mutation": "Try Golomb ruler pattern with marks [0.0, 0.4, 0.8, 1.2, 1.6]",
            "rationale": "Structural change needed - start from known good pattern"
        }
    
    return analysis