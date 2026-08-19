def run(ctx, args):
    import numpy as np
    import math
    
    num_steps = args.get("num_steps", 5)
    step_locations = args.get("step_locations", None)
    temperature = args.get("temperature", 0.5)
    
    domain = 2.0
    N = 800
    dx = domain / N
    
    if step_locations is None:
        # Default: evenly spaced steps
        step_locations = [i * domain / num_steps for i in range(num_steps + 1)]
    
    # Ensure locations are in [0, 2]
    step_locations = [max(0.0, min(2.0, loc)) for loc in step_locations]
    step_locations = sorted(list(set(step_locations)))
    
    # Generate step values that sum to 1 over [0, 2]
    # Create a step function by sampling at midpoints of intervals
    def create_step_function(values, locations):
        h = np.zeros(N)
        cumulative_width = 0.0
        prev_val = 0.0
        for i in range(len(locations) - 1):
            mid = (locations[i] + locations[i+1]) / 2.0
            interval_width = locations[i+1] - locations[i]
            idx_start = int(mid / dx)
            idx_end = int((mid + 0.5 * dx) / dx)
            if idx_end > idx_start:
                count = idx_end - idx_start
                h[idx_start:idx_end] = values[i]
        return h
    
    # Try multiple random value assignments and pick the one closest to integral=1
    best_values = None
    best_error = float("inf")
    
    for _ in range(100):
        # Sample step values from a distribution
        if temperature > 0:
            sampled = np.random.uniform(-1.0, 2.0, num_steps) * temperature
        else:
            sampled = np.ones(num_steps) / 3.0
        
        # Normalize to satisfy integral constraint approximately
        total = np.sum(sampled)
        if total > 0:
            normalized = sampled / total
            # Check integral
            integral_approx = np.sum(normalized) * domain / num_steps
            error = abs(integral_approx - 1.0)
            if error < best_error:
                best_error = error
                best_values = normalized.tolist()
    
    # Ensure integral is exactly 1 by scaling
    if best_values is not None:
        best_values = np.array(best_values)
        current_integral = np.sum(best_values)
        if current_integral > 0:
            best_values = best_values / current_integral
        else:
            best_values = np.ones(num_steps) / num_steps
    
    # Convert to step function on N intervals
    h_arr = np.zeros(N)
    for i in range(num_steps):
        start_loc = step_locations[i]
        end_loc = step_locations[i+1] if i < num_steps else 2.0
        if end_loc <= start_loc:
            continue
        start_idx = int(start_loc / dx)
        end_idx = int(end_loc / dx)
        if end_idx > start_idx:
            h_arr[start_idx:end_idx] = best_values[i]
    
    # Compute C5 bound via FFT
    h_padded = np.pad(h_arr, (0, N))
    j_padded = np.pad(1.0 - h_arr, (0, N))
    corr = np.fft.ifft(np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))).real
    c5_bound = np.max(corr * dx)
    
    # Clamp h to [0, 1]
    h_arr = np.clip(h_arr, 0.0, 1.0)
    
    # Recompute C5 with clamped values
    h_padded = np.pad(h_arr, (0, N))
    j_padded = np.pad(1.0 - h_arr, (0, N))
    corr = np.fft.ifft(np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))).real
    c5_bound = np.max(corr * dx)
    
    candidates = [{
        "h": h_arr.tolist(),
        "num_steps": num_steps,
        "step_locations": step_locations,
        "step_values": best_values.tolist() if best_values is not None else [1.0/num_steps]*num_steps,
        "c5_bound": float(c5_bound),
        "integral": float(np.sum(h_arr) * dx),
        "architecture": f"{num_steps} steps at locations {step_locations}"
    }]
    
    return {"candidates": candidates, "num_candidates": 1}