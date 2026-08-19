def run(ctx, args):
    import numpy as np
    
    candidates = args.get("candidates", [])
    probe_scores = args.get("probe_scores", [None] * len(candidates))
    
    results = []
    for i, (threshold, h) in enumerate(candidates):
        if probe_scores[i] is not None:
            c5_bound = 0.38092303510845016 / probe_scores[i]  # approximate
        else:
            # Compute c5_bound for this bipartite function
            h_padded = np.pad(h, (0, len(h)))
            j_padded = np.pad(1.0 - h, (0, len(h)))
            corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
            correlation = np.fft.ifft(corr_fft).real
            dx = 2.0 / len(h)
            c5_bound = float(np.max(correlation * dx))
        
        results.append({
            "threshold": threshold,
            "c5_bound": c5_bound,
            "combined_score": 0.38092303510845016 / c5_bound if c5_bound > 0 else float('inf')
        })
    
    # Sort by combined_score (descending)
    results.sort(key=lambda x: x["combined_score"], reverse=True)
    
    top_k = results[:5]  # Return top 5 candidates
    
    return {
        "ranked_candidates": top_k,
        "recommended_for_eval": top_k[:2],  # Recommend top 2 for full evaluation
        "note": f"Ranked {len(candidates)} bipartite candidates, top 2 recommended for full evaluation"
    }
