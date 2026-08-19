def run(ctx, args):
    code = ctx.get_program()
    analysis = {
        "truncated_function": None,
        "potential_params": [],
        "has_missing_libs": False
    }
    lines = code.split('\n')
    last_complete_line = len(lines)
    for i in range(len(lines)-1, -1, -1):
        line = lines[i].strip()
        if line and not (line.startswith('"""') or line.startswith("'''") or
                        line == '' or line.startswith('#') or
                        line.endswith(':') or line.endswith('=') or
                        line.endswith(',') or line.endswith(']') or
                        line.endswith(')') or line.endswith('{')):
            last_complete_line = i
            break
    if last_complete_line < len(lines) - 2:
        analysis["truncated_function"] = f"Function possibly truncated near line {last_complete_line+1}"
    else:
        analysis["truncated_function"] = "No obvious truncation detected"
    if 'def rebalance_experts_hierarchical' in code:
        func_start = code.find('def rebalance_experts_hierarchical')
        if func_start >= 0:
            func_end = code.find('\n\ndef ', func_start+1)
            if func_end == -1:
                func_end = code.find('\n# ', func_start+1)
            if func_end == -1:
                func_end = len(code)
            func_body = code[func_start:func_end]
            import re
            numeric_vars = re.findall(r'(\w+)\s*=\s*\d+(\.\d+)?', func_body)
            analysis["potential_params"] = [v[0] for v in numeric_vars[:10]]
    analysis["has_missing_libs"] = 'import numpy' not in code and 'import torch' not in code
    analysis["summary"] = f"Truncation: {analysis['truncated_function']}; Potential params: {analysis['potential_params']}; Missing libs: {analysis['has_missing_libs']}"
    return analysis
