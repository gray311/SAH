def run(ctx, args):
    min_x = args.get("min_x", 0)
    max_x = args.get("max_x", 100000)
    min_y = args.get("min_y", 0)
    max_y = args.get("max_y", 100000)
    
    # Quick grid-based approximation (sample every 10th point)
    mackerels = ctx.read_input_df("mackerels.csv", nrows=5000)
    sardines = ctx.read_input_df("sardines.csv", nrows=5000)
    
    # Approximate counts by subsampling
    sample_step = 50
    m_count = 0
    s_count = 0
    
    for idx in range(0, len(mackerels), sample_step):
        if mackerels.iloc[idx].get('x') is not None and mackerels.iloc[idx].get('y') is not None:
            if mackerels.iloc[idx]['x'] >= min_x and mackerels.iloc[idx]['x'] <= max_x and \
               mackerels.iloc[idx]['y'] >= min_y and mackerels.iloc[idx]['y'] <= max_y:
                m_count += 1
    
    for idx in range(0, len(sardines), sample_step):
        if sardines.iloc[idx].get('x') is not None and sardines.iloc[idx].get('y') is not None:
            if sardines.iloc[idx]['x'] >= min_x and sardines.iloc[idx]['x'] <= max_x and \
               sardines.iloc[idx]['y'] >= min_y and sardines.iloc[idx]['y'] <= max_y:
                s_count += 1
    
    # Scale back to estimate full counts
    scale_factor = len(mackerels) / sample_step
    est_m = int(m_count * scale_factor)
    est_s = int(s_count * scale_factor)
    
    return {
        "approx_mackerels": est_m,
        "approx_sardines": est_s,
        "approx_score": max(0, est_m - est_s + 1)
    }