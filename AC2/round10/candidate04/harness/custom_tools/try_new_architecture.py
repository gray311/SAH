def run(ctx, args):
    import random
    random.seed(42 + hash("architecture"))
    
    arch_types = ["asymmetric_bimodal", "trimodal_plateau", "logarithmic_steps", "narrow_peaked_wide", "flat_top_asymmetric"]
    arch_type = random.choice(arch_types)
    num_intervals = random.choice([300, 450, 600, 750, 900])
    
    templates = {
        "asymmetric_bimodal": """
            f = jnp.zeros(n)
            f = f.at[int(0.1*n):int(0.35*n)].set({h1})
            f = f.at[int(0.45*n):int(0.75*n)].set({h2})
            f = f.at[int(0.8*n):int(0.95*n)].set({h3})
        """,
        "trimodal_plateau": """
            f = jnp.zeros(n)
            f = f.at[int(0.08*n):int(0.22*n)].set({h1})
            f = f.at[int(0.22*n):int(0.55*n)].set({h2})
            f = f.at[int(0.55*n):int(0.78*n)].set({h1})
        """,
        "logarithmic_steps": """
            f = jnp.zeros(n)
            steps = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
            for i, pos in enumerate(steps):
                start = int(pos * n * 0.9)
                end = int((pos + 0.1) * n * 0.9)
                f = f.at[start:end].set({h})
        """,
        "narrow_peaked_wide": """
            f = jnp.zeros(n)
            f = f.at[int(0.25*n):int(0.32*n)].set({h_peak})
            f = f.at[int(0.32*n):int(0.38*n)].set({h_mid})
            f = f.at[int(0.62*n):int(0.68*n)].set({h_mid})
            f = f.at[int(0.68*n):int(0.75*n)].set({h_peak})
        """,
        "flat_top_asymmetric": """
            f = jnp.zeros(n)
            f = f.at[int(0.05*n):int(0.2*n)].set({h_left})
            f = f.at[int(0.2*n):int(0.5*n)].set({h_top})
            f = f.at[int(0.5*n):int(0.75*n)].set({h_right})
            f = f.at[int(0.75*n):int(0.9*n)].set({h_left})
        """
    }
    
    template = templates[arch_type]
    base_h = 1.0
    h1, h2, h3 = base_h * 1.2, base_h * 1.5, base_h * 1.1
    h = base_h * 1.3
    h_peak = base_h * 1.8
    h_mid = base_h * 1.2
    h_left = base_h * 1.0
    h_top = base_h * 1.6
    h_right = base_h * 1.4
    
    code = template.format(h1=h1, h2=h2, h3=h3, h=h, h_peak=h_peak, h_mid=h_mid, h_left=h_left, h_top=h_top, h_right=h_right, n=num_intervals)
    return {"arch_type": arch_type, "num_intervals": num_intervals, "code": code}
