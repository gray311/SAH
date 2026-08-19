def run(ctx, args):
    import numpy as np
    import re
    matrix_text = ctx.get_best_program()
    try:
        lines = matrix_text.split('\n')
        det_val = None
        for line in lines:
            if 'Det:' in line or 'Determinant' in line:
                match = re.search(r'Det:\s*([-\d.]+)', line, re.IGNORECASE)
                if match:
                    det_val = float(match.group(1))
                    break
        if det_val is None:
            det_val = ctx.best_score()
        if det_val is None:
            return {"error": "Cannot determine matrix or determinant"}
        n = 29
        return {
            "det_estimate": det_val,
            "matrix_size": [n, n],
            "row_count": n,
            "column_count": n,
            "quality_assessment": "Check if |det| > 10^10 for good Hadamard approximation",
            "recommended_next_steps": [
                "If det < 10^10: try different seed or longer annealing",
                "If det > 10^12: you are doing well, consider fine-tuning",
                "Look for row pairs with correlation > 0.1 to mutate"
            ],
            "note": "Full matrix analysis requires matrix array access. Use this for guidance."
        }
    except Exception as e:
        return {"error": str(e), "note": "Analysis failed, try again"}
