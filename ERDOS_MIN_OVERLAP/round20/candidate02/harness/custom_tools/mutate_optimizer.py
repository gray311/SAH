def run(ctx, args):
    import re
    parameter = args.get("parameter", "num_intervals")
    new_value = args.get("value", None)
    
    code = ctx.get_program()
    edit = None
    rationale = ""
    
    if parameter == "num_intervals":
        old_val = re.search(r"num_intervals:\s*(\d+)", code)
        if old_val:
            old_num = int(old_val.group(1))
            if new_value:
                edit = re.sub(
                    r"num_intervals:\s*\d+",
                    f"num_intervals: {int(new_value)}",
                    code
                )
                rationale = f"Changed num_intervals from {old_num} to {int(new_value)} for finer discretization"
    
    elif parameter == "base_learning_rate":
        old_val = re.search(r"base_learning_rate:\s*[\d.]+", code)
        if old_val and new_value:
            edit = re.sub(
                r"base_learning_rate:\s*[\d.]+",
                f"base_learning_rate: {float(new_value)}",
                code
            )
            rationale = f"Changed base_learning_rate to {float(new_value)} for different convergence dynamics"
    
    elif parameter == "penalty_strength":
        old_val = re.search(r"penalty_strength:\s*[\d.]+", code)
        if old_val and new_value:
            edit = re.sub(
                r"penalty_strength:\s*[\d.]+",
                f"penalty_strength: {float(new_value)}",
                code
            )
            rationale = f"Changed penalty_strength to {float(new_value)} for better constraint enforcement"
    
    elif parameter == "num_restarts":
        old_val = re.search(r"num_restarts:\s*(\d+)", code)
        if old_val:
            old_num = int(old_val.group(1))
            if new_value:
                edit = re.sub(
                    r"num_restarts:\s*\d+",
                    f"num_restarts: {int(new_value)}",
                    code
                )
                rationale = f"Changed num_restarts from {old_num} to {int(new_value)}"
    
    elif parameter == "latent_bias":
        # Add bias term to initialization
        old_code = """latent = latent + jax.random.normal(subkey, (N,)) * 0.3"""
        if old_code in code:
            edit = code.replace(old_code, """latent = latent + jax.random.normal(subkey, (N,)) * 0.3
        latent = latent + 1.0  # Add bias to shift sigmoid output""")
            rationale = "Added latent bias (+1.0) to shift sigmoid output distribution"
        else:
            # Try to find any latent noise line and add bias after
            patterns = [
                r"latent = latent \+ jax\.random\.normal\(subkey, \(N,\)\) \* [\d.]+",
                r"latent = latent \+ jax\.random\.normal\(subkey, \(N,\)\) \* [0-9]"
            ]
            for pat in patterns:
                match = re.search(pat, code)
                if match:
                    latent_line = match.group(0)
                    edit = code.replace(latent_line, latent_line.rstrip() + "\n              latent = latent + 1.0")
                    rationale = "Added latent bias after noise term"
                    break
    
    if edit:
        return {
            "edit": edit,
            "parameter": parameter,
            "new_value": new_value,
            "rationale": rationale,
            "success": True
        }
    else:
        return {
            "edit": None,
            "parameter": parameter,
            "new_value": new_value,
            "rationale": f"Could not find parameter {parameter} to edit",
            "success": False,
            "error": "Edit not applied"
        }
