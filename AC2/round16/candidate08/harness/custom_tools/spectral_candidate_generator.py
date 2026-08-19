def run(ctx, args):
    import random
    random.seed(42)
    proposals = []
    
    # Space 1: Fourier eigenfunctions (sine series)
    proposals.append({
        "family": "fourier_eigen",
        "description": "Fourier sine series: f(x) = sum c_k * sin(k*pi*(x+L/2)/L), optimized coefficients",
        "code_snippet": "import jax.numpy as jnp\\nimport jax\\nf_values = jnp.linspace(-3, 3, 600)\\nL = 6.0\\nK = 5\\nks = jnp.arange(1, K+1)\\nweights = jnp.exp(-jnp.sqrt(ks))\\nc = jnp.zeros_like(ks)\\nc = c.at[0].set(1.0)\\nc = c.at[1:4].set(0.3 + 0.2 * random.random(3))\\nc = c.at[4:].set(0.15 + 0.05 * random.random(len(c)))\\nf = (c[None,:] * jnp.sin(ks[None,:] * jnp.pi * (f_values + L/2) / L)).sum(axis=0)\\nf = jnp.maximum(f, 1e-6)\\nf = f / jnp.max(f)",
        "rationale": "Eigenfunctions of convolution operators may optimize spectral ratios"
    })
    
    # Space 2: Laguerre polynomial mixture
    proposals.append({
        "family": "laguerre",
        "description": "Laguerre polynomials with exponential weight: f(x) = sum a_n * L_n(alpha*x^2) * exp(-alpha*x^2/2)",
        "code_snippet": "import jax.numpy as jnp\\nimport jax\\nf_values = jnp.linspace(-3, 3, 600)\\nalpha = 0.8 + 0.3 * random.random()\\nn_terms = 4\\nfrom scipy.special import eval_laguerre\\nL_vals = jnp.stack([eval_laguerre(alpha * f_values**2 / 2, i) for i in range(n_terms)], axis=0)\\ncoeffs = jnp.random.uniform(0.3, 1.5, n_terms)\\ncoeffs = coeffs / jnp.sum(coeffs)\\nf = (coeffs[None,:] * L_vals).sum(axis=0)\\nf = f * jnp.exp(-alpha * f_values**2 / 2)\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Laguerre basis is natural for functions on semi-infinite domains with decay"
    })
    
    # Space 3: Variational modulated envelope
    proposals.append({
        "family": "variational_modulated",
        "description": "f(x) = (1 + alpha*cos(beta*x))^n * exp(-gamma*|x|), variational trial function",
        "code_snippet": "import jax.numpy as jnp\\nimport jax\\nf_values = jnp.linspace(-5, 5, 800)\\nn = random.choice([2, 3, 4])\\nalpha = 0.2 + 0.3 * random.random()\\nbeta = 2.0 + 3.0 * random.random()\\ngamma = 0.5 + 0.5 * random.random()\\nf = (1 + alpha * jnp.cos(beta * f_values))**n * jnp.exp(-gamma * jnp.abs(f_values))\\nf = jnp.maximum(f, 1e-6)",
        "rationale": "Variational trial functions from calculus of variations may capture optimal shape"
    })
    
    # Space 4: Dense-sparse hybrid
    proposals.append({
        "family": "dense_sparse_hybrid",
        "description": "f(x) = base_exp + sum localized Gaussian bumps at optimized positions",
        "code_snippet": "import jax.numpy as jnp\\nimport jax\\nf_values = jnp.linspace(-4, 4, 700)\\nbase = jnp.exp(-0.6 * jnp.abs(f_values))\\nnum_bumps = 3\\nbump_centers = f_values[jnp.linspace(-0.3, 0.3, num_bumps)]\\nbump_widths = jnp.array([0.4, 0.5, 0.35])\\nfor i in range(num_bumps):\\n    dist = jnp.abs(f_values[:,None] - bump_centers[i][None])\\n    f = f + 0.4 * jnp.exp(-dist**2 / bump_widths[i]**2)\\nf = jnp.maximum(f, 1e-6)\\nf = f / jnp.max(f)",
        "rationale": "Localized features on smooth background may improve L2/infinity ratio better than steps"
    })
    
    # Space 5: Hermite-Gaussian
    proposals.append({
        "family": "hermite_gaussian",
        "description": "Hermite-Gaussian: f(x) = sum a_n * H_n(sqrt(alpha)*x) * exp(-alpha*x^2/2)",
        "code_snippet": "import jax.numpy as jnp\\nimport jax\\nf_values = jnp.linspace(-3, 3, 600)\\nalpha = 0.7 + 0.3 * random.random()\\nfrom scipy.special import hermite\\nn_terms = 4\\nH_polys = [hermite(i) for i in range(n_terms)]\\nH_vals = jnp.stack([H_polys[i](jnp.sqrt(alpha) * f_values) for i in range(n_terms)], axis=0)\\ncoeffs = jnp.random.uniform(0.2, 1.2, n_terms)\\ncoeffs = coeffs / jnp.sum(coeffs)\\nf = (coeffs[None,:] * H_vals).sum(axis=0)\\nf = f * jnp.exp(-alpha * f_values**2 / 2)\\nf = jnp.maximum(f, 1e-6)\\nf = f / jnp.max(f)",
        "rationale": "Hermite functions are eigenfunctions of Fourier transform, natural for convolution problems"
    })
    
    return {
        "proposals": proposals,
        "note": "Evaluate each candidate DIRECTLY with evaluate_solution. Do NOT use probes."
    }
