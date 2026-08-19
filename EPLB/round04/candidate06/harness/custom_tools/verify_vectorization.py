def run(ctx, args):
    code = ctx.get_program()
    has_loops = 'for p in valid' in code or 'for group in indices' in code or 'for pack in' in code
    has_sort = 'argsort' in code and 'torch' in code
    return {"is_vectorized": not has_loops or has_sort, "note": "Use torch.argsort with broadcasting, no Python loops"}