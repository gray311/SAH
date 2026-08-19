def run(ctx, args):
    return {"candidates": [
        {"name": "single", "code": "h=jnp.where(x<=1.0,1.0,0.0)", "integral": 1.0},
        {"name": "double", "code": "h=jnp.where((x<=0.5)|(x>=1.5),0.5,0.0)", "integral": 0.5},
        {"name": "concentrated", "code": "h=jnp.where((x>=0.9)&(x<=1.1),0.5,0.0)", "integral": 0.1},
        {"name": "sin", "code": "h=jnp.clip(jnp.sin(jnp.pi*x)+0.5,0.0,1.0)", "integral": "normalize"},
        {"name": "piecewise", "code": "h=jnp.where(x<0.5,1.0,0.0)", "integral": 0.5}
    ], "recommendation": "Test single with num_intervals=100, num_steps=2000. Check integral constraint.", "next": "Measure c5_bound, increase complexity only if < 0.38"}
