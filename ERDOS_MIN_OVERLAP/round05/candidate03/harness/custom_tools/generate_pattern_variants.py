def run(ctx, args):
    # Generate diverse pattern suggestions based on task knowledge
    patterns = [
        {"name": "symmetric_single_pulse", "desc": "h=1 on [a, a+1], 0 elsewhere", "params": {"a_suggested": [0., 0.2, 0.5, 0.8, 1.0]}},
        {"name": "asymmetric_two_pulses", "desc": "Two pulses with asymmetric placement", "params": {"width1": "0.6", "width2": "0.4", "gap": "0.0-1.0"}},
        {"name": "sin_cos_blend", "desc": "Sinusoidal with cosine modulation", "params": {"freq1": 1.0, "freq2": 2.0, "amp_scale": "0.5-2.0"}},
        {"name": "region_tripartite", "desc": "Three regions with different heights", "params": {"regions": "0-0.67, 0.67-1.33, 1.33-2.0", "heights": "low, medium, high"}},
        {"name": "boundary_sharpening", "desc": "Refine existing gradient solution into sharp steps", "params": {"threshold": "sigmoid(10*val)"}},
    ]
    return {
        "patterns": patterns,
        "strategy": "Systematically test each pattern family, probe all, evaluate best",
        "budget_efficient": True
    }
