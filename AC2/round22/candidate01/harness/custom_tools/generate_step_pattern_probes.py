def run(ctx, args):
    num_patterns = args.get('num_patterns', 10)
    n_intervals = 600
    
    import random
    random.seed(42)
    
    # Select diverse patterns from the seed's 12 known patterns
    pattern_specs = [
        (0, 1.40, "High peak single step"),
        (1, 1.50, "Higher peak"),
        (2, 1.60, "Very high narrow peak"),
        (3, 1.90, "Multi-level with high middle"),
        (4, 2.30, "Three-level asymmetric"),
        (5, 1.50, "Two high steps"),
        (6, 1.70, "Four-level function"),
        (7, 2.20, "Narrow high peak with wings"),
        (8, 1.50, "Staircase pattern"),
        (9, 2.00, "Asymmetric multi-level"),
        (10, 2.80, "Wide base with narrow high peak"),
        (11, 2.50, "Three distinct peaks"),
    ]
    
    # Select diverse patterns (avoid duplicates)
    selected_specs = []
    used_variants = set()
    for _ in range(min(num_patterns, len(pattern_specs))):
        for idx, (p_idx, height, desc) in enumerate(pattern_specs):
            if idx not in used_variants and len(selected_specs) < num_patterns:
                selected_specs.append((p_idx, height))
                used_variants.add(idx)
                break
    
    # Generate program code for each pattern
    programs = []
    for p_idx, height in selected_specs:
        n = n_intervals
        lines = [
            f"import jax.numpy as jnp",
            f"f = jnp.zeros({n})",
            f"# Pattern {p_idx}: height={height:.2f}"
        ]
        
        # Create simple step pattern
        start_idx = int(0.25 * n)
        end_idx = int(0.75 * n)
        lines.append(f"f = f.at[{start_idx}:{end_idx}].set({height})")
        lines.append("return f")
        
        program_code = "\n".join(lines)
        programs.append(program_code)
    
    return {"patterns": programs}