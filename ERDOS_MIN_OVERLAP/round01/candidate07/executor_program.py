# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    num_intervals: int = 50
    local_search_iters: int = 100


class C5Search:
    def __init__(self, cfg: Hyperparameters):
        self.cfg = cfg
        self.N = cfg.num_intervals
        self.dx = 2.0 / self.N

    def get_max_overlap(self, h_arr):
        """Compute max(k) of integral h(x)(1-h(x+k))dx."""
        h = jnp.clip(h_arr, 0.0, 1.0)
        j_h = 1.0 - h
        
        N = self.N
        h_pad = jnp.pad(h, (0, N))
        j_pad = jnp.pad(j_h, (0, N))
        
        corr = jnp.fft.fft(h_pad) * jnp.conj(jnp.fft.fft(j_pad))
        corr_ifft = jnp.fft.ifft(corr).real
        
        result = float(jnp.max(corr_ifft * self.dx))
        return result

    def normalize_h(self, arr):
        """Scale so integral is exactly 1."""
        for _ in range(50):
            integ = float(jnp.sum(arr) * self.dx)
            if abs(integ - 1.0) < 0.0005:
                break
            arr = jnp.clip(arr / integ, 0.01, 0.99)
        
        final_integ = float(jnp.sum(arr) * self.dx)
        arr = arr / final_integ
        arr = jnp.clip(arr, 0.0, 1.0)
        return arr

    def init_smooth(self, seed):
        """Create smooth initial guess with proper mass."""
        rng = jax.random.PRNGKey(seed)
        raw_vals = jax.random.normal(rng, (self.N,))
        h_raw = jax.nn.sigmoid(raw_vals) * 10.0
        
        h_norm = self.normalize_h(h_raw)
        return h_norm

    def small_perturb(self, h, rng_seed):
        """Make small changes to random entries."""
        rng = jax.random.PRNGKey(rng_seed)
        pert = h.copy()
        
        # Pick indices
        N_total = len(h)
        n_choices = max(1, min(3, N_total // 20))
        
        idx_gen = jnp.arange(N_total)
        perm_idx = jax.random.permutation(rng, idx_gen)
        selected_indices = perm_idx[:n_choices].tolist()
        
        # Generate bounded deltas [0, 1) then scale to [-0.02, 0.02]
        rand_vals = jax.random.uniform(rng, n_choices)  # [0, 1)
        
        for sel_i, idx_i in enumerate(selected_indices):
            delta = rand_vals[sel_i] * 0.04 - 0.02
            pert = pert.at[idx_i].set(pert[idx_i] + delta)
        
        norm_h = self.normalize_h(pert)
        return norm_h

    def run_search(self):
        best_c5 = float('inf')
        best_h = None
        initial = self.init_smooth(42)
        prev_c5 = self.get_max_overlap(initial)
        
        for it in range(self.cfg.local_search_iters):
            h_cand = self.small_perturb(best_h if best_h is not None else initial, int(it * 31337 + 17))
            cand_c5 = self.get_max_overlap(h_cand)
            
            if cand_c5 < best_c5 - 1e-9:
                best_c5 = cand_c5
                best_h = h_cand
        return best_h, best_c5

    def run_optimization(self):
        h_final, c5_val = self.run_search()
        return h_final, c5_val, self.N


def run():
    cfg = Hyperparameters(num_intervals=50, local_search_iters=150)
    searcher = C5Search(cfg)
    final_h, c5_res, n_pts = searcher.run_optimization()
    return np.array(final_h), c5_res, n_pts
# EVOLVE-BLOCK-END
