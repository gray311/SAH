def run(ctx, args):
    import random
    random.seed(42)
    import numpy as np
    proposals = []
    
    # Family 1: Gaussian mixtures - smooth multi-peaked functions
    proposals.append({
        "family": "gaussian_mixture",
        "description": "Weighted sum of Gaussians: f(x) = sum w_i * exp(-((x-mu_i)^2)/(2*sigma_i^2))",
        "code_snippet": "import jax.numpy as jnp\\nimport jax\\n\\nf_values = jnp.linspace(-5, 5, 800)\\nmu = jnp.array([0.0, 1.0, -1.0, 0.5, -0.5])\\nsigma = jnp.array([0.8, 0.6, 0.7, 0.5, 0.5])\\nweights = jnp.array([0.25, 0.20, 0.20, 0.15, 0.15])\\ngaussians = jnp.exp(-jnp.sum((f_values[:, None] - mu)[None, :] ** 2 / (2 * sigma ** 2), axis=1))\\nf = weights * gaussians\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Smooth multi-peaked functions create bell-shaped convolutions that may optimize the L2/inf ratio differently than sharp steps."
    })
    
    # Family 2: Oscillatory with decay - structured multi-peak convolutions
    proposals.append({
        "family": "oscillatory_decay",
        "description": "f(x) = (1 + alpha*cos(beta*x)) * exp(-gamma*abs(x)) - creates oscillatory convolution",
        "code_snippet": "import jax.numpy as jnp\\nimport jax\\n\\nf_values = jnp.linspace(-6, 6, 1000)\\nalpha = 0.4\\nbeta = 5.0\\ngamma = 0.9\\noscillatory = 1 + alpha * jnp.cos(beta * f_values)\\ndecay = jnp.exp(-gamma * jnp.abs(f_values))\\nf = oscillatory * decay\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Oscillatory functions create structured convolutions with multiple peaks, potentially creating favorable L2/inf ratios."
    })
    
    # Family 3: Asymmetric multi-peaked - strategic peak placement
    proposals.append({
        "family": "asymmetric_multi_peak",
        "description": "Multi-peaked function with asymmetric heights and positions for strategic convolution overlap",
        "code_snippet": "import jax.numpy as jnp\\nimport jax\\n\\nf_values = jnp.linspace(-4, 4, 700)\\nn = len(f_values)\\n# Three peaks with asymmetric heights and positions\\nf = jnp.zeros(n)\\nf = f.at[int(0.20*n):int(0.35*n)].set(1.8)  # Left peak\\nf = f.at[int(0.35*n):int(0.60*n)].set(1.2)  # Middle plateau\\nf = f.at[int(0.60*n):int(0.80*n)].set(1.6)  # Right peak (taller)\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Asymmetric multi-peaked functions may create convolution patterns with better L2/inf balance than symmetric step functions."
    })
    
    # Family 4: B-spline basis - flexible smooth transitions
    proposals.append({
        "family": "bspline_smooth",
        "description": "B-spline with optimized control points and knots for smooth transitions",
        "code_snippet": "import jax.numpy as jnp\\nfrom scipy.interpolate import splev, splrep\\n\\nf_values = jnp.linspace(-4, 4, 800)\\nn_control = 40\\nknots = jnp.linspace(-4, 4, 30)\\ncontrols = jnp.random.uniform(0.8, 1.5, n_control)\\ncontrols = jax.nn.softplus(controls - 1.0) + 0.5  # Ensure positive\\ntry:\\n    fit = splev(f_values, knots, s=0, k=3, dx=1, w=controls)\\n    f = jnp.maximum(fit, 1e-6)\\nexcept:\\n    f = jnp.ones_like(f_values) * 1.0",
        "rationale": "B-splines offer flexible smooth transitions; optimizing control points may find architectures with favorable convolution properties."
    })
    
    # Family 5: Piecewise-linear with optimized heights
    proposals.append({
        "family": "piecewise_linear_smooth",
        "description": "Piecewise-linear function with smooth transitions and optimized vertex heights",
        "code_snippet": "import jax.numpy as jnp\\n\\nf_values = jnp.linspace(-4, 4, 700)\\nn_vertices = 25\\nvertices = jnp.linspace(-3.5, 3.5, n_vertices)\\n# Heights with smooth transitions (avoid sharp steps)\\nheights = 1.0 + 0.5 * jnp.sin(jnp.linspace(0, 4*jnp.pi, n_vertices))\\nf = jnp.piecewise(f_values, \\n                  [lambda x: i == jnp.searchsorted(vertices, x) for i in range(n_vertices)], \\n                  [lambda x: (heights[i] + (heights[i+1]-heights[i])*(x-vertices[i])/(vertices[i+1]-vertices[i])) for i in range(n_vertices-1)])\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Piecewise-linear with smooth transitions may capture intermediate properties between step and smooth functions."
    })
    
    return {
        "proposals": proposals,
        "note": "Each proposal implements a COMPLETE function from scratch. Use evaluate_solution to test them."
    }
