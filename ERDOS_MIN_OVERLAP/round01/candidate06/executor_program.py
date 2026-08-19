# EVOLVE-BLOCK-START
import numpy as np
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    num_intervals: int = 200
    internal_search_steps: int = 30


class ErdosOptimizer:
    """
    Direct optimization over step function heights.
    Uses explicit construction with guaranteed integral constraint.
    """

    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers
        self.domain_width = 2.0
        self.dx = self.domain_width / self.hypers.num_intervals

    def _compute_c5_bound(self, h_values: np.ndarray) -> float:
        """Compute C5 bound for given h values"""
        h = h_values.copy()
        h = np.clip(h, 0, 1)
        
        # Normalize to integral = 1
        current_sum = np.sum(h)
        needed_sum = 1.0 / self.dx
        
        if current_sum > 0 and abs(current_sum - needed_sum) > 0.01:
            scale = needed_sum / current_sum
            h = np.clip(h * scale, 0, 1)
        
        j = 1.0 - h
        N = len(h)
        
        h_padded = np.pad(h, (0, N))
        j_padded = np.pad(j, (0, N))
        
        corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
        correlation = np.fft.ifft(corr_fft).real
        c5_bound = np.max(correlation) * self.dx
        return c5_bound

    def _build_block_pattern(self, num_on: int) -> np.ndarray:
        """Build block pattern with exactly num_on intervals set to 1"""
        h = np.zeros(self.hypers.num_intervals)
        h[:num_on] = 1.0
        return h

    def _normalize_explicit(self, h_values: np.ndarray) -> np.ndarray:
        """Explicit normalization that guarantees integral = 1"""
        h = h_values.copy()
        needed_sum = 1.0 / self.dx
        current_sum = np.sum(h)
        
        if current_sum <= 0:
            return np.zeros_like(h)
        
        # Scale to target
        scale = needed_sum / current_sum
        h = np.clip(h * scale, 0, 1)
        
        # Fine-tune: adjust values to hit exactly needed_sum
        for _ in range(1000):
            current_sum = np.sum(h)
            if abs(current_sum - needed_sum) < 1e-9:
                break
            
            diff = current_sum - needed_sum
            
            if diff > 0:
                # Too large, decrease some values
                mask = h > 0.001
                if np.sum(mask) == 0:
                    break
                decrease = diff / np.sum(mask)
                h[mask] = np.clip(h[mask] - decrease, 0, 1)
            else:
                # Too small, increase some values
                mask = h < 1.0
                if np.sum(mask) == 0:
                    break
                increase = -diff / np.sum(mask)
                h[mask] = np.clip(h[mask] + increase, 0, 1)
        
        return h

    def _coordinate_descent(self, h_init: np.ndarray, steps: int) -> np.ndarray:
        """Coordinate descent optimization"""
        h = h_init.copy()
        
        for _ in range(steps):
            improved = False
            for i in range(len(h)):
                best_val = h[i]
                best_score = self._compute_c5_bound(h)
                
                # Try variations
                for delta in [-0.2, -0.15, -0.1, -0.05, 0, 0.05, 0.1, 0.15, 0.2]:
                    new_val = np.clip(h[i] + delta, 0, 1)
                    new_h = h.copy()
                    new_h[i] = new_val
                    
                    # Quick integral check
                    new_integral = np.sum(new_h) * self.dx
                    if abs(new_integral - 1.0) > 0.05:
                        continue
                    
                    score = self._compute_c5_bound(new_h)
                    if score < best_score:
                        best_score = score
                        best_val = new_val
                        improved = True
                
                if improved:
                    h[i] = best_val
            
            if not improved:
                break
        
        return h

    def run_optimization(self):
        print(f"Optimizing with {self.hypers.num_intervals} intervals...")
        print(f"dx = {self.dx}, needed_sum = {1.0/self.dx}")
        
        best_h = None
        best_score = float('inf')
        
        # Strategy 1: Various block patterns
        for num_on in [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]:
            h = self._normalize_explicit(self._build_block_pattern(num_on))
            score = self._compute_c5_bound(h)
            if score < best_score:
                best_score = score
                best_h = h.copy()
        
        # Strategy 2: From normalized block patterns with coordinate descent
        for num_on in [50, 60, 70, 80, 90, 100]:
            h_init = self._normalize_explicit(self._build_block_pattern(num_on))
            h_opt = self._coordinate_descent(h_init, self.hypers.internal_search_steps)
            # Final normalize after optimization
            h_opt = self._normalize_explicit(h_opt)
            score = self._compute_c5_bound(h_opt)
            if score < best_score:
                best_score = score
                best_h = h_opt.copy()
        
        # Final check
        integral = np.sum(best_h) * self.dx if best_h is not None else 0
        print(f"Final: integral={integral:.6f}, C5={best_score:.8f}")
        
        # Ensure returned h has correct integral
        if best_h is not None:
            best_h = self._normalize_explicit(best_h)
            return np.array(best_h, dtype=np.float64), float(best_score), self.hypers.num_intervals
        else:
            h_default = np.ones(self.hypers.num_intervals) * 0.5
            return np.array(h_default, dtype=np.float64), 1.0, self.hypers.num_intervals


def run():
    hypers = Hyperparameters()
    optimizer = ErdosOptimizer(hypers)
    final_h_values, c5_bound, num_intervals = optimizer.run_optimization()

    return final_h_values, c5_bound, num_intervals
# EVOLVE-BLOCK-END
