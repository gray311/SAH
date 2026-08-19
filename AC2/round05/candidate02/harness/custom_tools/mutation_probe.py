def run(ctx, args):
    import random
    random.seed(42 + ctx.budget_left().get('probes_remaining', 0))
    
    variants = []
    
    # Family 1: Step functions (record holders)
    step_variants = [
        {'type': 'step', 'params': {'num_pieces': 3, 'symmetry': 'symmetric', 'heights': [1.0, 1.3, 1.6]}, 
         'code': '# EVOLVE-BLOCK-START\nimport jax\nimport jax.numpy as jnp\nimport optax\nfrom dataclasses import dataclass\n@dataclass\nclass C2StepParams:\n    num_pieces: int = 3\n    symmetry: str = "symmetric"\n    heights: list = None\n    step_widths: list = None\n    piece_start: int = None\nc2_params = C2StepParams()\n'},
        {'type': 'step', 'params': {'num_pieces': 5, 'symmetry': 'asymmetric', 'heights': [0.8, 1.2, 1.5, 1.4, 1.1]}, 
         'code': '# EVOLVE-BLOCK-START\nimport jax\nimport jax.numpy as jnp\nimport optax\nfrom dataclasses import dataclass\n@dataclass\nclass C2MultiStep:\n    num_pieces: int = 5\n    heights: list = None\n    widths: list = None\n    piece_start: int = None\nc2_params = C2MultiStep(num_pieces=5, heights=[0.8, 1.2, 1.5, 1.4, 1.1], widths=[20, 25, 30, 25, 20])\n'},
        {'type': 'step', 'params': {'num_pieces': 4, 'symmetry': 'symmetric', 'heights': [1.0, 1.4, 1.0]}, 
         'code': '# EVOLVE-BLOCK-START\nimport jax\nimport jax.numpy as jnp\nimport optax\nfrom dataclasses import dataclass\n@dataclass\nclass C2SymStep:\n    num_pieces: int = 4\n    heights: list = None\n    piece_start: int = None\nc2_params = C2SymStep(num_pieces=4, heights=[1.0, 1.4, 1.0], piece_start=120)\n'},
    ]
    variants.extend(step_variants)
    
    # Family 2: Piecewise linear
    pw_variants = [
        {'type': 'piecewise', 'params': {'num_intervals': 800, 'reinit_fraction': 0.15, 'reinit_std': 0.03},
         'code': '# EVOLVE-BLOCK-START\nimport jax\nimport jax.numpy as jnp\nimport optax\nfrom dataclasses import dataclass\n@dataclass\nclass PWParams:\n    num_intervals: int = 800\n    learning_rate: float = 0.2\n    num_steps: int = 30000\n    warmup_steps: int = 3000\n    reinit_fraction: float = 0.15\n    reinit_std: float = 0.03\n    stagnation_window: int = 100\n    reinit_interval: int = 150\nc2_hypers = PWParams()\n'},
    ]
    variants.extend(pw_variants)
    
    # Family 3: Gaussian mixtures
    gauss_variants = [
        {'type': 'gaussian', 'params': {'K': 3, 'sigma': 0.15, 'means': 'clustered'},
         'code': '# EVOLVE-BLOCK-START\nimport jax\nimport jax.numpy as jnp\nimport optax\nfrom dataclasses import dataclass\nfrom scipy import stats\n@dataclass\nclass GaussMixParams:\n    K: int = 3\n    sigma: float = 0.15\n    means: list = None\nc2_gauss = GaussMixParams(K=3, sigma=0.15, means=[50, 200, 350])\n'},
        {'type': 'gaussian', 'params': {'K': 2, 'sigma': 0.2, 'means': 'bimodal'},
         'code': '# EVOLVE-BLOCK-START\nimport jax\nimport jax.numpy as jnp\nimport optax\nfrom dataclasses import dataclass\n@dataclass\nclass BimodalGauss:\n    K: int = 2\n    sigma: float = 0.2\n    mu1: float = None\n    mu2: float = None\nc2_bimodal = BimodalGauss(K=2, sigma=0.2, mu1=100, mu2=300)\n'},
    ]
    variants.extend(gauss_variants)
    
    # Family 4: Exponential combinations
    exp_variants = [
        {'type': 'exponential', 'params': {'decay_rates': [0.1, 0.3], 'num_terms': 2},
         'code': '# EVOLVE-BLOCK-START\nimport jax\nimport jax.numpy as jnp\nimport optax\nfrom dataclasses import dataclass\n@dataclass\nclass ExpComboParams:\n    decay_rates: list = None\n    num_terms: int = 2\n    centers: list = None\nc2_exp = ExpComboParams(decay_rates=[0.1, 0.3], centers=[150, 250])\n'},
    ]
    variants.extend(exp_variants)
    
    # Return top variants
    for i, v in enumerate(variants[:10]):
        v['variant_id'] = i
    return {"variants": variants[:10], "recommendation": "Start with step functions (record holders), then explore piecewise linear, gaussian mixtures, and exponential combinations."}
