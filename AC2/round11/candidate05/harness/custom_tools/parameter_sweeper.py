def run(ctx, args):
    prog = ctx.get_program()
    if '# EVOLVE-BLOCK' not in prog:
        return {"note": "no evolve block", "proposals": []}
    return {"variations": [{"height_shifts": [1.42, 1.45, 1.48, 1.52, 1.38]}, {"interval_shifts": [0.23, 0.24, 0.26, 0.27]}]}
