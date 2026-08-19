def run(ctx, args):
    import numpy as np
    N = 800
    
    def make_step():
        h = np.zeros(N)
        h[0:400] = 1.0
        h[400:800] = 0.0
        h = h / (np.sum(h) * 2.0 / N)
        return h
    
    def make_sin():
        x = np.linspace(0, 2, N)
        latent = np.sin(3 * np.pi * x) * 0.8 + np.cos(5 * np.pi * x) * 0.4
        h = 1.0 / (1.0 + np.exp(-latent))
        h = h / (np.sum(h) * 2.0 / N)
        return h
    
    def make_piecewise():
        h = np.zeros(N)
        heights = [0.9, 0.2, 0.3, 0.1, 0.5]
        for i, hi in enumerate(heights):
            s = int(i * N / 5)
            e = int((i + 1) * N / 5)
            h[s:e] = hi
        h = h / (np.sum(h) * 2.0 / N)
        return h
    
    def make_ga():
        np.random.seed(42)
        pop_size = 20
        
        def random_h():
            return np.clip(np.random.uniform(0, 2, N) - 1.0, 0.0, 1.0)
        
        pop = [random_h() for _ in range(pop_size)]
        
        def fitness(h):
            j_part = 1.0 - h
            h_p = np.concatenate([h, h])
            j_p = np.concatenate([j_part, j_part])
            corr = np.fft.ifft(np.fft.fft(h_p) * np.conj(np.fft.fft(j_p))).real
            c5 = np.max(corr) * 2.0 / N
            int_h = np.sum(h) * 2.0 / N
            return (1.0 - c5) * (1.0 + 0.1 * abs(int_h - 1.0))
        
        best_h, best_score = pop[0], fitness(pop[0])
        
        for _ in range(50):
            selected = []
            for _ in range(pop_size):
                a, b = np.random.choice(pop_size, 2, replace=False)
                selected.append(pop[a] if fitness(pop[a]) > fitness(pop[b]) else pop[b])
            pop = selected
            for i in range(len(pop)):
                pop[i] = np.clip(pop[i] + np.random.normal(0, 0.1, N), 0.0, 1.0)
            for h in pop:
                if fitness(h) > best_score:
                    best_score = fitness(h)
                    best_h = h
        return best_h / (np.sum(best_h) * 2.0 / N)
    
    def make_sa():
        np.random.seed(123)
        h = np.clip(np.random.uniform(0, 2, N) - 1.0, 0.0, 1.0)
        
        def fitness(h):
            j_part = 1.0 - h
            h_p = np.concatenate([h, h])
            j_p = np.concatenate([j_part, j_part])
            corr = np.fft.ifft(np.fft.fft(h_p) * np.conj(np.fft.fft(j_p))).real
            c5 = np.max(corr) * 2.0 / N
            int_h = np.sum(h) * 2.0 / N
            return (1.0 - c5) - 100.0 * abs(int_h - 1.0) ** 2
        
        best_h, best_score = h.copy(), fitness(h)
        temp = 10.0
        for _ in range(5000):
            noise = np.random.normal(0, 0.02, N)
            h_new = np.clip(h + noise, 0.0, 1.0)
            score_new = fitness(h_new)
            if score_new > best_score or np.random.uniform() < np.exp((score_new - fitness(h)) / temp):
                h = h_new
                if score_new > best_score:
                    best_score = score_new
                    best_h = h.copy()
            temp *= 0.998
        return best_h / (np.sum(best_h) * 2.0 / N)
    
    return {"candidates": ["make_step()", "make_sin()", "make_piecewise()", "make_ga()", "make_sa()"],
            "note": "5 diverse strategies implemented: step-function, sinusoidal, piecewise-constant, genetic-algorithm, simulated-annealing"}