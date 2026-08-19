def run(ctx, args):
    import numpy as np
    n = 29
    residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
    H = ctx.get_program()
    # Extract 10x10 submatrix from center
    start = (n - 10) // 2
    sub = np.array([[1 if ((i+start)-(j+start)) % n in residues else -1 
                    for j in range(n-10)] for i in range(n-10)])
    det_val = abs(np.linalg.det(sub.astype(float)))
    return {"sub_det": float(det_val), "expected_paley_10_det": 60.0,
            "valid": det_val > 0.1}
