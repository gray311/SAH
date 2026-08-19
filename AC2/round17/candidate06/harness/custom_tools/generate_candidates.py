def run(ctx, args):
    import random
    random.seed(42)
    proposals = []
    
    # Family 1: Gaussian mixtures (smooth, multi-peaked)
    proposals.append({
        "family": "gaussian_mixture",
        "description": "Weighted sum of Gaussians: f(x) = sum w_i * exp(-((x-mu_i)^2)/(2*sigma_i^2))",
        "code_snippet": "import jax.numpy as jnp\nimport jax\n\nf_values = jnp.linspace(-4, 4, 600)\nmu = jnp.array([0.0, 1.5, -1.2, 2.0])\nsigma = jnp.array([0.6, 0.8, 0.7, 0.9])\nweights = jnp.array([0.25, 0.25, 0.25, 0.25])\nf = weights[None,:] @ jnp.exp(-((f_values[:,None] - mu)[None,:,:])**2 / (2*sigma**2[None,:]))\nf = jnp.maximum(f, 1e-6)"
    })
    
    # Family 2: B-spline basis (flexible smooth transitions)
    proposals.append({
        "family": "bspline",
        "description": "B-spline with optimized control points and knots",
        "code_snippet": "import jax.numpy as jnp\nfrom scipy.interpolate import splev, splrep\n\nn_control = 40\nknots = jnp.linspace(-3, 3, 20)\ncontrols = jnp.random.uniform(0.8, 2.0, n_control)\ncontrols = jax.nn.softplus(controls)\nf_values = jnp.linspace(-3, 3, 600)\nfit = splev(f_values, knots, s=0, k=3, dx=1, w=controls)\nf = jnp.maximum(f, 1e-6)"
    })
    
    # Family 3: Piecewise-linear with optimized vertices
    proposals.append({
        "family": "piecewise_linear",
        "description": "Linear segments connecting vertices, optimized for C2",
        "code_snippet": "import jax.numpy as jnp\n\nf_values = jnp.linspace(-3, 3, 600)\nn_vertices = 35\nvertices = jnp.linspace(-2.5, 2.5, n_vertices)\nheights = 0.8 + 0.7 * jnp.exp(-((vertices[:n_vertices//2] - 0.3)**2 + (vertices[n_vertices//2:] + 0.5)**2) / 2)\nf = jnp.piecewise(f_values, [(f_values <= x) for x in vertices[:-1]], \
    [lambda x, v, h: h * (x - v) / (x[0] - v) for v, h in zip(vertices[:-1], heights)])\nf = jnp.maximum(f, 1e-6)"
    })
    
    # Family 4: Oscillatory with decay
    proposals.append({
        "family": "oscillatory_decay",
        "description": "f(x) = (1 + alpha * cos(beta*x)) * exp(-gamma*|x|)",
        "code_snippet": "import jax.numpy as jnp\nimport jax\n\nf_values = jnp.linspace(-5, 5, 800)\nalpha = 0.35\nbeta = 5.0\ngamma = 0.75\nf = (1 + alpha * jnp.cos(beta * f_values)) * jnp.exp(-gamma * jnp.abs(f_values))\nf = jnp.maximum(f, 1e-6)"
    })
    
    # Family 5: Multi-level improved step with asymmetry
    proposals.append({
        "family": "multi_level_asymmetric",
        "description": "Multi-level step with optimized heights and asymmetric structure",
        "code_snippet": "import jax.numpy as jnp\nimport jax\n\nf_values = jnp.linspace(-3, 3, 600)\nn = len(f_values)\nlevels = jnp.array([0.0, 1.35, 1.85, 1.45, 0.95, 0.0])\npositions = jnp.array([0.0, 0.15, 0.35, 0.55, 0.75, 1.0])\nf = jnp.zeros_like(f_values)\nfor i in range(len(positions) - 1):\n    start = int(positions[i] * n)\n    end = int(positions[i+1] * n)\n    if i == 0 or i == len(positions) - 2:\n        f = f.at[start:end].set(levels[i])\n    else:\n        f = f.at[start:end].set(levels[i] + 0.15 * jnp.sin(2 * jnp.pi * (f_values[start:end] - positions[i]) / (positions[i+1] - positions[i])))\nf = jnp.maximum(f, 1e-6)"
    })
    
    # Family 6: Hybrid step-spline (best of both worlds)
    proposals.append({
        "family": "hybrid_step_spline",
        "description": "Step-function base with smooth spline transitions",
        "code_snippet": "import jax.numpy as jnp\nimport jax\n\nf_values = jnp.linspace(-3, 3, 600)\nn = len(f_values)\n# Step regions with smooth transitions\ntransitions = jnp.array([-2.5, -0.5, 0.5, 2.5])\nheights = jnp.array([0.0, 1.40, 1.90, 1.30, 0.0])\nf = jnp.zeros_like(f_values)\nfor i in range(len(transitions) - 1):\n    if i == 0:\n        t0, t1 = transitions[i], transitions[i+1]\n        f = f.at[(t0*n):int(t1*n)].set(heights[i+1] * jnp.exp(-((f_values[(t0*n):int(t1*n)] - (t0+t1)*n/2)**2 / (2*0.8**2))))\n    elif i == 3:\n        t0, t1 = transitions[i], transitions[i+1]\n        f = f.at[(t0*n):int(t1*n)].set(heights[i+1] * jnp.exp(-((f_values[(t0*n):int(t1*n)] - (t0+t1)*n/2)**2 / (2*0.8**2))))\n    else:\n        f = f.at[int(t0*n):int(t1*n)].set(heights[i+1])\nf = jnp.maximum(f, 1e-6)"
    })
    
    return {
        "proposals": proposals,
        "note": "Use probe_solution to rank these quickly (3-5 probes each). Evaluate top 3-4 with evaluate_solution. Then refine winners in Phase 2."
    }