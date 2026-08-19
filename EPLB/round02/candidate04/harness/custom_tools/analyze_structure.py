def run(ctx, args):
    code = ctx.get_program()
    lines = code.split('\n')
    in_block = False
    block_lines = []
    block_start = -1
    for i, line in enumerate(lines):
        if 'EVOLVE-BLOCK-START' in line:
            in_block = True
            block_start = i
        elif in_block and line.strip().startswith('def rebalance_experts'):
            block_lines = lines[block_start+1:i]
            break
    if not block_lines:
        return {"note": "Could not find EVOLVE-BLOCK"}
    
    code_block = '\n'.join(block_lines)
    score = 0
    suggestions = []
    
    # Check for python loops
    if 'for ' in code_block and 'in range' in code_block:
        score += 10
        suggestions.append("Consider numpy vectorization for loop elimination")
    
    if '.sort' in code_block or 'torch.sort' in code_block:
        score += 5
        suggestions.append("Sort is used for initial ordering")
    
    # Check for in-place operations
    if '=' in code_block and '=' not in ['def ', '->', 'type:']:
        score += 15
        suggestions.append("Stateful tracking for optimization potential")
    
    # Count complexity hints
    import re
    loops = len(re.findall(r'for\s+\w+\s+in', code_block))
    if loops > 3:
        score += 20
        suggestions.append(f"Multiple loops ({loops}) - vectorization could help")
    
    return {
        "block_lines": len(block_lines),
        "has_loops": loops > 0,
        "complexity_estimate": score,
        "suggestions": suggestions,
        "note": "Use suggestions to form next hypothesis"
    }
