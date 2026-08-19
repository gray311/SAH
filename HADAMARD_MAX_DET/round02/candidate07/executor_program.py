# EVOLVE-BLOCK-START
"""Final attempt with extended search and diverse configurations"""
import numpy as np
import random
import time


def construct_hadamard_matrix(n=29):
    """
    Construct Hadamard-like matrix using Paley construction with extended search.
    """
    
    QR = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
    
    def build_paley_matrix():
        matrix = []
        for i in range(n):
            row = []
            for j in range(n):
                diff = (i - j) % n
                row.append(1 if diff in QR else -1)
            matrix.append(row)
        return matrix
    
    def det_bareiss(A):
        """Bareiss algorithm for exact determinant."""
        size = len(A)
        if size == 0:
            return 1
        M = [row.copy() for row in A]
        for k in range(size - 1):
            if M[k][k] == 0:
                for i in range(k + 1, size):
                    if M[i][k] != 0:
                        M[k], M[i] = M[i], M[k]
                        break
                else:
                    return 0
            for i in range(k + 1, size):
                for j in range(k + 1, size):
                    num = M[i][j] * M[k][k] - M[i][k] * M[k][j]
                    den = M[k - 1][k - 1] if k > 0 else 1
                    M[i][j] = num // den
        return M[-1][-1]
    
    def hill_climb_with_cooldown(A, max_iters=12000, seed=None, initial_temp=2.5, cool_rate=0.997):
        """Hill climbing with simulated annealing and exponential cooling."""
        rng = random.Random(seed)
        size = len(A)
        current_matrix = [row.copy() for row in A]
        det_curr = det_bareiss(current_matrix)
        best_det = det_curr
        best_matrix = [row.copy() for row in current_matrix]

        T = initial_temp
        
        for t in range(1, max_iters + 1):
            i = rng.randrange(size)
            j = rng.randrange(size)
            old_val = current_matrix[i][j]
            current_matrix[i][j] = -old_val
            
            d_new = det_bareiss(current_matrix)
            
            delta = abs(d_new) - abs(det_curr)
            
            if delta >= 0:
                det_curr = d_new
                if abs(det_curr) > abs(best_det):
                    best_det = det_curr
                    best_matrix = [row.copy() for row in current_matrix]
            else:
                if T > 0 and rng.random() < np.exp(delta / max(1.0, T)):
                    det_curr = d_new
                    if abs(det_curr) > abs(best_det):
                        best_det = det_curr
                        best_matrix = [row.copy() for row in current_matrix]
                else:
                    current_matrix[i][j] = old_val
            
            T *= cool_rate

        return np.array(best_matrix), best_det

    def create_perturbed_matrix(base, seed, n_flips=5):
        """Create perturbed version of base matrix."""
        rng = random.Random(seed)
        mat = [row[:] for row in base]
        for _ in range(n_flips):
            i = rng.randrange(n)
            j = rng.randrange(n)
            mat[i][j] *= -1
        return mat

    # Try multiple seeds with different constructions and perturbations
    best_result = None
    best_det = 0
    
    max_time = 180
    start_time = time.time()
    
    # Method 1: Extensive search with Paley perturbations
    for seed in range(15):
        if time.time() - start_time > max_time:
            break
        
        base = build_paley_matrix()
        perturbed = create_perturbed_matrix(base, seed=42000 + seed * 1000, n_flips=4)
        
        result, det_val = hill_climb_with_cooldown(perturbed, max_iters=12000, seed=42000 + seed * 1000, 
                                                   initial_temp=2.5, cool_rate=0.997)
        if abs(det_val) > best_det:
            best_det = det_val
            best_result = result
    
    # Method 2: Different temperature schedules
    if best_result is None and time.time() - start_time < max_time:
        for temp in [2.0, 2.5, 3.0]:
            if time.time() - start_time > max_time:
                break
            
            base = build_paley_matrix()
            perturbed = create_perturbed_matrix(base, seed=50000, n_flips=5)
            
            result, det_val = hill_climb_with_cooldown(perturbed, max_iters=10000, seed=50000, 
                                                       initial_temp=temp, cool_rate=0.997)
            if abs(det_val) > best_det:
                best_det = det_val
                best_result = result
    
    # Method 3: Unperturbed Paley with extended search
    if best_result is None and time.time() - start_time < max_time:
        base = build_paley_matrix()
        result, det_val = hill_climb_with_cooldown(base, max_iters=12000, seed=0, initial_temp=2.5, cool_rate=0.997)
        if abs(det_val) > best_det:
            best_det = det_val
            best_result = result
    
    return best_result if best_result is not None else build_paley_matrix()
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
