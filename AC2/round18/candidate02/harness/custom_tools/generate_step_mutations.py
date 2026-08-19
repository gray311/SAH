def run(ctx, args):
    import random
    random.seed(42)
    
    heights = [1.40, 1.50, 1.60, 1.90, 0.90]
    positions = [0.25, 0.35, 0.55, 0.70, 0.85]
    n_intervals = 600
    
    mutations = []
    
    for i in range(8):
        pos_shift = random.uniform(-0.05, 0.05)
        height_shift = random.uniform(-0.2, 0.2)
        add_level = random.random() > 0.7
        
        mutations.append({
            'variant_id': i,
            'pos_shift': round(pos_shift, 4),
            'height_shift': round(height_shift, 4),
            'add_level': add_level,
            'code': f'''import jax.numpy as jnp
import jax

n = {n_intervals}
f = jnp.zeros(n)

f = f.at[int(0.25*n):int(0.35*n)].set({heights[0]} + {height_shift:+.2f})
f = f.at[int(0.35*n):int(0.55*n)].set({heights[1]} + {height_shift:+.2f})
f = f.at[int(0.55*n):int(0.70*n)].set({heights[2]} + {height_shift:+.2f})
f = f.at[int(0.70*n):int(0.85*n)].set({heights[3]} + {height_shift:+.2f})
f = f.at[int(0.85*n):int(0.95*n)].set({heights[4]} + {height_shift:+.2f})
f = jnp.maximum(f, 0)
'''
        })
    
    return {
        'mutations': mutations,
        'note': f'Generated {len(mutations)} step function mutations'
    }