def run(ctx, args):
    import numpy as np
    strategy = args.get("strategy", "threshold")
    position = args.get("position", 0.5)
    
    N = 800
    domain = 2.0
    dx = domain / N
    
    if strategy == "threshold":
        p = max(0.1, min(1.9, float(position)))
        h = np.zeros(N)
        h_end = int(p * N)
        h[:h_end] = 1.0 / p
    
    elif strategy == "two_threshold":
        if isinstance(position, list):
            a, b = min(float(position[0]), float(position[1])), max(float(position[0]), float(position[1]))
        else:
            a, b = float(position) * 0.3, float(position) * 0.7
        a, b = max(0.05, min(a, 1.5)), max(0.5, min(b, 1.95))
        if a >= b:
            a, b = b, a
        h = np.zeros(N)
        h[:int(a * N)] = 1.0
        h[int(b * N):] = 1.0
        total = 2 * (a * N) + (2 - 2 * a)
        if total > 0:
            scale = 1.0 / total
            h[:int(a * N)] *= scale
            h[int(b * N):] *= scale
        else:
            h = np.ones(N) / N
    
    elif strategy == "symmetric":
        a = max(0.1, min(0.9, float(position)))
        h = np.zeros(N)
        left_end = int(a * N)
        right_start = int((2 - a) * N)
        h[:left_end] = 1.0
        h[right_start:] = 1.0
        mass = left_end + (N - right_start)
        if mass > 0:
            h = h / mass
        else:
            h = np.ones(N) / N
    
    elif strategy == "multi_peak":
        h = np.zeros(N)
        if isinstance(position, (int, float)):
            pk1, pk2 = position - 0.3, position + 0.3
        else:
            pk1, pk2 = position[0], position[1]
        for pk in [pk1, pk2]:
            left = max(0, int((pk - 0.2) * N))
            right = min(N, int((pk + 0.2) * N))
            h[left:right] = 1.0
        mass = np.sum(h) * dx
        if mass > 0:
            h = h / (mass / 2.0)
            h = np.clip(h, 0, 1)
        else:
            h = np.ones(N) / N
    
    program_lines = []
    program_lines.append('import jax')
    program_lines.append('import jax.numpy as jnp')
    program_lines.append('from dataclasses import dataclass')
    program_lines.append('')
    program_lines.append('N = ' + str(N))
    program_lines.append('dx = 2.0 / N')
    program_lines.append('')
    program_lines.append('h = jnp.array(' + str(h.tolist()) + ')')
    program_lines.append('total = float(jnp.sum(h) * dx)')
    program_lines.append('if abs(total - 1.0) > 0.01:')
    program_lines.append('    h = h * (1.0 / total)')
    program_lines.append('    h = jnp.clip(h, 0, 1)')
    program_lines.append('')
    program_lines.append('print(f"Integral check: {{total:.4f}}")')
    program_lines.append('print(f"h range: [{{h.min():.4f}}, {{h.max():.4f}}]")')
    program_lines.append('')
    program_lines.append('h_padded = jnp.pad(h, (0, N))')
    program_lines.append('j_val = jnp.pad(1.0 - h, (0, N))')
    program_lines.append('corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_val))')
    program_lines.append('correlation = jnp.fft.ifft(corr_fft).real')
    program_lines.append('c5_bound = float(jnp.max(correlation * dx))')
    program_lines.append('print(f"c5_bound: {{c5_bound:.8f}}")')
    program_lines.append('')
    program_lines.append('print("Step function constructed successfully")')
    
    return {"program": "\n".join(program_lines), "strategy": strategy, "position": position}
