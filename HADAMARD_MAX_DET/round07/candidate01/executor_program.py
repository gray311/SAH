# EVOLVE-BLOCK-START
"""Exact config that gave 0.523117 - try to beat it"""
import numpy as np
import random

def det_fn(A):
    return abs(np.linalg.det(np.array(A, dtype=float)))

def sa_refine(matrix_list, n, seed, iters, T_start, cool_rate):
    """Refine with SA"""
    rng = random.Random(seed)
    cur = [row[:] for row in matrix_list]
    best = cur[:]
    cd = det_fn(cur)
    bd = cd
    T_val = T_start
    
    for _ in range(iters):
        i, j = rng.randrange(n), rng.randrange(n)
        cur[i][j] *= -1
        nd = det_fn(cur)
        delta = nd - cd
        
        if delta >= 0:
            cd = nd
            if T_val > 1e-15:
                T_val *= cool_rate
            else:
                best = cur[:]
        elif T_val > 1e-15 and rng.random() < np.exp(delta/T_val):
            cd = nd
            if T_val > 1e-15:
                T_val *= cool_rate
        else:
            cur[i][j] *= -1
            if T_val > 1e-15:
                T_val *= cool_rate
        
        if nd > bd:
            bd, best = nd, cur[:]
    
    return best

def perturb_matrix(matrix, num_flips=15):
    """Flip random entries in matrix"""
    perturbed = [row[:] for row in matrix]
    indices_to_flip = random.sample(range(29*29), min(num_flips, 29*29))
    for idx in indices_to_flip:
        i, j = divmod(idx, 29)
        perturbed[i][j] *= -1
    return perturbed

def get_variant_matrices(n=29):
    variants = []
    QR = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
    paley = [[1 if (i-j)%n in QR else -1 for j in range(n)] for i in range(n)]
    variants.append(paley)
    
    random_var = [[random.choice([1, -1]) for _ in range(n)] for _ in range(n)]
    variants.append(random_var)
    
    def thue_morse(k):
        s = bin(k).count('1')
        return 1 if s % 2 == 0 else -1
    
    tm = [[thue_morse(i + j) for j in range(n)] for i in range(n)]
    variants.append(tm)
    
    lattice = [[1 if (((i * 29 + j) * 0.5 - int((i * 29 + j) * 0.5)) - 0.5) >= 0 else -1 for j in range(n)] for i in range(n)]
    variants.append(lattice)
    
    block_size = 14
    block = []
    for i in range(n):
        row = []
        for j in range(n):
            bi, bj = i // block_size, j // block_size
            ri, rj = i % block_size, j % block_size
            if bi == bj:
                val = thue_morse(ri + rj) if bi % 2 == 0 else (1 if (ri + rj) % 2 == 0 else -1)
            else:
                val = thue_morse(bi * block_size + ri + bj * block_size + rj)
            row.append(val)
        block.append(row)
    variants.append(block)
    
    return variants

def construct_hadamard_matrix(n=29):
    best_matrix = None
    best_det = 0.0
    
    variants = get_variant_matrices(n)
    
    # The winning config: T=6.0, cool=0.995, iters=7500
    for T, cool, iters in [(6.0, 0.995, 7500)]:
        local_best_matrix = None
        local_best_det = 0.0
        
        # Phase 1
        for variant_idx, variant in enumerate(variants):
            for seed in range(30):
                refined = sa_refine(variant, n, variant_idx * 30 + seed, iters, T, cool)
                d = det_fn(refined)
                if d > local_best_det:
                    local_best_det = d
                    local_best_matrix = refined
        
        # Phase 2
        for pert_pass in range(2):
            if local_best_matrix is not None:
                perturbed = perturb_matrix(local_best_matrix, num_flips=15)
                for seed in range(20):
                    refined = sa_refine(perturbed, n, 1000 + pert_pass * 20 + seed, iters, T, cool)
                    d = det_fn(refined)
                    if d > local_best_det:
                        local_best_det = d
                        local_best_matrix = refined
        
        if local_best_det > best_det:
            best_det = local_best_det
            best_matrix = local_best_matrix
    
    return best_matrix

def run_code():
    matrix = construct_hadamard_matrix(n=29)
    return (matrix,)

if __name__ == "__main__":
    m, = run_code()
    print(f"Det: {abs(np.linalg.det(m.astype(float))):.2e}")
# EVOLVE-BLOCK-END
# Fixed API for evaluator
def run_code():
    """
    Run the Hadamard matrix constructor for n=29.
    
    Returns:
        Tuple of (matrix,) where matrix is an (29, 29) array with entries ±1
    """
    matrix = construct_hadamard_matrix(n=29)
    return (matrix,)


if __name__ == "__main__":
    matrix = run_code()[0]
    print(f"Constructed Hadamard matrix of size {matrix.shape[0]}x{matrix.shape[1]}")
    # Calculate determinant for verification
    det_val = np.linalg.det(matrix.astype(float))
    print(f"Determinant: {abs(det_val):.2e}")
# Fixed API for evaluator
def run_code():
    """
    Run the Hadamard matrix constructor for n=29.
    
    Returns:
        Tuple of (matrix,) where matrix is an (29, 29) array with entries ±1
    """
    matrix = construct_hadamard_matrix(n=29)
    return (matrix,)


if __name__ == "__main__":
    matrix = run_code()[0]
    print(f"Constructed Hadamard matrix of size {matrix.shape[0]}x{matrix.shape[1]}")
    # Calculate determinant for verification
    det_val = np.linalg.det(matrix.astype(float))
    print(f"Determinant: {abs(det_val):.2e}")
# Fixed API for evaluator
def run_code():
    """
    Run the Hadamard matrix constructor for n=29.
    
    Returns:
        Tuple of (matrix,) where matrix is an (29, 29) array with entries ±1
    """
    matrix = construct_hadamard_matrix(n=29)
    return (matrix,)


if __name__ == "__main__":
    matrix = run_code()[0]
    print(f"Constructed Hadamard matrix of size {matrix.shape[0]}x{matrix.shape[1]}")
    # Calculate determinant for verification
    det_val = np.linalg.det(matrix.astype(float))
    print(f"Determinant: {abs(det_val):.2e}")
# Fixed API for evaluator
def run_code():
    """
    Run the Hadamard matrix constructor for n=29.
    
    Returns:
        Tuple of (matrix,) where matrix is an (29, 29) array with entries ±1
    """
    matrix = construct_hadamard_matrix(n=29)
    return (matrix,)


if __name__ == "__main__":
    matrix = run_code()[0]
    print(f"Constructed Hadamard matrix of size {matrix.shape[0]}x{matrix.shape[1]}")
    # Calculate determinant for verification
    det_val = np.linalg.det(matrix.astype(float))
    print(f"Determinant: {abs(det_val):.2e}")
# Fixed API for evaluator
def run_code():
    """
    Run the Hadamard matrix constructor for n=29.
    
    Returns:
        Tuple of (matrix,) where matrix is an (29, 29) array with entries ±1
    """
    matrix = construct_hadamard_matrix(n=29)
    return (matrix,)


if __name__ == "__main__":
    matrix = run_code()[0]
    print(f"Constructed Hadamard matrix of size {matrix.shape[0]}x{matrix.shape[1]}")
    # Calculate determinant for verification
    det_val = np.linalg.det(matrix.astype(float))
    print(f"Determinant: {abs(det_val):.2e}")
# Fixed API for evaluator
def run_code():
    """
    Run the Hadamard matrix constructor for n=29.
    
    Returns:
        Tuple of (matrix,) where matrix is an (29, 29) array with entries ±1
    """
    matrix = construct_hadamard_matrix(n=29)
    return (matrix,)


if __name__ == "__main__":
    matrix = run_code()[0]
    print(f"Constructed Hadamard matrix of size {matrix.shape[0]}x{matrix.shape[1]}")
    # Calculate determinant for verification
    det_val = np.linalg.det(matrix.astype(float))
    print(f"Determinant: {abs(det_val):.2e}")
# Fixed API for evaluator
def run_code():
    """
    Run the Hadamard matrix constructor for n=29.
    
    Returns:
        Tuple of (matrix,) where matrix is an (29, 29) array with entries ±1
    """
    matrix = construct_hadamard_matrix(n=29)
    return (matrix,)


if __name__ == "__main__":
    matrix = run_code()[0]
    print(f"Constructed Hadamard matrix of size {matrix.shape[0]}x{matrix.shape[1]}")
    # Calculate determinant for verification
    det_val = np.linalg.det(matrix.astype(float))
    print(f"Determinant: {abs(det_val):.2e}")
# Fixed API for evaluator
def run_code():
    """
    Run the Hadamard matrix constructor for n=29.
    
    Returns:
        Tuple of (matrix,) where matrix is an (29, 29) array with entries ±1
    """
    matrix = construct_hadamard_matrix(n=29)
    return (matrix,)


if __name__ == "__main__":
    matrix = run_code()[0]
    print(f"Constructed Hadamard matrix of size {matrix.shape[0]}x{matrix.shape[1]}")
    # Calculate determinant for verification
    det_val = np.linalg.det(matrix.astype(float))
    print(f"Determinant: {abs(det_val):.2e}")
# Fixed API for evaluator
def run_code():
    """
    Run the Hadamard matrix constructor for n=29.
    
    Returns:
        Tuple of (matrix,) where matrix is an (29, 29) array with entries ±1
    """
    matrix = construct_hadamard_matrix(n=29)
    return (matrix,)


if __name__ == "__main__":
    matrix = run_code()[0]
    print(f"Constructed Hadamard matrix of size {matrix.shape[0]}x{matrix.shape[1]}")
    # Calculate determinant for verification
    det_val = np.linalg.det(matrix.astype(float))
    print(f"Determinant: {abs(det_val):.2e}")
# Fixed API for evaluator
def run_code():
    """
    Run the Hadamard matrix constructor for n=29.
    
    Returns:
        Tuple of (matrix,) where matrix is an (29, 29) array with entries ±1
    """
    matrix = construct_hadamard_matrix(n=29)
    return (matrix,)


if __name__ == "__main__":
    matrix = run_code()[0]
    print(f"Constructed Hadamard matrix of size {matrix.shape[0]}x{matrix.shape[1]}")
    # Calculate determinant for verification
    det_val = np.linalg.det(matrix.astype(float))
    print(f"Determinant: {abs(det_val):.2e}")
# Fixed API for evaluator
def run_code():
    """
    Run the Hadamard matrix constructor for n=29.
    
    Returns:
        Tuple of (matrix,) where matrix is an (29, 29) array with entries ±1
    """
    matrix = construct_hadamard_matrix(n=29)
    return (matrix,)


if __name__ == "__main__":
    matrix = run_code()[0]
    print(f"Constructed Hadamard matrix of size {matrix.shape[0]}x{matrix.shape[1]}")
    # Calculate determinant for verification
    det_val = np.linalg.det(matrix.astype(float))
    print(f"Determinant: {abs(det_val):.2e}")
# Fixed API for evaluator
def run_code():
    """
    Run the Hadamard matrix constructor for n=29.
    
    Returns:
        Tuple of (matrix,) where matrix is an (29, 29) array with entries ±1
    """
    matrix = construct_hadamard_matrix(n=29)
    return (matrix,)


if __name__ == "__main__":
    matrix = run_code()[0]
    print(f"Constructed Hadamard matrix of size {matrix.shape[0]}x{matrix.shape[1]}")
    # Calculate determinant for verification
    det_val = np.linalg.det(matrix.astype(float))
    print(f"Determinant: {abs(det_val):.2e}")
# Fixed API for evaluator
def run_code():
    """
    Run the Hadamard matrix constructor for n=29.
    
    Returns:
        Tuple of (matrix,) where matrix is an (29, 29) array with entries ±1
    """
    matrix = construct_hadamard_matrix(n=29)
    return (matrix,)


if __name__ == "__main__":
    matrix = run_code()[0]
    print(f"Constructed Hadamard matrix of size {matrix.shape[0]}x{matrix.shape[1]}")
    # Calculate determinant for verification
    det_val = np.linalg.det(matrix.astype(float))
    print(f"Determinant: {abs(det_val):.2e}")
