def run(ctx, args):
    import math
    import re
    
    code = ctx.get_program()
    lines = code.split('\n')
    
    # Find rebalance_experts_hierarchical function
    func_start = None
    func_end = None
    in_function = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if 'def rebalance_experts_hierarchical' in line:
            func_start = i
            in_function = True
        elif in_function and func_start is not None:
            if stripped.startswith('def ') and 'rebalance_experts_hierarchical' not in line:
                func_end = i
                break
            if stripped.startswith('rebalance_experts_hierarchical(') and 'def ' not in line:
                continue
    
    if func_start is None:
        return {"load_balance_score": 0.0, "execution_time_estimate_ms": 1000.0,
                "structural_notes": "Could not find rebalance_experts_hierarchical function"}
    
    if func_end is None:
        func_end = len(lines)
    
    func_lines = lines[func_start:func_end]
    func_code = '\n'.join(func_lines)
    
    has_return = 'return' in func_code.lower()
    has_tensor_ops = 'torch.' in func_code
    has_loops = 'for ' in func_code or 'while' in func_code
    
    issues = []
    if not has_return:
        issues.append("Missing return statement in function")
    if 'assert' in func_code.upper() and 'rebalance' not in func_code.lower():
        issues.append("Missing assertion checks")
    
    num_for_loops = len(re.findall(r'for\s+\w+\s+in', func_code))
    num_torch_calls = len(re.findall(r'torch\.', func_code))
    num_iterate = len(re.findall(r'iterate', func_code, re.IGNORECASE))
    
    base_time = 50.0
    if num_torch_calls > 15:
        base_time *= 1.5
    if num_for_loops > 8:
        base_time *= 1.3
    if num_iterate > 0:
        base_time *= 1.2
    
    base_time = min(base_time, 2000.0)
    
    balance_patterns = ['balanced', 'pack', 'replica', 'rebalance', 'minimize', 'load_']
    has_balance_logic = any(p in func_code.lower() for p in balance_patterns)
    has_indexing = 'pack_index' in func_code or 'rank_in_pack' in func_code or 'phy2log' in func_code
    
    score = 0.0
    if has_return and has_balance_logic:
        score = 0.7 + 0.2 * has_tensor_ops
    elif has_return:
        score = 0.5
    elif has_indexing:
        score = 0.4
    else:
        score = 0.2 + 0.1 * num_for_loops * 0.1
    
    score = min(score, 0.95)
    
    notes = []
    if issues:
        notes.extend(issues)
    if has_balance_logic:
        notes.append("Balancing logic detected")
    if has_tensor_ops:
        notes.append("Using PyTorch tensors")
    if has_loops:
        notes.append("Contains iterative logic")
    if not notes:
        notes.append("Code structure appears incomplete")
    
    return {
        "load_balance_score": round(score, 4),
        "execution_time_estimate_ms": round(base_time, 2),
        "structural_notes": "; ".join(notes)
    }
