def run(ctx, args):
    import re
    import random
    
    code = ctx.get_program()
    lines = code.split('\n')
    n = 600
    
    # Extract actual step levels from the EVOLVE-BLOCK
    levels_found = []
    
    for line in lines:
        if '.set(' in line and 'jnp.array' in line:
            try:
                match = re.search(r'set\((\d+\.?\d*)', line)
                if match:
                    levels_found.append(float(match.group(1)))
            except:
                pass
    
    # Default to reasonable step function levels if not found
    if not levels_found:
        levels_found = [1.0, 1.4, 2.0, 1.4, 1.0]
    
    # Generate 5 mutation proposals
    mutations = [
        {
            "type": "height_fine_tuning",
            "description": "Perturb heights by ±0.02-0.05",
            "rationale": "Fine-tune the L2/inf ratio with small changes",
            "code_snippet": "import jax.numpy as jnp\nimport random\nrandom.seed(42)\nf_values = jnp.linspace(-3, 3, {n})\nf = jnp.zeros({n})\nlevels = jnp.array({levels_found})\nfor i in range(len(levels)):\n    delta = random.uniform(-0.04, 0.04)\n    levels = levels.at[i].set(levels[i] + delta)\npositions = jnp.linspace(-1, 1, 6)\nfor i in range(len(positions) - 1):\n    start = int((positions[i] + 1) / 2 * {n})\n    end = int((positions[i+1] + 1) / 2 * {n})\n    f = f.at[start:end].set(levels[i])\nf = jnp.maximum(f, 1e-6)",
            "mutation_params": {"delta_range": [-0.04, 0.04]}
        },
        {
            "type": "width_redistribution",
            "description": "Redistribute interval widths by ±3%",
            "rationale": "Expand core intervals to increase L2 norm",
            "code_snippet": "import jax.numpy as jnp\nimport random\nrandom.seed(42)\nf_values = jnp.linspace(-3, 3, {n})\nf = jnp.zeros({n})\nlevels = jnp.array({levels_found})\npositions = jnp.linspace(-1, 1, 6)\nfor i in range(len(positions) - 1):\n    # Expand middle intervals, contract outer ones\n    if 1 <= i <= 3:\n        delta = random.uniform(0.02, 0.04)\n        positions = positions.at[i+1].set(positions[i+1] + delta)\n    else:\n        delta = random.uniform(-0.02, -0.04)\n        positions = positions.at[i+1].set(positions[i+1] + delta)\nfor i in range(len(positions) - 1):\n    start = int((positions[i] + 1) / 2 * {n})\n    end = int((positions[i+1] + 1) / 2 * {n})\n    f = f.at[start:end].set(levels[i])\nf = jnp.maximum(f, 1e-6)",
            "mutation_params": {"width_delta": [-0.04, 0.04]}
        },
        {
            "type": "asymmetric_perturbation",
            "description": "Break symmetry by making left/right widths different",
            "rationale": "Reduce constructive interference from perfect symmetry",
            "code_snippet": "import jax.numpy as jnp\nf_values = jnp.linspace(-3, 3, {n})\nf = jnp.zeros({n})\n# Asymmetric widths: left narrower, right wider\nleft_width = 0.22 * {n}\nright_width = 0.28 * {n}\nplateau = {n} - left_width - right_width\nf = f.at[0:left_width].set(levels[0])\nf = f.at[{n}-right_width:{n}].set(levels[4])\nf = f.at[left_width:{n}-right_width].set(levels[2])\nf = jnp.maximum(f, 1e-6)",
            "mutation_params": {"left_width_frac": 0.22, "right_width_frac": 0.28}
        },
        {
            "type": "level_split",
            "description": "Split the highest level into two",
            "rationale": "Create more sophisticated step pattern with 6 levels",
            "code_snippet": "import jax.numpy as jnp\nimport random\nrandom.seed(42)\nf_values = jnp.linspace(-3, 3, {n})\nf = jnp.zeros({n})\nlevels = jnp.array({levels_found})\npositions = jnp.linspace(-1, 1, 7)  # 6 intervals for split\nfor i in range(len(positions) - 1):\n    start = int((positions[i] + 1) / 2 * {n})\n    end = int((positions[i+1] + 1) / 2 * {n})\n    if i == 2:\n        mid = (start + end) // 2\n        f = f.at[start:mid].set(levels[2] + 0.08)\n        f = f.at[mid:end].set(levels[2] + 0.12)\n    else:\n        f = f.at[start:end].set(levels[i])\nf = jnp.maximum(f, 1e-6)",
            "mutation_params": {"split_level": 2, "delta1": 0.08, "delta2": 0.12}
        },
        {
            "type": "position_shift",
            "description": "Shift all boundaries by +2% of domain",
            "rationale": "Change effective support, possibly reducing ||f★f||_inf",
            "code_snippet": "import jax.numpy as jnp\nf_values = jnp.linspace(-3, 3, {n})\nf = jnp.zeros({n})\nlevels = jnp.array({levels_found})\npositions = jnp.linspace(-1, 1, 6) + 0.04  # Shift right\nfor i in range(len(positions) - 1):\n    start = int((positions[i] + 1) / 2 * {n})\n    end = int((positions[i+1] + 1) / 2 * {n})\n    f = f.at[start:end].set(levels[i])\nf = jnp.maximum(f, 1e-6)",
            "mutation_params": {"shift": 0.04}
        }
    ]
    
    return {"mutations": mutations, "note": "Use probe_solution to rank these mutations before full evaluation. Probes are reliable for comparing step-function variants."}
