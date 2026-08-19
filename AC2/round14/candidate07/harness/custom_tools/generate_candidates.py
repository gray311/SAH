def run(ctx, args):
    import random
    random.seed(42)
    proposals = []
    
    proposals.append({
        "family": "gaussian_mixture",
        "description": "Weighted sum of Gaussians at different locations - creates multi-modal function",
        "code_snippet": "import jax.numpy as jnp\\nimport jax\\n\\nf_values = jnp.linspace(-5, 5, 800)\\nmu = jnp.array([-2.5, 0.0, 2.5])\\nsigma = jnp.array([0.8, 0.6, 0.8])\\nweights = jnp.array([0.35, 0.30, 0.35])\\nf = weights[None,:] @ jnp.exp(-((f_values[:,None] - mu)[None,:,:])**2 / (2*sigma**2[None,:]))\\nf = jnp.maximum(f, 1e-8)",
        "rationale": "Separated modes create convolution interference that can flatten peaks"
    })
    
    proposals.append({
        "family": "ramp_function",
        "description": "Triangular pulse - smooth transition reduces convolution peak concentration",
        "code_snippet": "import jax.numpy as jnp\\n\\nf_values = jnp.linspace(-5, 5, 800)\\npeak_loc = 0.0\\npeak_height = 2.0\\nwidth = 8.0\\ndist = jnp.abs(f_values - peak_loc)\\nf = jnp.where(dist <= width/2, peak_height * (1 - 2*dist/width), 0.0)\\nf = jnp.maximum(f, 1e-8)",
        "rationale": "Triangular shape has smooth derivatives, producing flatter convolution peaks"
    })
    
    proposals.append({
        "family": "oscillatory_decay",
        "description": "Oscillatory function with exponential decay - creates structured convolution patterns",
        "code_snippet": "import jax.numpy as jnp\\n\\nf_values = jnp.linspace(-8, 8, 1000)\\nalpha = 0.5\\nbeta = 5.0\\ngamma = 1.2\\nf = (1.0 + alpha * jnp.cos(beta * f_values)) * jnp.exp(-gamma * jnp.abs(f_values))\\nf = jnp.maximum(f, 1e-8)",
        "rationale": "Oscillation creates structured convolutions; decay ensures integrability"
    })
    
    proposals.append({
        "family": "asymmetric_multistep",
        "description": "Multi-level step with asymmetric heights and non-symmetric positions",
        "code_snippet": "import jax.numpy as jnp\\n\\nf_values = jnp.linspace(-4, 4, 600)\\nn = len(f_values)\\npositions = jnp.array([0.05, 0.20, 0.45, 0.65, 0.85])\\nlevels = jnp.array([0.4, 1.3, 2.2, 1.1, 0.3])\\nf = jnp.zeros_like(f_values)\\nfor i in range(len(positions)-1):\\n    start = int(positions[i] * n)\\n    end = int(positions[i+1] * n)\\n    f = f.at[start:end].set(levels[i])\\nf = jnp.maximum(f, 1e-8)",
        "rationale": "Asymmetric multi-level breaks the perfect symmetry of standard step functions"
    })
    
    proposals.append({
        "family": "bspline_composition",
        "description": "B-spline basis with optimized control points for flexible shape control",
        "code_snippet": "import jax.numpy as jnp\\nfrom scipy.interpolate import splev, splrep\\n\\nf_values = jnp.linspace(-6, 6, 1000)\\nn_control = 60\\nknots = jnp.linspace(-5, 5, 40)\\ncontrol_basis = jnp.random.uniform(0.3, 2.5, n_control)\\ncontrols = jnp.softplus(control_basis)\\nfit = splev(f_values, knots, s=0, k=3, dx=1, w=controls)\\nf = jnp.maximum(f, 1e-8)",
        "rationale": "Splines provide smooth, flexible shapes; optimize for flatter convolutions"
    })
    
    return {
        "proposals": proposals,
        "note": "Call probe_solution for each proposal to rank before full evaluation. 30 probes = your advantage!"
    }