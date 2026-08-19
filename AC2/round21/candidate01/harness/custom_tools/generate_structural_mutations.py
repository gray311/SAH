def run(ctx, args):
    n = 600
    variants = []
    
    variants.append({"description": "Asymmetric: left low, right high", "edit": "f = f.at[int(0.08*n):int(0.30*n)].set(1.0); f = f.at[int(0.30*n):int(0.60*n)].set(2.8); f = f.at[int(0.60*n):int(0.80*n)].set(1.2)"})
    
    variants.append({"description": "Asymmetric: left high, right low", "edit": "f = f.at[int(0.08*n):int(0.35*n)].set(2.8); f = f.at[int(0.35*n):int(0.65*n)].set(1.0); f = f.at[int(0.65*n):int(0.82*n)].set(1.4)"})
    
    variants.append({"description": "Three-level staircase", "edit": "f = f.at[int(0.10*n):int(0.30*n)].set(0.9); f = f.at[int(0.30*n):int(0.50*n)].set(1.9); f = f.at[int(0.50*n):int(0.75*n)].set(2.4); f = f.at[int(0.75*n):int(0.90*n)].set(1.1)"})
    
    variants.append({"description": "Wide base with narrow high peak", "edit": "f = f.at[int(0.12*n):int(0.88*n)].set(1.1); f = f.at[int(0.38*n):int(0.62*n)].set(3.2)"})
    
    variants.append({"description": "Multi-level with valley", "edit": "f = f.at[int(0.10*n):int(0.35*n)].set(1.8); f = f.at[int(0.35*n):int(0.45*n)].set(0.6); f = f.at[int(0.45*n):int(0.70*n)].set(2.6); f = f.at[int(0.70*n):int(0.85*n)].set(1.3)"})
    
    return {"variants": variants[:5], "num_variants": 5}