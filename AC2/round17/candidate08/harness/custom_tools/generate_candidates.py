def run(ctx, args):
    import random
    random.seed(42)
    proposals = []
    
    # Family 1: Gaussian mixtures
    proposals.append({
        "family": "gaussian_mixture",
        "description": "Weighted sum of Gaussians with optimized parameters",
        "code_snippet": "import jax.numpy as jnp\\nimport jax\\n\\nf_values = jnp.linspace(-4, 4, 600)\\nmu = jnp.array([0.0, 1.5, -1.5])\\nsigma = jnp.array([0.8, 0.6, 0.7])\\nweights = jnp.array([0.35, 0.35, 0.30])\\nf = weights[None,:] @ jnp.exp(-((f_values[:,None] - mu)[None,:,:])**2 / (2*sigma**2[None,:]))\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Smooth multi-peaked functions may achieve better L2/Infinity ratio than sharp steps"
    })
    
    # Family 2: B-spline basis
    proposals.append({
        "family": "bspline",
        "description": "B-spline with optimized control points and knots",
        "code_snippet": "import jax.numpy as jnp\\nfrom scipy.interpolate import splev, splrep\\n\\nn_control = 50\\nknots = jnp.linspace(-3, 3, 20)\\ncontrols = jnp.random.uniform(0.5, 2.0, n_control)\\ncontrols = jax.nn.softplus(controls)\\nf_values = jnp.linspace(-3, 3, 600)\\nfit = splev(f_values, knots, s=0, k=3, dx=1, w=controls)\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Splines offer flexible smooth transitions; optimize control points for C2"
    })
    
    # Family 3: Piecewise-linear
    proposals.append({
        "family": "piecewise_linear",
        "description": "Linear segments connecting vertices, optimized for shape",
        "code_snippet": "import jax.numpy as jnp\\n\\nf_values = jnp.linspace(-3, 3, 600)\\nn_vertices = 30\\nvertices = jnp.linspace(-2, 2, n_vertices)\\nheights = 0.5 + 0.7 * jnp.abs(jnp.sin(jnp.linspace(0, 2*jnp.pi, n_vertices)))\\nf = jnp.piecewise(f_values, [(f_values <= x) for x in vertices[:-1]], \\\n    lambda x, i: heights[i] * (x - vertices[i]) / (vertices[i+1] - vertices[i]) if x > vertices[i] else 0.0)\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Piecewise-linear can mimic step functions with smoother transitions, potentially better norms"
    })
    
    # Family 4: Oscillatory with decay
    proposals.append({
        "family": "oscillatory_decay",
        "description": "Oscillatory function with exponential decay",
        "code_snippet": "import jax.numpy as jnp\\n\\nf_values = jnp.linspace(-5, 5, 800)\\nalpha = 0.5\\nbeta = 5.0\\ngamma = 0.7\\nf = (1 + alpha * jnp.cos(beta * f_values)) * jnp.exp(-gamma * jnp.abs(f_values))\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Oscillatory functions create structured convolutions; decay ensures integrability"
    })
    
    # Family 5: Multi-level improved step
    proposals.append({
        "family": "multi_level_improved",
        "description": "Multi-level step with optimized heights and asymmetric structure",
        "code_snippet": "import jax.numpy as jnp\\nimport jax\\n\\nf_values = jnp.linspace(-3, 3, 600)\\nn = len(f_values)\\nlevels = [0.8, 1.8, 2.2, 1.8, 1.2, 0.8]\\npositions = jnp.array([0.10, 0.25, 0.40, 0.60, 0.75, 0.90])\\nf = jnp.zeros(len(f_values))\\nfor i in range(len(positions) - 1):\\n    start = int(positions[i] * n)\\n    end = int(positions[i+1] * n)\\n    f = f.at[start:end].set(levels[i])\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Refined multi-level steps with asymmetric heights may beat simple step patterns"
    })
    
    # Family 6: Asymmetric exponential
    proposals.append({
        "family": "asymmetric_exponential",
        "description": "Asymmetric exponential decay with different rates",
        "code_snippet": "import jax.numpy as jnp\\n\\nf_values = jnp.linspace(-4, 4, 700)\\ngamma_left = 0.5\\ngamma_right = 0.8\\nf = jnp.where(f_values < 0, jnp.exp(gamma_left * f_values), jnp.exp(-gamma_right * f_values))\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Asymmetric decay may reduce L_infinity while maintaining L2 norm"
    })
    
    return {
        "proposals": proposals,
        "note": "Use analyze_convolution to estimate structure, then probe_solution to rank before full evaluation."
    }
