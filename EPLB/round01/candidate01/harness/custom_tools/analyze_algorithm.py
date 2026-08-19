def run(ctx, args):
    program = ctx.get_program()
    lines = program.split('\n')
    
    # Extract weight tensor usage
    weight_refs = 0
    loop_count = 0
    for line in lines:
        if 'weight:' in line.lower() or 'weight' in line and '[' in line and ']' in line:
            weight_refs += 1
        if 'for ' in line or 'for(' in line:
            loop_count += line.count('for ')
    
    # Parse function signatures
    functions = []
    func_name = ""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('def '):
            if func_name and func_name != "":
                functions.append(func_name)
            func_name = stripped[4:].split('(')[0]
    if func_name and func_name != "":
        functions.append(func_name)
    
    return {
        "num_weight_refs": weight_refs,
        "estimated_loop_count": loop_count,
        "functions": functions,
        "recommendation": "Vectorize loops using torch operations"
    }
