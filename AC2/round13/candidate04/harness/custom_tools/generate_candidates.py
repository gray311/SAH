def run(ctx, args):
    import random
    random.seed(42)
    proposals = []

    # Family 1: Gaussian mixtures with varied parameters
    proposals.append({
        "family": "gaussian_mixture",
        "description": "Weighted sum of Gaussians with varied means and widths",
        "code_snippet": "import jax.numpy as jnp\\nimport jax\\n\\nf_values = jnp.linspace(-4, 4, 800)\\nnum_gauss = jnp.random.uniform(3, 8)\\nmu = jnp.sort(jnp.random.uniform(-3, 3, num_gauss))\\nsigma = 0.3 + jnp.random.uniform(0.2, 0.8, num_gauss)\\nweights = jnp.random.uniform(0.1, 0.5, num_gauss)\\nf = weights[None,:] @ jnp.exp(-((f_values[:,None] - mu)[None,:,:])**2 / (2*sigma**2[None,:]))\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Smooth multi-peaked functions may achieve better norm ratios"
    })

    # Family 2: B-spline with optimized knots
    proposals.append({
        "family": "bspline_knot_optimized",
        "description": "B-spline with optimized knot placement for shape control",
        "code_snippet": "import jax.numpy as jnp\\nimport jax\\nfrom scipy.interpolate import splev, splrep\\n\\nn_knots = jnp.linspace(-3, 3, 15)\\nn_ctrl = 40\\ncontrols = jnp.exp(jnp.random.uniform(0.1, 1.5, n_ctrl))\\ncontrols = controls / jnp.max(controls)\\nf_values = jnp.linspace(-3, 3, 600)\\ntry:\\n    fit = splev(f_values, n_knots, s=0, k=3, w=controls)\\n    f = jnp.maximum(fit, 1e-6)\\nexcept:\\n    f = jnp.ones_like(f_values) * 0.8",
        "rationale": "Splines offer flexible smooth transitions with knot optimization"
    })

    # Family 3: Oscillatory with exponential decay
    proposals.append({
        "family": "oscillatory_decay",
        "description": "f(x) = (1 + alpha*cos(beta*x)) * exp(-gamma*|x|)",
        "code_snippet": "import jax.numpy as jnp\\nf_values = jnp.linspace(-6, 6, 1000)\\nalpha = jnp.random.uniform(0.2, 0.8)\\nbeta = 2.0 + jnp.random.uniform(0, 4)\\ngamma = 0.3 + jnp.random.uniform(0.1, 0.6)\\nf = (1 + alpha * jnp.cos(beta * f_values)) * jnp.exp(-gamma * jnp.abs(f_values))\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Oscillatory structures create interesting convolution patterns"
    })

    # Family 4: Piecewise-linear with optimized vertices
    proposals.append({
        "family": "piecewise_linear_optimized",
        "description": "Linear segments with optimized vertex heights",
        "code_snippet": "import jax.numpy as jnp\\nf_values = jnp.linspace(-3, 3, 600)\\nn_vtx = jnp.random.uniform(15, 35)\\nvtx_pos = jnp.linspace(-2.5, 2.5, int(n_vtx))\\nheights = 0.3 + jnp.random.uniform(0.4, 1.5, len(vtx_pos))\\nf = jnp.piecewise(f_values, [(f_values <= x) for x in vtx_pos[:-1]], [lambda x: heights[i] * (x - vtx_pos[i]) / (vtx_pos[i+1] - vtx_pos[i]) for i in range(len(vtx_pos)-1)])\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Piecewise-linear can approximate optimal shapes with smooth transitions"
    })

    # Family 5: Multi-level asymmetric steps
    proposals.append({
        "family": "multi_level_asymmetric",
        "description": "Asymmetric multi-level step with varied heights",
        "code_snippet": "import jax.numpy as jnp\\nf_values = jnp.linspace(-3, 3, 600)\\nn = len(f_values)\\nnum_levels = jnp.random.randint(3, 6)\\npositions = jnp.linspace(0.1, 0.9, num_levels + 1)\\nheights = 0.5 + jnp.random.uniform(0.3, 1.8, num_levels)\\nf = jnp.zeros_like(f_values)\\nfor i in range(num_levels):\\n    start = int(positions[i] * n)\\n    end = int(positions[i+1] * n)\\n    f = f.at[start:end].set(heights[i])\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Asymmetric multi-level steps may beat symmetric patterns"
    })

    return {
        "proposals": proposals,
        "note": "Call probe_solution for each proposal before full evaluation."
    }