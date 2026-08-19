def run(ctx, args):
    import re
    code = ctx.get_program()
    
    # Detect construction approach
    code_lower = code.lower()
    
    has_structured = 'quadratic' in code_lower or 'paley' in code_lower or 'structured' in code_lower or 'residue' in code_lower
    has_hill_climb = 'hill' in code_lower or 'climb' in code_lower or 'annealing' in code_lower or 'simulated' in code_lower
    has_random = 'random' in code_lower
    has_numpy = 'numpy' in code_lower
    has_bareiss = 'bareiss' in code_lower
    
    analysis = {
        "construction_type": "unknown",
        "has_structured_init": has_structured,
        "has_optimization": has_hill_climb,
        "has_randomness": has_random,
        "uses_numpy": has_numpy,
        "has_determinant_calc": has_bareiss,
        "code_length": len(code)
    }
    
    # Extract seed if present
    seed_val = None
    seed_match = re.search(r'seed=(\d+)', code)
    if seed_match:
        seed_val = int(seed_match.group(1))
        analysis["has_seed"] = True
    
    # Extract max_iters if present
    iters_match = re.search(r'max_iters=(\d+)', code)
    if iters_match:
        analysis["max_iters"] = int(iters_match.group(1))
        analysis["has_max_iters"] = True
    
    # Extract temp0 if present
    temp_match = re.search(r'temp0=([\d.]+)', code)
    if temp_match:
        analysis["temp0"] = float(temp_match.group(1))
        analysis["has_temp0"] = True
    
    # Extract QR set if present
    qr_match = re.search(r'quadratic_residues\s*=\s*\{([^}]+)\}', code)
    if qr_match:
        qr_str = qr_match.group(1)
        qr_nums = [int(x.strip()) for x in qr_str.split(',') if x.strip().isdigit()]
        analysis["qr_set"] = qr_nums
        analysis["has_qr_set"] = True
    
    analysis["construction_type"] = "structured_paley" if has_structured and has_qr else "hill_climb" if has_hill_climb else "random"
    
    return analysis
