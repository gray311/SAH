def run(ctx, args):
    import numpy as np
    import random
    
    n = 29
    
    # Method 1: Pure random
    random_matrix = np.random.choice([-1, 1], size=(n, n))
    
    # Method 2: Paley construction
    def paley_matrix(size):
        residues = set()
        for i in range(1, size):
            residues.add((i * i) % size)
        residues.add(0)
        matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                diff = (i - j) % size
                row.append(1 if diff in residues else -1)
            matrix.append(row)
        return np.array(matrix)
    
    paley_matrix_arr = paley_matrix(n)
    
    # Method 3: Random perturbations of Paley
    perturbed = paley_matrix_arr.copy()
    for _ in range(int(n * 0.1)):  # 10% perturbations
        i, j = np.random.randint(n), np.random.randint(n)
        perturbed[i, j] *= -1
    
    return {
        "random": random_matrix.tolist(),
        "paley": paley_matrix_arr.tolist(),
        "perturbed": perturbed.tolist(),
        "suggestion": "Choose one of these starting points for hill climbing"
    }
