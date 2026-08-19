# EVOLVE-BLOCK-START
"""Constructor-based Hadamard matrix optimization for n=29 - 20 RESTARTS"""
import numpy as np
import random

# CORRECT Quadratic residues mod 29 (Legendre symbol)
QUADRATIC_RESIDUES_29 = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}

# Use 20 restarts as upper bound of requirement
NUM_RESTARTS = 20
MAX_ITERS = 15000
INITIAL_TEMP = 3.0
COOL_RATE = 0.9985


def construct_hadamard_matrix(n=29):
    """Fixed Paley + hill climbing with 20 restarts."""
    
    def det_bareiss(A):
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

    def hill_climb(A, seed=None):
        rng = random.Random(seed)
        size = len(A)
        current = [row.copy() for row in A]
        det_curr = det_bareiss(current)
        best_det = det_curr
        best_matrix = [row.copy() for row in current]
        T = INITIAL_TEMP
        
        for it in range(MAX_ITERS):
            i = rng.randrange(size)
            j = rng.randrange(size)
            old_val = current[i][j]
            current[i][j] = -old_val
            
            det_new = det_bareiss(current)
            delta = abs(det_new) - abs(det_curr)
            
            if delta >= 0:
                det_curr = det_new
                if abs(det_curr) > best_det:
                    best_det = det_curr
                    best_matrix = [row.copy() for row in current]
            else:
                if T > 1e-15 and rng.random() < np.exp(delta / T):
                    det_curr = det_new
                    if abs(det_curr) > best_det:
                        best_det = det_curr
                        best_matrix = [row.copy() for row in current]
                else:
                    current[i][j] = old_val
                T *= COOL_RATE

        return np.array(best_matrix), best_det

    def create_paley_correct(size):
        matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                diff = (i - j) % size
                row.append(1 if diff in QUADRATIC_RESIDUES_29 else -1)
            matrix.append(row)
        return matrix

    best_result = None
    best_det = 0
    
    for seed in range(NUM_RESTARTS):
        start_matrix = create_paley_correct(n)
        result, det_val = hill_climb(start_matrix, seed=seed)
        if abs(det_val) > best_det:
            best_det = det_val
            best_result = result
    
    return best_result


def run_code():
    matrix = construct_hadamard_matrix(n=29)
    return (matrix,)


if __name__ == "__main__":
    matrix = run_code()[0]
    print(f"Size: {matrix.shape[0]}x{matrix.shape[1]}")
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
