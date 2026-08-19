def run(ctx, args):
    import random
    random.seed(42)
    n = 600
    proposals = []
    
    # Family A: Level count variation
    for levels in [3, 4, 5, 6, 7]:
        heights = [0.8, 1.5, 2.2] if levels <= 4 else [0.6, 1.2, 1.8, 2.5]
        positions = [0.1 + i * (0.9 - 0.1) / levels for i in range(levels)]
        proposals.append({
            'family': 'levels_' + str(levels),
            'code': 'nf = jnp.zeros(n)\nfor pos, h in zip([' + str(positions) + ']:\n' +
                    '    nf = nf.at[int(pos*n):int((pos+0.15)*n)].set(h)\n' +
                    'nf = jnp.maximum(nf, 0.0)',
            'rationale': 'Test ' + str(levels) + ' level patterns'
        })
    
    # Family B: Asymmetric clusters
    code_left = 'nf = jnp.zeros(n)\nnf = nf.at[int(0.1*n):int(0.35*n)].set(1.5)\nnf = nf.at[int(0.35*n):int(0.55*n)].set(2.2)\nnf = nf.at[int(0.55*n):int(0.85*n)].set(1.0)\nnf = jnp.maximum(nf, 0.0)'
    proposals.append({'family': 'clustered_left', 'code': code_left, 'rationale': 'Left-heavy cluster'})
    
    code_right = 'nf = jnp.zeros(n)\nnf = nf.at[int(0.15*n):int(0.45*n)].set(1.8)\nnf = nf.at[int(0.45*n):int(0.65*n)].set(2.5)\nnf = nf.at[int(0.65*n):int(0.95*n)].set(1.2)\nnf = jnp.maximum(nf, 0.0)'
    proposals.append({'family': 'clustered_right', 'code': code_right, 'rationale': 'Right-heavy cluster'})
    
    code_multi = 'nf = jnp.zeros(n)\nnf = nf.at[int(0.1*n):int(0.25*n)].set(1.2)\nnf = nf.at[int(0.25*n):int(0.40*n)].set(2.0)\nnf = nf.at[int(0.40*n):int(0.55*n)].set(1.8)\nnf = nf.at[int(0.55*n):int(0.70*n)].set(2.0)\nnf = nf.at[int(0.70*n):int(0.9*n)].set(1.2)\nnf = jnp.maximum(nf, 0.0)'
    proposals.append({'family': 'clustered_multi', 'code': code_multi, 'rationale': 'Multi-peak cluster'})
    
    code_fractal = 'nf = jnp.zeros(n)\nnf = nf.at[int(0.1*n):int(0.35*n)].set(0.7)\nnf = nf.at[int(0.35*n):int(0.65*n)].set(2.0)\nnf = nf.at[int(0.65*n):int(0.9*n)].set(0.7)\nmid_start = int(0.35 * n)\nmid_end = int(0.65 * n)\nfor i in range(0, mid_end - mid_start, n // 20):\n    nf = nf.at[mid_start + i:mid_start + min(i + 15, mid_end)].set(2.3)\nnf = jnp.maximum(nf, 0.0)'
    proposals.append({'family': 'fractal', 'code': code_fractal, 'rationale': 'Fractal-like pattern'})
    
    return {'proposals': proposals, 'note': 'Use probe_solution to rank before full eval'}
