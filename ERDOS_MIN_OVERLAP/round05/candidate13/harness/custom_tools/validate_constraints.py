import re

def run(ctx, args):
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK-START" not in prog:
        return {"note": "no EVOLVE-BLOCK region"}
    
    # Check for critical structural elements
    has_sigmoid = "jax.nn.sigmoid" in prog or "jax.lax.sigmoid" in prog
    has_penalty = "penalty_strength" in prog
    has_integral = "integral_h" in prog or "_sum(h)" in prog
    
    # Check for obvious violations
    has_direct_assignment = re.search(r"h\s*=\s*[\w\.]+\([^\)]+\)", prog)
    if has_direct_assignment and "sigmoid" not in prog:
        return {
            "constraint_status": "INVALID",
            "violations": ["Direct assignment without sigmoid - values may violate [0,1]"],
            "recommendations": ["Restore sigmoid(latent) pattern"]
        }
    
    has_removal_penalty = re.search(r"penalty_strength\s*=\s*[\d.]+", prog)
    if has_removal_penalty is None and "constraint_loss" in prog:
        return {
            "constraint_status": "INVALID", 
            "violations": ["Penalty term missing - integral constraint not enforced"],
            "recommendations": ["Add penalty_strength parameter"]
        }
    
    return {
        "constraint_status": "VALID",
        "has_sigmoid": has_sigmoid,
        "has_penalty": has_penalty,
        "has_integral_check": has_integral,
        "note": "Structural constraints appear preserved"
    }