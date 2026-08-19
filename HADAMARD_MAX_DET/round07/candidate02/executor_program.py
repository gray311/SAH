# EVOLVE-BLOCK-START
"""Multi-chain SA: Final attempt - ultra-aggressive refinement"""
import numpy as np
import random

def construct_hadamard_matrix(n=29, iterations_per_chain=5000):
    def det_fn(A):
        return abs(np.linalg.det(np.array(A, dtype=float)))
    
    def sa_run(start_mat, iters, T, cool_rate, seed):
        rng = random.Random(seed)
        cur = [row[:] for row in start_mat]
        best = cur[:]
        cd = det_fn(cur)
        bd = cd
        T_val = T
        
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
    
    # Generate Paley from quadratic residues
    QR = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
    paley = [[1 if (i-j)%n in QR else -1 for j in range(n)] for i in range(n)]
    
    def create_perturbed_paley(paly, num_flips, seed):
        rng = random.Random(seed)
        cur = [row[:] for row in paly]
        flip_positions = rng.sample([(i, j) for i in range(n) for j in range(n)], num_flips)
        for r, c in flip_positions:
            cur[r][c] *= -1
        return cur
    
    def create_random_matrix(seed):
        rng = random.Random(seed)
        return [[rng.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    
    best_matrix = None
    best_det = 0.0
    
    # Chain 1: Perturbed Paley 5 flips
    mat1 = create_perturbed_paley(paley, 5, 1)
    res1 = sa_run(mat1, iterations_per_chain, T=3.0, cool_rate=0.995, seed=100)
    d1 = det_fn(res1)
    if d1 > best_det: best_det, best_matrix = d1, res1
    
    # Chain 2: Perturbed Paley 10 flips
    mat2 = create_perturbed_paley(paley, 10, 2)
    res2 = sa_run(mat2, iterations_per_chain, T=3.0, cool_rate=0.995, seed=200)
    d2 = det_fn(res2)
    if d2 > best_det: best_det, best_matrix = d2, res2
    
    # Chain 3: Perturbed Paley 15 flips
    mat3 = create_perturbed_paley(paley, 15, 3)
    res3 = sa_run(mat3, iterations_per_chain, T=3.0, cool_rate=0.995, seed=300)
    d3 = det_fn(res3)
    if d3 > best_det: best_det, best_matrix = d3, res3
    
    # Chain 4: Random moderate
    mat4 = create_random_matrix(4)
    res4 = sa_run(mat4, iterations_per_chain, T=5.0, cool_rate=0.997, seed=400)
    d4 = det_fn(res4)
    if d4 > best_det: best_det, best_matrix = d4, res4
    
    # Chain 5: Random aggressive
    mat5 = create_random_matrix(5)
    res5 = sa_run(mat5, iterations_per_chain, T=15.0, cool_rate=0.998, seed=500)
    d5 = det_fn(res5)
    if d5 > best_det: best_det, best_matrix = d5, res5
    
    # Chain 6: Original Paley
    mat6 = [row[:] for row in paley]
    res6 = sa_run(mat6, iterations_per_chain, T=3.0, cool_rate=0.997, seed=600)
    d6 = det_fn(res6)
    if d6 > best_det: best_det, best_matrix = d6, res6
    
    # Ultra-aggressive refinement: 30 passes with extreme cooling
    if best_matrix is not None:
        best_matrix_float = [row[:] for row in best_matrix]
        
        # 30 refinement passes with progressively extreme cooling
        refinement_configs = [
            (700, 2.0, 0.998), (800, 1.5, 0.9985), (900, 1.0, 0.999),
            (1000, 0.8, 0.9992), (1100, 0.5, 0.9995), (1200, 0.3, 0.9998),
            (1300, 0.2, 0.9999), (1400, 0.15, 0.99995), (1500, 0.1, 0.99998),
            (1600, 0.08, 0.99999), (1700, 0.06, 0.999995), (1800, 0.04, 0.999998),
            (1900, 0.03, 0.999999), (2000, 0.02, 0.9999995), (2100, 0.01, 0.9999999),
            (2200, 0.008, 0.99999995), (2300, 0.006, 0.99999999), (2400, 0.005, 0.999999995),
            (2500, 0.004, 0.999999998), (2600, 0.003, 0.999999999), (2700, 0.002, 0.9999999995),
            (2800, 0.0015, 0.9999999998), (2900, 0.001, 0.9999999999), (3000, 0.0008, 0.99999999995)
        ]
        
        for ref_seed, T_val, cool_val in refinement_configs:
            res_ref = sa_run(best_matrix_float, iterations_per_chain, T=T_val, cool_rate=cool_val, seed=ref_seed)
            d_ref = det_fn(res_ref)
            if d_ref > best_det: best_det, best_matrix = d_ref, res_ref
    
    return np.array(best_matrix, dtype=int)

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
