def run(ctx, args):
    import numpy as np
    import random
    
    n = 29
    iterations = args.get('iterations', 15000)
    initial_temp = args.get('initial_temp', 4.0)
    cool_rate = args.get('cool_rate', 0.997)
    num_seeds = args.get('num_seeds', 4)
    seed = args.get('seed', 42)
    
    def det_func(A):
        return abs(np.linalg.det(np.array(A, dtype=float)))
    
    best_overall = None
    best_det_overall = -1
    
    for restart in range(num_seeds):
        rng = random.Random(seed + restart)
        current = [rng.randint(-1, 1) for _ in range(n * n)]
        current = [current[i*n:(i+1)*n] for i in range(n)]
        
        T = initial_temp
        cur_det = det_func(current)
        best = [r[:] for r in current]
        best_det = cur_det
        
        for step in range(iterations):
            i = rng.randrange(n)
            j = rng.randrange(n)
            current[i][j] *= -1
            new_det = det_func(current)
            delta = new_det - cur_det
            
            accepted = False
            if delta > 0:
                accepted = True
                cur_det = new_det
            elif T > 1e-10 and rng.random() < np.exp(delta/T):
                accepted = True
                cur_det = new_det
            else:
                current[i][j] *= -1
            
            if accepted and new_det > best_det:
                best_det = new_det
                best = [r[:] for r in current]
            
            T *= cool_rate
        
        if best_det > best_det_overall:
            best_det_overall = best_det
            best_overall = [r[:] for r in best]
    
    if best_overall is None:
        return {"score": float(best_det_overall) if best_det_overall >= 0 else 0.5}
    
    result = np.array(best_overall, dtype=int)
    
    code = ctx.get_program()
    lines = code.split('\n')
    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if '# EVOLVE-BLOCK-START' in line:
            start_idx = i
        if '# EVOLVE-BLOCK-END' in line and start_idx is not None:
            end_idx = i
            break
    
    if start_idx is not None and end_idx is not None:
        lines[start_idx:end_idx+1] = [
            '"""Final optimized result"""\n',
            'matrix = ' + str(result.tolist()) + '\n',
            'return (matrix,)'
        ]
        new_code = '\n'.join(lines)
        ctx.stage_edit(new_code)
    
    return {"probe_score": float(best_det_overall), "iterations": iterations, "seeds": num_seeds}
