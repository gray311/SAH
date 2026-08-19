def run(ctx, args):
    func_class = args.get("function_class", "cosine_variant")
    params = args.get("parameters", {})
    rationale = args.get("rationale", "")
    
    implementations = {
        "cosine_variant": "def _cosine_variant(n, freq=1.5, amp=1.2, phase=0.0):\n    x = jnp.linspace(0, 2*jnp.pi, n)\n    f = amp * jnp.cos(freq * x + phase)\n    f = jax.nn.relu(f)\n    return f\n",
        "gaussian_mixture": "def _gaussian_mixture(n, num_components=3, scale_factor=1.0):\n    x = jnp.linspace(0, 2.0, n)\n    f = jnp.zeros(n)\n    for i in range(num_components):\n        center = (i + 1) / (num_components + 1)\n        amp = 0.3 + i * 0.25 * scale_factor\n        sigma = 0.15 + i * 0.05 * scale_factor\n        f = f + amp * jnp.exp(-((x - center) / sigma)**2)\n    return jnp.clip(f, 0, None)\n",
        "spline_piecewise": "def _spline_piecewise(n, num_knots=5):\n    x = jnp.linspace(0, 2.0, n)\n    knots = jnp.linspace(0.0, 2.0, num_knots + 2)\n    values = jnp.zeros(num_knots + 1)\n    for i in range(num_knots):\n        left = knots[i] if i > 0 else 0.0\n        right = knots[i + 1] if i < num_knots else 2.0\n        if right > left:\n            height = 0.5 + 0.1 * i\n            values = values.at[i].set(height)\n    f = jnp.zeros(n)\n    for i in range(num_knots):\n        if i < num_knots - 1:\n            left = knots[i]\n            right = knots[i + 1]\n            height_left = values[i]\n            height_right = values[i + 1]\n            if right > left:\n                interp = jnp.where((x >= left) & (x < right), height_left + (height_right - height_left) * (x - left) / (right - left), jnp.zeros(n))\n                f = f + interp\n    return jnp.clip(f, 0, None)\n",
        "asymmetric_multi_peak": "def _asymmetric_multi_peak(n, peaks=4, scale=1.2):\n    x = jnp.linspace(0, 2.0, n)\n    f = jnp.zeros(n)\n    for i in range(peaks):\n        center = (i + 0.5) / peaks\n        width = 0.15 + 0.1 * (i % 2)\n        height = 0.6 + 0.2 * (i + 1) * scale\n        f = f + height * jnp.exp(-((x - center) / (width + 0.05))**2)\n    return jnp.clip(f, 0, None)\n"
    }
    
    impl = implementations.get(func_class, "Custom implementation needed")
    return {
        "function_class": func_class,
        "implementation": impl,
        "parameters_to_tune": list(params.keys()),
        "rationale": rationale,
        "next_steps": "Replace the function creation code with this function, then evaluate"
    }
