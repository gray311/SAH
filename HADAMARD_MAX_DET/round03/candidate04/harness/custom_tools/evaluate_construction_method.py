def run(ctx, args):
    import random
    import numpy as np
    n = 29
    ct = args.get('construction_type', 'paley')
    iters = args.get('iterations', 50000)
    mut_rate = args.get('mutation_rate', 0.02)
    
    best_det = 0
    
    def fast_det(A):
        return abs(np.linalg.det(np.array(A, dtype=float)))
    
    if ct == 'paley':
        res = {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
        start = [[1 if (i-j)%n in res else -1 for j in range(n)] for i in range(n)]
    elif ct == 'random':
        start = np.random.choice([-1,1], size=(n,n)).tolist()
    elif ct == 'block':
        res = {0,1,4,5,6,7,9,11,13,15,16,17,19,22,23}
        start = [[1 if (i-j)%(n-2) in res else -1 for j in range(n-2)] for i in range(n-2)]
        start = [[start[i][j] if j<n-2 else 1 for j in range(n)] for i in range(n)]
        start[0] = [1]*n
        start[-1] = [1]*n
    elif ct == 'genetic':
        pop = [np.random.choice([-1,1], size=(n,n)).tolist() for _ in range(10)]
        for gen in range(10):
            pop.sort(key=lambda m: fast_det(m), reverse=True)
            new_pop = pop[:5]
            for _ in range(5):
                child = pop[random.randint(0,4)][:][:]
                rows = random.sample(range(n), random.randint(5,10))
                for r in rows:
                    child[r] = pop[random.randint(0,4)][r][:]
                for i in range(n):
                    for j in range(n):
                        if random.random() < mut_rate:
                            child[i][j] *= -1
                new_pop.append(child)
            pop = new_pop[:10]
        start = pop[0]
    elif ct == 'permutation':
        start = np.random.choice([-1,1], size=(n,n)).tolist()
    
    final_det = fast_det(start)
    if final_det > best_det:
        best_det = final_det
    
    return {"construction": ct, "iterations": iters, "mutation_rate": mut_rate, "best_det": best_det, "ratio": best_det/(n*np.sqrt(n))}
