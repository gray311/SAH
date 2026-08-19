def run(ctx, args):
    code = ctx.get_program()
    # Analyze current structure
    improvements = []
    
    # Check initialization diversity
    if "for pattern in range(12)" in code:
        improvements.append(("DIVERSITY", "Good - uses 12 patterns. Try adding more structured patterns like piecewise constants."))
    
    # Check interval count
    if "num_intervals: int = 800" in code:
        improvements.append(("INTERVALS", "High interval count (800). Try starting with 100-200 for faster convergence, then refine."))
    
    # Check constraint handling
    if "penalty_strength: float = 1370.0" in code and "normalize" not in code:
        improvements.append(("CONSTRAINTS", "Relies on penalty alone. Consider explicit normalization: h = h / sum(h) * N to ensure ∫h=1."))
    
    # Check step function approach
    if "jax.nn.sigmoid" in code and "where" not in code:
        improvements.append(("STEP_FUNC", "Uses continuous sigmoid. Try explicit piecewise constant: use jnp.where with thresholds for true step functions."))
    
    recommendations = {
        "analysis": "Seed program overview",
        "improvements": improvements,
        "priority": ["INTERVALS", "CONSTRAINTS", "STEP_FUNC"]
    }
    return recommendations
