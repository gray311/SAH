# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
from dataclasses import dataclass
from typing import Tuple


@dataclass
class OptimizerHyperparameters:
    """Same structure as original baseline."""
    num_intervals: int = 600
    learning_rate: float = 0.15
    num_steps: int = 10000  # Reduced for faster testing
    best_c2: float = 0.8962799441554086
    stagnation_window: int = 100


def compute_c2_raw(f_vals):
    """Direct C2 computation returning a float."""
    f_clean = jnp.maximum(0.0, f_vals)
    N = len(f_clean)
    pad_len = 4 * N
    padded = jnp.pad(f_clean, (0, pad_len))
    fft_padded = jnp.fft.fft(padded)
    convolution = jnp.fft.ifft(fft_padded * fft_padded).real
    
    # Compute L2 norm with trapezoidal rule
    num_points = len(convolution)
    h = 1.0 / (num_points)
    y_points = jnp.concatenate([jnp.array([0.0]), convolution, jnp.array([0.0])])
    y1, y2 = y_points[:-1], y_points[1:]
    l2_squared = jnp.sum((h / 3) * (y1**2 + y1 * y2 + y2**2))
    
    norm_1 = jnp.sum(jnp.abs(convolution)) / (len(convolution) + 1)
    norm_inf = jnp.max(jnp.abs(convolution))
    denominator = norm_1 * norm_inf
    
    c2_result = l2_squared / denominator
    return float(c2_result) if denominator > 1e-15 else 0.0


def create_optimized_pattern(n: int, pattern_type: str) -> jnp.ndarray:
    """Create initial functions of different architectural families."""
    f = jnp.zeros(n)
    
    if pattern_type == "step_basic":
        # Refined baseline step pattern
        left_edge = int(0.22 * n)
        right_edge = int(0.68 * n)
        center_start = int(0.35 * n)
        center_end = int(0.65 * n)
        
        f = f.at[left_edge:center_start].set(1.50)
        f = f.at[center_start:center_end].set(2.15)
        f = f.at[center_end:right_edge].set(1.50)
        f = f.at[:left_edge].set(0.90)
        f = f.at[right_edge:].set(0.90)
    
    elif pattern_type == "step_wider_peak":
        # Wider high-peak
        mid_start = int(0.28 * n)
        mid_end = int(0.72 * n)
        f = f.at[:mid_start].set(1.0)
        f = f.at[mid_start:mid_end].set(2.80)
        f = f.at[mid_end:].set(1.0)
    
    elif pattern_type == "step_multipeak":
        # Multiple peaks pattern
        f = f.at[int(0.15*n):int(0.22*n)].set(1.10)
        f = f.at[int(0.22*n):int(0.28*n)].set(2.70)
        f = f.at[int(0.35*n):int(0.41*n)].set(2.70)
        f = f.at[int(0.48*n):int(0.54*n)].set(2.70)
        f = f.at[int(0.61*n):int(0.67*n)].set(2.70)
        f = f.at[int(0.74*n):int(0.81*n)].set(2.70)
        f = f.at[:int(0.15*n)].set(1.10)
        for i in range(len(f)):
            if 0 <= i < int(0.15*n) or int(0.28*n) <= i < int(0.35*n) or int(0.41*n) <= i < int(0.48*n):
                f = f.at[i].set(1.10)
    
    return f


def run():
    """
    Replicates baseline signature.
    Returns: f_np_array, c2_float, negative_c2_float, n_points_int
    """
    hypers = OptimizerHyperparameters()
    n = hypers.num_intervals
    
    # Test all three pattern architectures
    all_results = []
    names = ["step_basic", "step_wider_peak", "step_multipeak"]
    
    for pat_name in names:
        pattern = create_optimized_pattern(n, pat_name)
        c2_val = compute_c2_raw(pattern)
        f_np = jnp.array(pattern)
        combined = c2_val / hypers.best_c2
        all_results.append({
            'name': pat_name,
            'f': f_np,
            'c2': c2_val,
            'combined': combined
        })
        
        print(f"\nArchitectures Tested in this program ({pat_name}):")
        print(f"  - {pat_name}")
        print(f"    C2={c2_val:.8f}")
        print(f"    combined_score = {combined:.4f}")
    
    # Find best pattern
    best = max(all_results, key=lambda x: x['c2'])
    
    print(f"\n{'='*60}")
    print(f"RESULT SUMMARY:")
    print(f"{'='*60}")
    print(f"Best Pattern: {best['name']}")
    print(f"Best C2: {best['c2']:.8f}")
    print(f"Best combined_score: {best['combined']:.4f}")
    
    # Return tuple matching baseline signature
    return (best['f'], best['c2'], -best['c2'], n)


if __name__ == "__main__":
    f_val, c2_val, loss_val, n_pts = run()
    print(f"\nFinal Output:")
    print(f"  Function shape: {f_val.shape}")
    print(f"  C2: {c2_val:.6f}")
    print(f"  Combined score vs baseline: {c2_val/0.8962799441554086:.4f}")
# EVOLVE-BLOCK-END
