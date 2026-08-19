def run(ctx, args):
    import numpy as np
    num_marks = args.get("num_marks", 5)
    num_buckets = 200
    domain = 2.0
    
    def compute_c5(marks):
        N = 800
        dx = domain / N
        h = np.zeros(N)
        for m in marks:
            idx = int(m * N)
            h[idx] = 1.0
        j = 1.0 - h
        h_padded = np.pad(h, (0, N))
        j_padded = np.pad(j, (0, N))
        corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
        correlation = np.fft.ifft(corr_fft).real
        c5 = np.max(correlation * dx)
        return c5
    
    # Greedy hill climbing
    marks = [domain * i / (num_buckets - 1) for i in range(num_marks)]
    best_marks = marks[:]
    best_c5 = compute_c5(best_marks)
    
    improved = True
    while improved:
        improved = False
        new_marks = best_marks[:]
        for i in range(len(best_marks)):
            for delta in [-1, 1]:
                new_idx = int(best_marks[i] * num_buckets) + delta
                if new_idx == 0 or new_idx >= num_buckets:
                    continue
                new_marks[i] = domain * new_idx / (num_buckets - 1)
                c5 = compute_c5(new_marks)
                if c5 < best_c5:
                    best_c5 = c5
                    best_marks = new_marks[:]
                    improved = True
                    break
            if improved:
                break
    
    return {
        "marks": [float(m) for m in best_marks],
        "c5_bound": float(best_c5),
        "num_marks": num_marks
    }