def run(ctx, args):
    import numpy as np
    n = 29
    residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
    
    # Variant A: Paley base
    def build_paley():
        H = np.zeros((n, n), dtype=int)
        for i in range(n):
            for j in range(n):
                H[i, j] = 1 if (i-j) % n in residues else -1
        return H
    
    # Variant B: Random matrix
    def build_random():
        return np.random.choice([-1, 1], size=(n, n))
    
    # Variant C: Perturbed Paley
    def build_perturbed_paley():
        H = build_paley().copy()
        for i in range(n):
            for j in range(n):
                if np.random.random() < 0.05:
                    H[i, j] *= -1
        return H
    
    base = build_paley()
    random_mat = build_random()
    perturbed = build_perturbed_paley()
    
    return {
        "base_paley": {"matrix": base.tolist(), "params": {"sa_iters": 5000, "T": 3.0, "cool": 0.995, "seeds": [42, 123, 456]}},
        "random_start": {"matrix": random_mat.tolist(), "params": {"sa_iters": 5000, "T": 4.0, "cool": 0.995, "seeds": [789, 2024, 2025]}},
        "perturbed_paley": {"matrix": perturbed.tolist(), "params": {"sa_iters": 5000, "T": 2.5, "cool": 0.995, "seeds": [2026, 2027, 4000]}}
    }
