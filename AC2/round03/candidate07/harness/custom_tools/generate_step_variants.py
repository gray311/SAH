def run(ctx, args):
    import re
    
    n = ctx.get_program()
    if isinstance(n, (int, float)):
        num_intervals = int(n)
    else:
        try:
            prog_text = str(ctx.get_program())
            match = re.search(r'num_intervals\s*=\s*(\d+)', prog_text)
            if match:
                num_intervals = int(match.group(1))
            else:
                num_intervals = 300
        except:
            num_intervals = 300
    
    variants = []
    ni = num_intervals
    
    variants.append({
        "name": "wide_step",
        "code": "f = jnp.zeros(" + str(ni) + "); f = f.at[int(0.2*"+str(ni)+"):int(0.8*"+str(ni)+")].set(1.0)",
        "description": "Standard wide step 0.2n-0.8n"
    })
    
    variants.append({
        "name": "taller_step", 
        "code": "f = jnp.zeros(" + str(ni) + "); f = f.at[int(0.2*"+str(ni)+"):int(0.8*"+str(ni)+")].set(1.3)",
        "description": "Wider step with height 1.3"
    })
    
    variants.append({
        "name": "narrow_tall",
        "code": "f = jnp.zeros(" + str(ni) + "); f = f.at[int(0.3*"+str(ni)+"):int(0.7*"+str(ni)+")].set(1.5)",
        "description": "Narrower support, taller height"
    })
    
    variants.append({
        "name": "wide_short",
        "code": "f = jnp.zeros(" + str(ni) + "); f = f.at[int(0.15*"+str(ni)+"):int(0.85*"+str(ni)+")].set(0.7)",
        "description": "Very wide, shorter step"
    })
    
    variants.append({
        "name": "asymmetric_two",
        "code": "f = jnp.zeros(" + str(ni) + "); f = f.at[int(0.2*"+str(ni)+"):int(0.45*"+str(ni)+")].set(2.0); f = f.at[int(0.55*"+str(ni)+"):int(0.8*"+str(ni)+")].set(0.6)",
        "description": "Asymmetric two-level: high left, low right"
    })
    
    variants.append({
        "name": "dual_regions",
        "code": "f = jnp.zeros(" + str(ni) + "); f = f.at[int(0.1*"+str(ni)+"):int(0.35*"+str(ni)+")].set(1.2); f = f.at[int(0.65*"+str(ni)+"):int(0.9*"+str(ni)+")].set(1.2)",
        "description": "Two disjoint regions"
    })
    
    variants.append({
        "name": "three_level",
        "code": "f = jnp.zeros(" + str(ni) + "); f = f.at[int(0.1*"+str(ni)+"):int(0.25*"+str(ni)+")].set(1.5); f = f.at[int(0.25*"+str(ni)+"):int(0.7*"+str(ni)+")].set(0.8); f = f.at[int(0.7*"+str(ni)+"):int(0.85*"+str(ni)+")].set(1.5)",
        "description": "Three-level with high-middle-low pattern"
    })
    
    variants.append({
        "name": "twin_spikes",
        "code": "f = jnp.zeros(" + str(ni) + "); f = f.at[int(0.2*"+str(ni)+"):int(0.35*"+str(ni)+")].set(2.5); f = f.at[int(0.5*"+str(ni)+"):int(0.65*"+str(ni)+")].set(2.5)",
        "description": "Two tall narrow spikes"
    })
    
    variants.append({
        "name": "canonical",
        "code": "f = jnp.zeros(" + str(ni) + "); f = f.at[int(0.25*"+str(ni)+"):int(0.75*"+str(ni)+")].set(1.0)",
        "description": "Canonical step function"
    })
    
    return {"variants": variants, "num_intervals": num_intervals, "total": len(variants)}
