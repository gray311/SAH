def run(ctx, args):
    import math
    import re
    f = ctx.get_program()
    if not f or 'jnp' not in f:
        return {"error": "Invalid program", "recommendations": ["Ensure f(x) is defined with jax.numpy"]}
    try:
        f_text = f
        peak_count = 1
        symmetry_hint = "unknown"
        decay_hint = "unknown"
        recommendations = []
        
        if 'exp(' in f_text and 'cos(' in f_text:
            peak_count = 2
            symmetry_hint = "likely_symmetric"
            decay_hint = "exponential_decay"
            recommendations.append("Consider adjusting oscillation frequency to reduce L_infinity")
            recommendations.append("Try asymmetric decay (different rates for x>0 and x<0)")
        elif 'jnp.piecewise' in f_text or 'jnp.where' in f_text:
            peak_count = "variable"
            symmetry_hint = "check_definition"
            recommendations.append("Analyze piecewise breakpoints for symmetry issues")
        elif 'splev' in f_text or 'bspline' in f_text.lower():
            peak_count = "depends_on_control_points"
            symmetry_hint = "check_control_points"
            recommendations.append("Optimize control points for desired peak structure")
        elif 'gaussian' in f_text.lower() or 'exp(-(' in f_text and 'mu' in f_text:
            peak_count = "multiple_possible"
            symmetry_hint = "likely_symmetric"
            recommendations.append("Add more Gaussian centers for multimodal structure")
            recommendations.append("Try asymmetric weights for better L2/Infinity ratio")
        
        if 'mu = ' in f_text:
            try:
                mu_part = f_text.split('mu = ')[-1].split(']')[0] if '] ' in f_text else f_text.split('mu = ')[-1][:200]
                mu_count = len(re.findall(r'\b\d+\.?\d*', mu_part))
                peak_count = max(2, min(mu_count + 1, 10))
            except:
                peak_count = 3
        
        if peak_count <= 1 or peak_count == "multiple_possible":
            recommendations.append("Single/under-determined peak; add secondary peak to increase L2 norm")
        elif isinstance(peak_count, int) and peak_count > 5:
            recommendations.append("Many peaks; merge close peaks to reduce L_infinity")
        
        if symmetry_hint == "likely_symmetric":
            recommendations.append("Function appears symmetric; try asymmetric variant (different left/right decay)")
        elif symmetry_hint == "check_definition":
            recommendations.append("Check if f(x) = f(-x); asymmetry may help reduce L_infinity")
        
        if decay_hint == "exponential_decay":
            recommendations.append("Exponential decay detected; try piecewise decay or multi-scale structure")
        
        return {
            "estimated_peak_count": peak_count if isinstance(peak_count, int) else "variable",
            "symmetry_hint": symmetry_hint,
            "decay_hint": decay_hint,
            "recommendations": recommendations[:5]
        }
    except Exception as e:
        return {"error": str(e), "recommendations": ["Review function definition", "Ensure valid JAX syntax"]}
