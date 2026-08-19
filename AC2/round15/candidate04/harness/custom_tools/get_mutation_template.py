def run(ctx, args):
    import random
    random.seed(42)
    template_idx = args.get("template_idx", 0)
    
    templates = [
        {
            "family": "gaussian_mixture",
            "rationale": "Smooth multi-peaked Gaussian mixtures create better L2/∞ ratios than steps."
        },
        {
            "family": "piecewise_linear",
            "rationale": "Piecewise linear with optimized vertices creates structured patterns."
        },
        {
            "family": "oscillatory_decay",
            "rationale": "Oscillatory functions with decay create structured convolutions."
        },
        {
            "family": "asymmetric_multi_level",
            "rationale": "Asymmetric multi-level steps break symmetry for better ratios."
        }
    ]
    
    template = templates[template_idx % len(templates)]
    return {
        "family": template["family"],
        "template_idx": template_idx,
        "rationale": template["rationale"],
        "edit_instruction": "Replace the seed's EVOLVE-BLOCK with a complete implementation of this function family using jax.numpy. Ensure the code is valid Python."
    }
