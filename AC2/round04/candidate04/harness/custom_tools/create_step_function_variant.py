def run(ctx, args):
    import re
    
    # Get num_intervals from program or default to 300
    program_text = str(ctx.get_program())
    num_intervals = 300
    if 'num_intervals' in program_text:
        match = re.search(r'num_intervals:\s*(\d+)', program_text)
        if match:
            num_intervals = int(match.group(1))
    
    # Generate diverse step function variants
    variants = []
    
    # Variant 1: Single wide step
    variants.append('Single wide step function\nstart = int(0.2 * {n})\nend = int(0.8 * {n})\nh = 1.2\nf = jnp.zeros({n})\nf = f.at[start:end].set(h)'.format(n=num_intervals))
    
    # Variant 2: Multi-level step (3 levels)
    variants.append('Multi-level step function (3 levels)\nn = {n}\nf = jnp.zeros(n)\nf = f.at[int(0.1*n):int(0.25*n)].set(1.0)\nf = f.at[int(0.25*n):int(0.5*n)].set(2.0)\nf = f.at[int(0.5*n):int(0.75*n)].set(1.5)\nf = f.at[int(0.75*n):int(0.9*n)].set(0.8)'.format(n=num_intervals))
    
    # Variant 3: Asymmetric step
    variants.append('Asymmetric step function\nstart = int(0.15 * {n})\nend = int(0.45 * {n})\nh_left = 1.3\nf = jnp.zeros({n})\nf = f.at[start:end].set(h_left)'.format(n=num_intervals))
    
    # Variant 4: Multiple narrow steps
    variants.append('Multiple narrow steps\nn = {n}\nf = jnp.zeros(n)\nf = f.at[int(0.2*n):int(0.25*n)].set(1.5)\nf = f.at[int(0.35*n):int(0.4*n)].set(2.0)\nf = f.at[int(0.5*n):int(0.55*n)].set(1.8)\nf = f.at[int(0.65*n):int(0.7*n)].set(2.2)'.format(n=num_intervals))
    
    # Variant 5: Two-level step with gap
    variants.append('Two-level step with gap\nn = {n}\nf = jnp.zeros(n)\nf = f.at[int(0.1*n):int(0.35*n)].set(1.8)\nf = f.at[int(0.45*n):int(0.8*n)].set(1.2)'.format(n=num_intervals))
    
    return {"variants": variants}
