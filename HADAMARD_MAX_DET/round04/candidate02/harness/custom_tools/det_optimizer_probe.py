def run(ctx, args):
    import numpy as np
    import random
    
    n = 29
    residues = (0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28)
    
    def det_func(A):
        return abs(np.linalg.det(np.array(A, dtype=float)))
    
    param_combos = [
        (15.0, 0.9995), (8.0, 0.998), (5.0, 0.996), 
        (3.0, 0.995), (2.0, 0.994), (20.0, 0.9998),
        (10.0, 0.999), (6.0, 0.997), (4.0, 0.9965)
    ]
    seeds = [42, 123, 456, 789, 999]
    
    best_combos = []
    palley_base = [[1 if (i-j)%n in residues else -1 for j in range(n)] for i in range(n)]
    
    for temp, cool_rate in param_combos:
        for seed in seeds[:3]:
            rng = random.Random(seed)
            current = [r[:] for r in palley_base]
            T = temp
            best_det = det_func(current)
            
            for step in range(5000):
                i = rng.randrange(n)
                j = rng.randrange(n)
                current[i][j] *= -1
                
                new_det = det_func(current)
                delta = new_det - best_det
                
                if delta > 0:
                    best_det = new_det
                    current[i][j] *= -1
                elif T > 1e-10 and rng.random() < np.exp(delta/T):
                    best_det = new_det
                    current[i][j] *= -1
                else:
                    current[i][j] *= -1
                T *= cool_rate
            
            if best_det > 170:
                best_combos.append({'temp': temp, 'cool_rate': cool_rate, 'score': best_det})
    
    best_combos.sort(key=lambda x: x['score'], reverse=True)
    return {'best_params': best_combos[:5]}
