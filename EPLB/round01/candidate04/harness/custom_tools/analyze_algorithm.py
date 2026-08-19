def run(ctx, args):
    code = ctx.get_program()
    lines = code.split('\n')
    
    def find_function_body(name):
        for i, line in enumerate(lines):
            if line.strip().startswith('def ' + name + '('):
                j = i + 1
                indent = len(lines[i]) - len(lines[i].lstrip())
                while j < len(lines) and (len(lines[j]) - len(lines[j].lstrip()) > indent or lines[j].strip().startswith('def ')):
                    j += 1
                return '\n'.join(lines[i+1:j])
        return None
    
    report = []
    funcs_to_check = ['balanced_packing', 'replicate_experts']
    
    for fname in funcs_to_check:
        body = find_function_body(fname)
        if body:
            has_loops = bool([l for l in body.split('\n') if 'for ' in l and 'in range' in l])
            has_torch_ops = bool([l for l in body.split('\n') if 'torch.' in l])
            nops = body.count('torch.')
            if has_loops:
                report.append(fname + ': Has Python loops (NEED vectorization)')
            else:
                report.append(fname + ': Vectorized OK')
            report.append(fname + ': Uses ' + str(nops) + ' torch ops')
    
    report.append('\nRecommendations:')
    if len([l for l in lines if 'for ' in l and 'in range' in l]) > 0:
        report.append('1. Replace for-loops with torch.argsort() + scatter operations')
        report.append('2. Use torch.cumsum() for running totals')
        report.append('3. Batch all operations to reduce overhead')
    else:
        report.append('1. Consider further optimization: tensor fusion, GPU kernels')
    
    return {'analysis': '\n'.join(report), 'needs_vectorization': len(report) > 0}
