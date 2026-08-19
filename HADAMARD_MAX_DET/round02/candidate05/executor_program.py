# EVOLVE-BLOCK-START
"""Constructor-based Hadamard matrix optimization for n=29"""
import numpy as np
import random


def construct_hadamard_matrix(n=29):
    """
    Construct a Hadamard-like matrix of size n using optimization methods.
    
    Args:
        n: Matrix size (default 29)
        
    Returns:
        n x n matrix with entries +1 or -1
    """
    
    def det_bareiss(A):
        """Bareiss algorithm for exact integer determinant calculation."""
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

    def hill_climb_with_cooldown(A, max_iters=10000, seed=None, initial_temp=2.5, cool_rate=0.997):
        """Hill climbing with simulated annealing and exponential cooling."""
        rng = random.Random(seed)
        size = len(A)
        current_matrix = [row.copy() for row in A]
        det_curr = det_bareiss(current_matrix)
        best_det = det_curr
        best_matrix = [row.copy() for row in current_matrix]

        T = initial_temp
        
        for t in range(1, max_iters + 1):
            # Random flip
            i = rng.randrange(size)
            j = rng.randrange(size)
            old_val = current_matrix[i][j]
            current_matrix[i][j] = -old_val
            
            d_new = det_bareiss(current_matrix)
            
            # Accept or reject
            delta = abs(d_new) - abs(det_curr)
            
            if delta >= 0:
                # Accept if improvement
                det_curr = d_new
                if abs(det_curr) > abs(best_det):
                    best_det = det_curr
                    best_matrix = [row.copy() for row in current_matrix]
            else:
                # Accept with probability based on temperature
                if T > 0 and rng.random() < np.exp(delta / max(1.0, T)):
                    det_curr = d_new
                    if abs(det_curr) > abs(best_det):
                        best_det = det_curr
                        best_matrix = [row.copy() for row in current_matrix]
                else:
                    # Reject
                    current_matrix[i][j] = old_val
            
            # Cool down
            T *= cool_rate

        return np.array(best_matrix), best_det

    def create_paley_matrix(size):
        """Create Paley construction matrix using quadratic residues."""
        quadratic_residues = set()
        for i in range(1, size):
            quadratic_residues.add((i * i) % size)
        quadratic_residues.add(0)
        
        matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                diff = (i - j) % size
                if diff in quadratic_residues:
                    row.append(1)
                else:
                    row.append(-1)
            matrix.append(row)
        return matrix

    def create_random_matrix(size, seed):
        """Create random starting matrix."""
        rng = random.Random(seed)
        return np.random.choice([-1, 1], size=(size, size)).tolist()

    # Try multiple seeds with different constructions
    best_result = None
    best_det = 0
    
    # Method 1: Paley with different seeds
    for seed in [42, 100, 200, 300, 400, 500, 600, 700, 800, 900]:
        start_matrix = create_paley_matrix(n)
        result, det_val = hill_climb_with_cooldown(start_matrix, max_iters=10000, seed=seed, initial_temp=2.5, cool_rate=0.997)
        if abs(det_val) > best_det:
            best_det = det_val
            best_result = result
    
    # Method 2: Random starts
    for seed in [1000, 1100, 1200, 1300]:
        start_matrix = create_random_matrix(n, seed)
        result, det_val = hill_climb_with_cooldown(start_matrix, max_iters=10000, seed=seed, initial_temp=2.5, cool_rate=0.997)
        if abs(det_val) > best_det:
            best_det = det_val
            best_result = result
    
    return best_result if best_result is not None else create_paley_matrix(n)


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
