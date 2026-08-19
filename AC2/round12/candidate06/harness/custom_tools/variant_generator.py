def run(ctx, args):
    import random
    random.seed(42)
    variants = []
    arch_types = ["narrow_spike", "wide_plateau", "bimodal", "trimodal", "smooth_gaussian"]
    for arch in arch_types:
        variants.append({"arch": arch, "params": {"width": 0.2 if "narrow" in arch else 0.7, "height": 1.4 if "low" in arch else 2.0}})
    variants.append({"arch": "extreme", "params": {"width": 0.15, "height": 3.0}})
    return {"variants": variants}
