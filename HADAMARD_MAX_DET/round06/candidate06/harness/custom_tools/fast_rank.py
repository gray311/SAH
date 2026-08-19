def run(ctx, args):
    import numpy as np
    if "matrix" not in args or len(args["matrix"]) != 29:
        return {"error": "Invalid matrix input"}
    mat = np.array(args["matrix"], dtype=float)
    if mat.shape != (29, 29):
        return {"error": "Matrix must be 29x29"}
    det_val = abs(np.linalg.det(mat))
    return {"det_value": float(det_val)}
