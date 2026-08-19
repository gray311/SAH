def run(ctx, args):
    import math
    families = args.get("families", ["step", "smoothed_step", "gaussian", "bspline", "poly"])
    results = []
    for fam in families:
        if fam == "step":
            f = ctx.get_best_program()
        elif fam == "smoothed_step":
            base_f = ctx.get_best_program()
            f = base_f
        elif fam == "gaussian":
            f_code = "import jax.numpy as jnp\nimport jax\ndef f(x):\n    x = jnp.asarray(x)\n    sigma1, sigma2, sigma3 = 1.0, 1.5, 2.0\n    mu1, mu2, mu3 = -1.0, 0.0, 1.0\n    w1, w2, w3 = 0.35, 0.30, 0.35\n    c1 = w1 * jnp.exp(-jnp.power(x - mu1, 2) / (2 * sigma1**2))\n    c2 = w2 * jnp.exp(-jnp.power(x - mu2, 2) / (2 * sigma2**2))\n    c3 = w3 * jnp.exp(-jnp.power(x - mu3, 2) / (2 * sigma3**2))\n    return jnp.maximum(0.0, c1 + c2 + c3)"
            f = f_code
        elif fam == "bspline":
            f_code = "import jax.numpy as jnp\nfrom scipy.interpolate import BSpline\ndef f(x):\n    knots = jnp.array([-1.0, 0.0, 1.0])\n    coeffs = jnp.array([1.0, 1.0, 1.0])\n    return jnp.maximum(0.0, BSpline(knots, coeffs, k=2)(x))"
            f = f_code
        elif fam == "poly":
            f_code = "import jax.numpy as jnp\ndef f(x):\n    x = jnp.asarray(x)\n    mask = (x >= 0) & (x <= 1)\n    poly = 1.0 - jnp.power(x - 0.5, 2) * 4.0\n    return jnp.where(mask, jnp.maximum(0.0, poly), 0.0)"
            f = f_code
        else:
            f = ctx.get_best_program()
        
        ctx.stage_edit(f)
        probe_score = ctx.probe()
        results.append({"family": fam, "probe_results": probe_score})
    
    return {"families_tested": families, "probe_results": results}
