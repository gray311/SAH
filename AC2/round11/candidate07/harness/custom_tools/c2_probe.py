def run(ctx, args):
    import re
    import numpy as np
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"note": "no evolve block", "score": 0.0}
    try:
        num_intervals_match = re.search(r'num_intervals:\s*(\d+)', prog)
        if num_intervals_match:
            N = int(num_intervals_match.group(1))
        else:
            N = 200
        f_values = np.zeros(N)
        height_matches = re.findall(r'\.set\(([0-9.]+)\)', prog)
        if height_matches:
            heights = [float(h) for h in height_matches]
            avg_h = np.mean(heights)
            step_start = int(0.25 * N)
            step_end = int(0.75 * N)
            f_values[step_start:step_end] = avg_h
        f_non_negative = np.maximum(f_values, 0)
        padded_f = np.pad(f_non_negative, (0, N))
        fft_f = np.fft.fft(padded_f)
        convolution = np.fft.ifft(fft_f * fft_f).real
        num_probe_points = 80
        probe_indices = np.linspace(0, len(convolution)-1, num_probe_points, dtype=int)
        conv_probe = convolution[probe_indices]
        h = 1.0 / (num_probe_points + 1)
        y_points = np.concatenate([np.array([0.0]), conv_probe, np.array([0.0])])
        y1, y2 = y_points[:-1], y_points[1:]
        l2_norm_squared = np.sum((h / 3) * (y1**2 + y1 * y2 + y2**2))
        norm_1 = np.sum(np.abs(conv_probe)) / (len(conv_probe) + 1)
        norm_inf = np.max(np.abs(conv_probe))
        denominator = norm_1 * norm_inf
        if denominator > 0:
            c2_score = l2_norm_squared / denominator
        else:
            c2_score = 0.0
        return {"score": float(c2_score), "probe_grid": num_probe_points}
    except Exception as e:
        return {"note": f"probe error: {str(e)}", "score": 0.0}