def run(ctx, args):
    program = ctx.get_program()
    lines = program.split('\n')
    in_balanced_packing = False
    hotspot_lines = []
    python_loop_lines = []
    
    for i, line in enumerate(lines):
        if 'def balanced_packing(' in line:
            in_balanced_packing = True
        elif in_balanced_packing and line.strip().startswith('def '):
            in_balanced_packing = False
        elif in_balanced_packing:
            if 'for ' in line and ':' in line:
                python_loop_lines.append((i+1, line.strip()))
            if '[' in line and 'for' in line:
                python_loop_lines.append((i+1, line.strip()))
            if 'min(' in line and 'lambda' in line:
                python_loop_lines.append((i+1, line.strip()))
    
    analysis = {
        "python_loops_detected": len(python_loop_lines),
        "hotspot_lines": [line[1] for line in python_loop_lines],
        "vectorization_recommendation": "Vectorize " + str(len(python_loop_lines)) + " Python loop(s) using torch operations. Replace for-loops with argsort/scatter.",
        "estimated_speedup": "5-10x if loops are eliminated"
    }
    return analysis
