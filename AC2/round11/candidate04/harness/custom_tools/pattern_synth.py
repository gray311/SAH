def run(ctx, args):
    import re
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"error": "no evolve block", "code": ""}

    # Extract current heights for context
    heights = re.findall(r'\.set\((\d+\.\d+)\)', prog)
    current_heights = [float(h) for h in heights if h]

    avg_h = sum(current_heights) / len(current_heights) if current_heights else 1.0
    max_h = max(current_heights) if current_heights else 1.0
    min_h = min(current_heights) if current_heights else 1.0

    # Generate 5 diverse new patterns as concrete code blocks
    patterns = []

    # Pattern 1: Asymmetric 5-peak
    p1_code = f"""        pattern_idx == {len(current_heights) + 1}:
      # Asymmetric 5-peak pattern
      # Heights: [low, tall, medium, tall2, low] - breaks symmetry
      f = f.at[int(0.06*n):int(0.18*n)].set({min_h * 0.5:.2f})
      f = f.at[int(0.18*n):int(0.32*n)].set({max_h * 1.4:.2f})
      f = f.at[int(0.32*n):int(0.48*n)].set({avg_h * 0.8:.2f})
      f = f.at[int(0.48*n):int(0.68*n)].set({max_h * 1.2:.2f})
      f = f.at[int(0.68*n):int(0.92*n)].set({min_h * 0.4:.2f})"""
    patterns.append(("asymmetric_5peak", p1_code))

    # Pattern 2: Smooth exponential decay
    p2_code = f"""        pattern_idx == {len(current_heights) + 2}:
      # Smooth transition pattern with exponential-like decay
      # Central plateau with soft edges
      f = f.at[int(0.20*n):int(0.80*n)].set({max_h * 1.2:.2f})
      # Left ramp-up (exponential-like)
      left_ramp = jnp.linspace(0, {max_h * 1.2:.2f}, num=int(0.18*n), endpoint=False)
      f = f.at[:int(0.20*n)].set(left_ramp)
      # Right ramp-down (exponential-like)  
      right_ramp = jnp.linspace({max_h * 1.2:.2f}, 0, num=int(0.18*n), endpoint=False)
      f = f.at[int(0.80*n):].set(right_ramp)"""
    patterns.append(("smooth_transition", p2_code))

    # Pattern 3: Bi-modal distribution
    p3_code = f"""        pattern_idx == {len(current_heights) + 3}:
      # Bi-modal: two peaks with deep valley
      # Left peak, valley, right peak - exploits convolution structure
      left_peak = jnp.full(int(0.25*n), {max_h * 1.1:.2f})
      valley = jnp.full(int(0.15*n), {avg_h * 0.3:.2f})
      right_peak = jnp.full(int(0.25*n), {max_h * 1.3:.2f})
      f = f.at[:int(0.15*n)].set(jnp.concatenate([jnp.zeros(int(0.1*n)), left_peak, valley]))
      f = f.at[int(0.15*n):int(0.60*n)].set(jnp.concatenate([valley, jnp.zeros(int(0.15*n)), right_peak, jnp.zeros(int(0.1*n))]))
      f = f.at[int(0.60*n):].set(jnp.zeros(int(0.40*n)))"""
    patterns.append(("bi_modal", p3_code))

    # Pattern 4: Irregular spacing multi-level
    p4_code = f"""        pattern_idx == {len(current_heights) + 4}:
      # Irregularly spaced multi-level with varying interval widths
      # Interval widths: 12%, 16%, 24%, 20%, 28% - avoids constructive interference
      f = f.at[int(0.08*n):int(0.22*n)].set({avg_h * 0.9:.2f})
      f = f.at[int(0.22*n):int(0.38*n)].set({max_h * 1.35:.2f})
      f = f.at[int(0.38*n):int(0.62*n)].set({avg_h * 0.65:.2f})
      f = f.at[int(0.62*n):int(0.82*n)].set({max_h * 1.15:.2f})
      f = f.at[int(0.82*n):int(0.95*n)].set({avg_h * 0.8:.2f})"""
    patterns.append(("irregular_spacing", p4_code))

    # Pattern 5: Tri-modal symmetric
    p5_code = f"""        pattern_idx == {len(current_heights) + 5}:
      # Tri-modal symmetric pattern: low-mid-high-mid-low
      # Balances concentration with spread
      outer = jnp.full(int(0.22*n), {min_h * 0.6:.2f})
      inner_low = jnp.full(int(0.20*n), {avg_h * 0.7:.2f})
      peak = jnp.full(int(0.30*n), {max_h * 1.4:.2f})
      inner_high = jnp.full(int(0.20*n), {avg_h * 0.9:.2f})
      f = f.at[:int(0.15*n)].set(outer)
      f = f.at[int(0.15*n):int(0.35*n)].set(inner_low)
      f = f.at[int(0.35*n):int(0.55*n)].set(peak)
      f = f.at[int(0.55*n):int(0.75*n)].set(inner_high)
      f = f.at[int(0.75*n):].set(outer)"""
    patterns.append(("tri_modal_sym", p5_code))

    # Return all patterns as executable code
    return {
        "current_analysis": {
            "avg_height": avg_h,
            "max_height": max_h,
            "min_height": min_h,
            "n_current_patterns": len(current_heights) + 1
        },
        "generated_patterns": [
            {"name": name, "code": code} for name, code in patterns
        ],
        "instruction": "Replace the corresponding pattern_idx blocks in _create_step_initializer with these new code blocks. Ensure all patterns are syntactically complete."
    }
