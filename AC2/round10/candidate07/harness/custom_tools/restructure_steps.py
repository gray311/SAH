def run(ctx, args):
    import re
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"note": "no evolve block", "action": "skip"}
    edit_type = args.get("edit_type", "merge")
    n = 450
    if edit_type == "merge":
        code = "f = jnp.zeros(n)\nf = f.at[int(0.0*n):int(0.3*n)].set(1.0)\nf = f.at[int(0.3*n):int(0.7*n)].set(1.8)\nf = f.at[int(0.7*n):int(0.95*n)].set(0.9)\n"
    elif edit_type == "split":
        code = "f = jnp.zeros(n)\nf = f.at[int(0.05*n):int(0.25*n)].set(0.7)\nf = f.at[int(0.25*n):int(0.45*n)].set(1.2)\nf = f.at[int(0.45*n):int(0.65*n)].set(2.1)\nf = f.at[int(0.65*n):int(0.95*n)].set(0.8)\n"
    elif edit_type == "reorder":
        code = "f = jnp.zeros(n)\nf = f.at[int(0.0*n):int(0.18*n)].set(1.1)\nf = f.at[int(0.18*n):int(0.42*n)].set(2.4)\nf = f.at[int(0.42*n):int(0.78*n)].set(1.3)\nf = f.at[int(0.78*n):int(0.98*n)].set(0.9)\n"
    elif edit_type == "reshape":
        code = "f = jnp.zeros(n)\nf = f.at[int(0.0*n):int(0.30*n)].set(0.65)\nf = f.at[int(0.30*n):int(0.70*n)].set(2.25)\nf = f.at[int(0.70*n):int(1.0*n)].set(0.65)\n"
    elif edit_type == "retune":
        code = "num_intervals = 650\nf = jnp.zeros(n)\nf = f.at[int(0.1*n):int(0.28*n)].set(1.15)\nf = f.at[int(0.28*n):int(0.72*n)].set(2.05)\nf = f.at[int(0.72*n):int(0.88*n)].set(1.05)\n"
    elif edit_type == "bimodal":
        code = "f = jnp.zeros(n)\nf = f.at[int(0.1*n):int(0.35*n)].set(2.0)\nf = f.at[int(0.35*n):int(0.65*n)].set(0.5)\nf = f.at[int(0.65*n):int(0.9*n)].set(1.9)\n"
    elif edit_type == "plateau":
        code = "f = jnp.zeros(n)\nf = f.at[int(0.0*n):int(0.25*n)].set(0.8)\nf = f.at[int(0.25*n):int(0.55*n)].set(1.6)\nf = f.at[int(0.55*n):int(0.75*n)].set(2.3)\nf = f.at[int(0.75*n):int(1.0*n)].set(1.1)\n"
    else:
        code = "f = jnp.zeros(n)\nf = f.at[int(0.05*n):int(0.20*n)].set(0.7)\nf = f.at[int(0.20*n):int(0.35*n)].set(1.3)\nf = f.at[int(0.35*n):int(0.65*n)].set(1.9)\nf = f.at[int(0.65*n):int(0.95*n)].set(0.9)\n"
    return {"action": "edit", "new_code": code, "edit_type": edit_type}
