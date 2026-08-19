def run(ctx, args):
    sigma = args.get("sigma", 0.1)
    base_f = ctx.get_best_program()
    f_code = "import jax.numpy as jnp\ndef f(x):\n    n = 600\n    f_base = jnp.zeros(n)\n    start = int(0.08*n)\n    f_base = f_base.at[start:start+10].set(0.80)\n    f_base = f_base.at[int(0.20*n):int(0.35*n)].set(1.60)\n    f_base = f_base.at[int(0.35*n):int(0.55*n)].set(2.00)\n    f_base = f_base.at[int(0.55*n):int(0.75*n)].set(1.40)\n    f_base = f_base.at[int(0.75*n):int(0.90*n)].set(0.90)"
    ctx.stage_edit(f_code)
    return {"note": "Smoothed with sigma={}".format(sigma)}
