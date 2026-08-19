def run(ctx, args):
    import re
    
    analysis = {
        "levels": [],
        "heights": [],
        "positions": [],
        "symmetry": "unknown",
        "weak_links": [],
        "mutation_suggestions": []
    }
    
    program = ctx.get_best_program()
    
    height_matches = re.findall(r'(?:base_height|height)\s*=\s*(?:jnp\.)?([\d.]+)', program)
    if height_matches:
        analysis["heights"] = [float(h) for h in height_matches[:10]]
    
    pos_matches = re.findall(r'int\(([0.5]\d)\s*\*?\s*n\)', program)
    if pos_matches:
        analysis["positions"] = [float(p) for p in pos_matches]
    
    if len(analysis["positions"]) >= 2:
        left_pos = analysis["positions"][:len(analysis["positions"])//2]
        right_pos = analysis["positions"][len(analysis["positions"])//2:]
        if abs(max(left_pos) - min(right_pos)) < 0.1:
            analysis["symmetry"] = "symmetric"
        else:
            analysis["symmetry"] = "asymmetric"
    
    if len(analysis["heights"]) >= 2:
        height_diffs = []
        for i in range(len(analysis["heights"]) - 1):
            diff = abs(analysis["heights"][i] - analysis["heights"][i+1])
            height_diffs.append((i, diff))
        
        height_diffs.sort(key=lambda x: x[1], reverse=True)
        
        if height_diffs:
            analysis["weak_links"] = [
                {"level_pair": (height_diffs[0][0], height_diffs[0][1]), 
                 "suggestion": f"Adjust level {height_diffs[0][0]} by ±0.03-0.06"}
            ]
            analysis["mutation_suggestions"].append({
                "type": "height_perturbation",
                "target": height_diffs[0][0],
                "change": "±0.03-0.06"
            })
    
    analysis["note"] = "Focus on weak links first. Try height perturbation before width changes."
    
    return analysis
