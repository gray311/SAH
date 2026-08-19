def run(ctx, args):
    import random
    random.seed(42)
    proposals = []
    
    # Family 1: Gaussian mixtures
    proposals.append({
        "family": "gaussian_mixture",
        "description": "Weighted sum of Gaussians: f(x) = sum w_i * exp(-((x-mu_i)^2)/(2*sigma_i^2))",
        "code_snippet": "import jax.numpy as jnp\\nimport jax\\n\\nf_values = jnp.linspace(-4, 4, 800)\\nmu = jnp.array([0.0, 1.5, -1.5])\\nsigma = jnp.array([0.6, 0.8, 0.7])\\nweights = jnp.array([0.35, 0.35, 0.30])\\nf = weights[None,:] @ jnp.exp(-((f_values[:,None] - mu)[None,:,:])**2 / (2*sigma**2[None,:]))\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Multi-modal smooth functions may achieve better ||f★f||2^2 / ||f★f||_∞ ratio"
    })
    
    # Family 2: B-spline basis
    proposals.append({
        "family": "bspline",
        "description": "B-spline with optimized control points and knots",
        "code_snippet": "import jax.numpy as jnp\\nfrom scipy.interpolate import splev, splrep\\n\\nn_control = 40\\nknots = jnp.linspace(-2, 2, 30)\\ncontrols = jnp.random.uniform(0.8, 2.0, n_control)\\ncontrols = jax.nn.softplus(controls)\\nf_values = jnp.linspace(-3, 3, 600)\\nfit = splev(f_values, knots, s=0, k=3, dx=1, w=controls)\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Splines offer flexible smooth transitions; optimize control points for C2"
    })
    
    # Family 3: Oscillatory with decay
    proposals.append({
        "family": "oscillatory_decay",
        "description": "f(x) = (1 + alpha * cos(beta*x)) * exp(-gamma*|x|)",
        "code_snippet": "import jax.numpy as jnp\\nimport jax\\n\\nf_values = jnp.linspace(-6, 6, 1000)\\nalpha = 0.4\\nbeta = 5.0\\ngamma = 0.9\\nf = (1 + alpha * jnp.cos(beta * f_values)) * jnp.exp(-gamma * jnp.abs(f_values))\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Oscillatory functions create structured convolutions; decay ensures integrability"
    })
    
    # Family 4: Multi-level sharp
    proposals.append({
        "family": "multi_level_sharp",
        "description": "Multi-level step with optimized heights and asymmetric structure",
        "code_snippet": "import jax.numpy as jnp\\nimport jax\\n\\nf_values = jnp.linspace(-3, 3, 800)\\nn = len(f_values)\\nlevels = jnp.array([0.6, 1.8, 2.5, 1.9, 0.7, 1.4])\\npositions = jnp.array([0.08, 0.25, 0.45, 0.60, 0.75, 0.90])\\nf = jnp.zeros(n)\\nfor i in range(len(positions) - 1):\\n    start = int(positions[i] * n)\\n    end = int(positions[i+1] * n)\\n    f = f.at[start:end].set(levels[i])\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Refined multi-level steps with asymmetric heights may beat simple step patterns"
    })
    
    # Family 5: Piecewise-linear
    proposals.append({
        "family": "piecewise_linear",
        "description": "Linear segments connecting vertices, optimized for shape",
        "code_snippet": "import jax.numpy as jnp\\n\\nf_values = jnp.linspace(-3, 3, 600)\\nn_vertices = 25\\nvertices = jnp.linspace(-2.5, 2.5, n_vertices)\\nheights = 0.6 + 0.7 * jnp.abs(jnp.sin(jnp.linspace(0, 3*jnp.pi, n_vertices)))\\nf = jnp.piecewise(f_values, [(f_values <= x) for x in vertices[:-1]], [lambda x: heights[i] for i in range(n_vertices-1)])\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Piecewise-linear can mimic step functions with smoother transitions"
    })
    
    return {
        "proposals": proposals,
        "note": "Use probe_solution to rank these quickly before full evaluation."
    }
