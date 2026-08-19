def run(ctx, args):
    code = ctx.get_program()
    import re
    
    # Extract num_intervals
    interval_match = re.search(r'num_intervals:\s*(\d+)', code)
    current_intervals = int(interval_match.group(1)) if interval_match else 400
    
    # Check for padding
    has_padding = 'pad' in code.lower() and ('fft' in code.lower() or 'convolution' in code.lower())
    
    # Check for normalization
    has_normalization = ('int_f' in code or 'sum(f' in code) and ('scale' in code.lower() or 'norm' in code.lower())
    
    # Check interval adequacy based on pattern complexity
    pattern_complexity = 0
    if '1.42' in code or '1.52' in code or '1.62' in code:
        pattern_complexity += 1
    if 'piecewise' in code.lower() or 'where' in code:
        pattern_complexity += 2
    if 'gaussian' in code.lower() or 'exp' in code:
        pattern_complexity += 1
    
    # Recommended intervals: more complex = more intervals
    if pattern_complexity >= 3:
        recommended_intervals = 1200
    elif pattern_complexity >= 2:
        recommended_intervals = 800
    elif current_intervals < 400:
        recommended_intervals = max(400, current_intervals * 2)
    else:
        recommended_intervals = 600
    
    # Quality score: better if intervals match complexity and has stability
    stability_bonus = 1.0 if has_padding else 0.6
    resolution_bonus = 1.0 if recommended_intervals <= current_intervals <= recommended_intervals * 1.5 else 0.7
    
    quality_score = min(1.0, stability_bonus * resolution_bonus)
    
    return {
        'current_intervals': current_intervals,
        'recommended_intervals': recommended_intervals,
        'has_padding': has_padding,
        'has_normalization': has_normalization,
        'discretization_quality_score': quality_score,
        'pattern_complexity': pattern_complexity,
        'recommendation': f"Consider {recommended_intervals} intervals" + ("" if has_padding else " and add FFT padding"),
        'action': "increase_resolution" if current_intervals < recommended_intervals * 0.8 else "decrease_resolution" if current_intervals > recommended_intervals * 1.2 else "fine-tune"
    }
