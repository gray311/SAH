def run(ctx, args):
    import random
    import numpy as np
    random.seed(42)
    f_values = np.linspace(-3, 3, 600)
    n = len(f_values)
    
    mutation = args.get("mutation_type", "height_adjust")
    intensity = args.get("intensity", 0.15)
    
    # Base: simple symmetric step (guaranteed to work)
    f = np.zeros(n)
    center = n // 2
    width = int(n * (0.4 + random.uniform(-intensity, intensity)))
    height = 1.0 + random.uniform(-intensity, intensity)
    
    start = max(0, center - width // 2)
    end = min(n, center + width // 2)
    f[start:end] = height
    
    # Add asymmetry if mutation suggests
    if mutation in ["add_level", "recenter"]:
        offset = int(n * intensity * 0.3)
        f[offset:offset+width//3] = height * 1.2
    
    # Ensure positivity
    f = np.maximum(f, 1e-6)
    
    return {
        "family": "step_variant",
        "mutation": mutation,
        "intensity": intensity,
        "code": f"import numpy as np\nf_values = np.linspace(-3, 3, 600)\nf = np.zeros(600)\ncenter = 300\nwidth = {width}\nheight = {height:.3f}\nstart = max(0, center - width // 2)\nend = min(600, center + width // 2)\nf[start:end] = height\nf = np.maximum(f, 1e-6)",
        "note": "Simple step variant - guaranteed to run. Use probe_solution to evaluate."
    }