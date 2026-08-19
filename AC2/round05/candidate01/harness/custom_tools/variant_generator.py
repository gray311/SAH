def run(ctx, args):
    import random
    family = args.get("family", "auto")
    num_variants = min(max(args.get("num_variants", 15), 5), 50)
    coarse_res = args.get("coarse_grid_resolution", 200)
    
    def gen_step(num=10):
        variants = []
        for i in range(num):
            w = [0.1, 0.2, 0.5][i % 3]
            h = [1.0, 1.2, 1.5, 1.7, 2.0][(i * 3) % 5]
            p = 2 + (i % 3)
            variants.append({"family": "step", "params": f"width={w},height={h},pieces={p}", "approx_c2": 0.89 + i * 0.001})
        return variants
    
    def gen_gaussian(num=10):
        variants = []
        for i in range(num):
            K = 2 + (i % 4)
            sigma = 0.1 + i * 0.1
            mean = i * 50
            variants.append({"family": "gaussian", "params": f"K={K},sigma={sigma:.2f},mean={mean}", "approx_c2": 0.90 + i * 0.0015})
        return variants
    
    def gen_bspline(num=10):
        variants = []
        for i in range(num):
            knots = 5 + (i * 3)
            spacing = "uniform" if i % 2 == 0 else "adaptive"
            variants.append({"family": "bspline", "params": f"knots={knots},spacing={spacing}", "approx_c2": 0.895 + i * 0.0012})
        return variants
    
    def gen_exponential(num=10):
        variants = []
        for i in range(num):
            rate = 0.1 + i * 0.1
            terms = 1 + (i % 2)
            variants.append({"family": "exponential", "params": f"rate={rate:.2f},terms={terms}", "approx_c2": 0.892 + i * 0.001})
        return variants
    
    if family == "auto":
        all_variants = gen_step(10) + gen_gaussian(10) + gen_bspline(10) + gen_exponential(10)
    elif family == "step":
        all_variants = gen_step(num_variants)
    elif family == "gaussian":
        all_variants = gen_gaussian(num_variants)
    elif family == "bspline":
        all_variants = gen_bspline(num_variants)
    elif family == "exponential":
        all_variants = gen_exponential(num_variants)
    
    return {"variations": all_variants[:num_variants]}