def run(ctx, args):
    import re
    code = ctx.get_program()
    block_start = code.find('# EVOLVE-BLOCK-START')
    block_end = code.find('# EVOLVE-BLOCK-END')
    if block_start == -1 or block_end == -1:
        return {"error": "EVOLVE-BLOCK markers not found"}
    block = code[block_start:block_end]
    param_map = {
        'learning_rate': (r'learning_rate:\s*([\d.]+)', lambda m: float(m.group(1)) * (1 + args.get('delta', 0.1))),
        'num_intervals': (r'num_intervals:\s*(\d+)', lambda m: int(m.group(1)) * int(args.get('delta', 0.1))),
        'num_steps': (r'num_steps:\s*(\d+)', lambda m: int(m.group(1)) * int(args.get('delta', 0.1))),
        'best_c2': (r'best_c2:\s*([\d.]+)', lambda m: float(m.group(1)) * (1 + args.get('delta', 0.1))),
        'warmup_steps': (r'warmup_steps:\s*(\d+)', lambda m: int(m.group(1)) * int(args.get('delta', 0.1))),
    }
    if args.get('param_name') not in param_map:
        return {"error": f"Unknown param: {args.get('param_name')}"}
    pattern, transform = param_map[args['param_name']]
    match = re.search(pattern, block)
    if not match:
        return {"error": f"Param not found in block: {args.get('param_name')}"}
    old_val = match.group(0)
    new_val = transform(match)
    new_block = re.sub(old_val, f'{args.get("param_name")}:\t{new_val}', block, count=1)
    return ctx.stage_edit(f"# Perturbed {args.get('param_name')} by {args.get('delta')}\n")