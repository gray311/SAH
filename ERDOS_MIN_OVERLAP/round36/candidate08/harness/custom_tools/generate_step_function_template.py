def run(ctx, args):
    import numpy as np
    template_type = args.get("template_type", "bipartite")
    num_intervals = args.get("num_intervals", 800)
    domain = 2.0
    dx = domain / num_intervals
    x = np.linspace(0, 2, num_intervals + 1)[0:num_intervals]
    h = np.zeros(num_intervals)
    
    if template_type == "bipartite":
        t = 0.5
        h = np.where(x < t, 1.0, 0.0)
    elif template_type == "multimodal_3peaks":
        peaks = np.array([0.5, 1.0, 1.5])
        widths = 0.15
        for p in peaks:
            mask = (x >= p - widths/2) & (x < p + widths/2)
            h = h + np.where(mask, 4.0, 0.0)
        h = np.clip(h, 0.0, 10.0)
        h = np.tanh(h / 2.0)
    elif template_type == "multimodal_5peaks":
        peaks = np.array([0.3, 0.7, 1.0, 1.3, 1.7])
        widths = 0.12
        for p in peaks:
            mask = (x >= p - widths/2) & (x < p + widths/2)
            h = h + np.where(mask, 5.0, 0.0)
        h = np.clip(h, 0.0, 10.0)
        h = np.tanh(h / 2.0)
    elif template_type == "golomb_ruler":
        marks = np.array([0.0, 0.4, 0.8, 1.2, 1.6])
        widths = 0.08
        for m in marks:
            mask = (x >= m - widths/2) & (x < m + widths/2)
            h = h + np.where(mask, 6.0, 0.0)
        h = np.clip(h, 0.0, 10.0)
        h = np.tanh(h / 2.0)
    elif template_type == "sinusoidal_threshold":
        a, b, c = 1.5, 2.0, -0.5
        h = 1.0 / (1.0 + np.exp(-(a * np.sin(2 * np.pi * x / b) + c)))
    elif template_type == "piecewise_constant":
        mid = num_intervals // 2
        h[:mid] = 2.0 / (mid * dx)
        h[mid:] = 0.0
        h = np.clip(h, 0.0, 1.0)
        
    integral = np.sum(h) * dx
    if integral > 1e-10:
        h = h * (1.0 / integral)
    h = np.clip(h, 0.0, 1.0)
    
    h_str = '[' + ','.join(f'{v:.10f}' for v in h) + ']'
    return {"h": h_str, "template_type": template_type, "num_intervals": num_intervals}
