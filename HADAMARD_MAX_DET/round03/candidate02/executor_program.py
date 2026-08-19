# EVOLVE-BLOCK-START
"""Optimized Hadamard matrix construction for n=29"""
import numpy as np
import random


def construct_hadamard_matrix(n=29):
    """
    Construct optimal Hadamard-like matrix of size n=29.
    Uses Paley construction with simulated annealing refinement.
    """
    
    def fast_det(A):
        """Fast determinant using numpy."""
        return abs(np.linalg.det(np.array(A, dtype=float)))
    
    def hill_climb_sa(A, max_iters=50000, seed=None, initial_temp=5.0, cool_rate=0.998):
        """Simulated annealing with fast numpy determinant."""
        rng = random.Random(seed)
        size = len(A)
        current_matrix = [row.copy() for row in A]
        current_det = fast_det(current_matrix)
        best_det = current_det
        best_matrix = [row.copy() for row in current_matrix]

        T = initial_temp
        
        for t in range(1, max_iters + 1):
            i = rng.randrange(size)
            j = rng.randrange(size)
            old_val = current_matrix[i][j]
            current_matrix[i][j] = -old_val
            
            new_det = fast_det(current_matrix)
            delta = new_det - current_det
            
            if delta >= 0:
                current_det = new_det
                if current_det > best_det:
                    best_det = current_det
                    best_matrix = [row.copy() for row in current_matrix]
            else:
                if T > 1e-10 and rng.random() < np.exp(delta / T):
                    current_det = new_det
                    if current_det > best_det:
                        best_det = current_det
                        best_matrix = [row.copy() for row in current_matrix]
                else:
                    current_matrix[i][j] = old_val
            
            T *= cool_rate

        return np.array(best_matrix, dtype=int), best_det

    def create_paley_matrix(size):
        """Create Paley matrix for n=29."""
        # Quadratic residues mod 29: {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
        quadratic_residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
        
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

    def run_sa(start_mat, seed, iters, temp, cool):
        result_mat, det_val = hill_climb_sa(start_mat, max_iters=iters, seed=seed, initial_temp=temp, cool_rate=cool)
        return result_mat, det_val

    palley_start = create_paley_matrix(n)
    
    best_det = 0
    best_mat = None
    
    # THE EXACT CONFIGURATION THAT WORKED: seed=42, temp=5.0, cool=0.998, iters=50000
    # Let's try more seeds with this EXACT same configuration
    
    # Many seeds with the winning parameters
    seed_offsets = list(range(0, 50))  # 50 different seeds
    seed_params = (5.0, 0.998, 50000)
    
    for idx in seed_offsets:
        seed = idx * 1000 + 42  # Different seeds with same params
        res_mat, det_val = run_sa(palley_start, seed, seed_params[2], seed_params[0], seed_params[1])
        if det_val > best_det:
            best_det = det_val
            best_mat = res_mat.copy()
    
    # Also try the original winning seed configuration
    res_mat, det_val = run_sa(palley_start, 42, 50000, 5.0, 0.998)
    if det_val > best_det:
        best_det = det_val
        best_mat = res_mat.copy()
    
    # Random starts with same params
    for si in range(3):
        rng = random.Random(si * 10000 + 2024)
        start_mat = np.random.choice([-1, 1], size=(n, n)).tolist()
        seed = 200000 + si
        res_mat, det_val = run_sa(start_mat, seed, 50000, 5.0, 0.998)
        if det_val > best_det:
            best_det = det_val
            best_mat = res_mat.copy()
    
    # Refinement
    if best_mat is not None:
        rng = random.Random(999999)
        start_mat = [[val for val in row] for row in best_mat]
        for _ in range(5):
            i = rng.randrange(n)
            j = rng.randrange(n)
            start_mat[i][j] *= -1
        
        res_mat, det_val = run_sa(start_mat, 300000, 30000, 4.5, 0.996)
        if det_val > best_det:
            best_det = det_val
            best_mat = res_mat.copy()
    
    return best_mat

def run_code():
    matrix = construct_hadamard_matrix(n=29)
    return (matrix, abs(np.linalg.det(matrix.astype(float))))

if __name__ == "__main__":
    matrix, det = run_code()
    print(f"Matrix shape: {matrix.shape}")
    print(f"Determinant: {det:.2e}")
    print(f"Ratio: {det / (29 * np.sqrt(29)):.4f}")
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
