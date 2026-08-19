def run(ctx, args):
    import random
    random.seed(42)
    import numpy as np
    proposals = []
    
    # Family 1: Gaussian mixtures
    proposals.append({
        "family": "gaussian_mixture",
        "description": "Weighted sum of Gaussians: f(x) = sum w_i * exp(-((x-mu_i)^2)/(2*sigma_i^2))",
        "code_snippet": "import jax.numpy as jnp\nimport jax\n\nf_values = jnp.linspace(-4, 4, 600)\nmu = jnp.array([0.0, 1.0, -1.0])\nsigma = jnp.array([0.6, 0.8, 0.7])\nweights = jnp.array([0.35, 0.35, 0.30])\nf = weights[None,:] @ jnp.exp(-((f_values[:,None] - mu)[None,:,:])**2 / (2*sigma**2[None,:]))\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Smooth functions may achieve better ||f★f||_2^2 / ||f★f||_∞ ratio than sharp steps"
    })
    
    # Family 2: B-spline basis
    proposals.append({
        "family": "bspline",
        "description": "B-spline with optimized control points and knots",
        "code_snippet": "import jax.numpy as jnp\nimport jax\nfrom scipy.interpolate import splev, splrep\n\nn_control = 50\nknots = jnp.linspace(-1.5, 1.5, 30)\ncontrols = jnp.random.uniform(0.8, 2.0, n_control)\ncontrols = jax.nn.softplus(controls)\nf_values = jnp.linspace(-4, 4, 600)\nfit = splev(f_values, knots, k=3, dx=1, w=controls)\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Splines offer flexible smooth transitions; optimize control points for C2"
    })
    
    # Family 3: Piecewise-linear
    proposals.append({
        "family": "piecewise_linear",
        "description": "Linear segments connecting vertices, optimized for shape",
        "code_snippet": "import jax.numpy as jnp\n\nf_values = jnp.linspace(-3, 3, 600)\nn_vertices = 25\nvertices = jnp.linspace(-2, 2, n_vertices)\nheights = 0.5 + 0.5 * jnp.sin(jnp.linspace(0, 2*jnp.pi, n_vertices))\nf = jnp.piecewise(f_values, [None], [lambda x: jnp.interp(x, vertices, heights)])\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Piecewise-linear can mimic step functions with smoother transitions, potentially better norms"
    })
    
    # Family 4: Oscillatory with decay
    proposals.append({
        "family": "oscillatory_decay",
        "description": "f(x) = (1 + alpha * cos(beta*x)) * exp(-gamma*|x|)",
        "code_snippet": "import jax.numpy as jnp\nimport jax\n\nf_values = jnp.linspace(-5, 5, 800)\nalpha = 0.4\nbeta = 3.5\ngamma = 0.9\nf = (1 + alpha * jnp.cos(beta * f_values)) * jnp.exp(-gamma * jnp.abs(f_values))\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Oscillatory functions create structured convolutions; decay ensures integrability"
    })
    
    # Family 5: Multi-level improved step
    proposals.append({
        "family": "multi_level_improved",
        "description": "Multi-level step with optimized heights and asymmetric structure",
        "code_snippet": "import jax.numpy as jnp\nimport jax\n\nf_values = jnp.linspace(-3, 3, 600)\nn = len(f_values)\nlevels = [0.6, 1.3, 2.1, 1.4, 0.8]\npositions = jnp.array([0.12, 0.32, 0.48, 0.68, 0.85])\nf = f_values\nfor i in range(len(positions) - 1):\n    start = int(positions[i] * n)\n    end = int(positions[i+1] * n)\n    f = f.at[start:end].set(levels[i])\nf = jnp.maximum(f, 0)",
        "rationale": "Refined multi-level steps with asymmetric heights may beat simple step patterns"
    })
    
    # Family 6: Exponential decay mixture
    proposals.append({
        "family": "exponential_decay",
        "description": "Mixture of exponentials with different scales",
        "code_snippet": "import jax.numpy as jnp\nimport jax\n\nf_values = jnp.linspace(-6, 6, 700)\nweights = jnp.array([0.4, 0.35, 0.25])\nscales = jnp.array([1.5, 0.8, 2.2])\nf = weights[None,:] @ jnp.exp(-jnp.abs((f_values[:,None]) / scales[None,:]))\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Exponential mixtures can create smooth, unimodal functions with controlled tails"
    })
    
    return {
        "proposals": proposals,
        "note": "Use probe_solution to rank these quickly before full evaluation. You have 30 probes!"
    }
