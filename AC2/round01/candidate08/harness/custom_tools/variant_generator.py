def run(ctx, args):
    current_code = ctx.get_program()
    best_code = ctx.get_best_program()
    notes = ctx.scratch_read("strategy_notes") or ""
    
    import re
    
    # Extract key parameters from the code
    patterns = [
        r'num_intervals:\s*(\d+)',
        r'learning_rate:\s*([\d.e+-]+)',
        r'num_steps:\s*(\d+)',
        r'warmup_steps:\s*(\d+)'
    ]
    
    param_names = ['intervals', 'lr', 'steps', 'warmup']
    params = {}
    for pat, name in zip(patterns, param_names):
        m = re.search(pat, current_code)
        if m:
            params[name] = m.group(1)
    
    variants = []
    
    # Variant 1: Coarser resolution (start simple)
    if 'intervals' in params:
        variants.append({
            "name": "coarser_grid",
            "edit": f"num_intervals: int = {int(params['intervals']) // 2}",
            "reason": "Coarse-to-fine optimization strategy"
        })
    
    # Variant 2: More steps, smaller LR
    if 'steps' in params and 'lr' in params:
        variants.append({
            "name": "more_steps_larger_lr",
            "edit": f"num_steps: int = {int(params['steps']) * 2}, learning_rate: float = {float(params['lr']) * 2 if float(params['lr']) < 0.01 else 0.01}",
            "reason": "More exploration budget with adaptive learning rate"
        })
    
    # Variant 3: Piecewise linear with more breakpoints
    variants.append({
        "name": "denser_piecewise",
        "edit": "# Change to piecewise linear with adaptive breakpoints",
        "reason": "Use piecewise constant/linear with optimized breakpoints"
    })
    
    # Variant 4: Fourier-based approach
    variants.append({
        "name": "fourier_rep",
        "edit": "# Switch to Fourier coefficient optimization with positivity constraints",
        "reason": "Exploit frequency domain structure"
    })
    
    ctx.scratch_write("variants_generated", str(variants))
    return {"variants": variants[:5], "note": f"Based on: {params}"}