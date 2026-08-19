def run(ctx, args):
    import numpy as np
    
    n = 29
    
    # Method 1: Paley construction (quadratic residues mod 29)
    paley_residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
    paley = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            diff = (i - j) % n
            paley[i, j] = 1 if diff in paley_residues else -1
    
    # Method 2: Random ±1 matrix
    random_mat = np.random.choice([-1, 1], size=(n, n))
    
    # Method 3: Thue-Morse based pattern (alternating blocks)
    thue = [0, 1, 1, 0]
    for _ in range(14):
        thue += [1-x for x in thue]
    thue_mat = np.zeros((n, n), dtype=int)
    for i in range(n):
        row_pattern = thue[:n]
        for j in range(n):
            thue_mat[i, j] = 1 if row_pattern[j] == 0 else -1
    
    # Method 4: Van der Corput lattice
    lattice = np.zeros((n, n), dtype=int)
    for i in range(n):
        row_val = 0
        temp = i + 1
        for b in range(15):
            if temp % 2 == 1:
                row_val += 2**b
            temp //= 2
        row_bits = [(row_val >> k) & 1 for k in range(n)]
        for j in range(n):
            lattice[i, j] = 1 if row_bits[j] == 0 else -1
    
    # Method 5: Structured block diagonal
    structured = np.ones((n, n), dtype=int)
    for block_idx in range(5):
        start = block_idx * 6
        if start >= n:
            break
        block_size = min(6, n - start)
        for i in range(block_size):
            for j in range(block_size):
                if (i - j) % 2 == 1:
                    structured[start + i, start + j] = -1
    
    variants = [
        {"name": "paley", "matrix": paley},
        {"name": "random", "matrix": random_mat},
        {"name": "thue_morse", "matrix": thue_mat},
        {"name": "lattice", "matrix": lattice},
        {"name": "structured", "matrix": structured}
    ]
    
    return {"variants": variants, "n": n, "methods_used": 5}
