def run(ctx, args):
    code = ctx.get_program()
    lines = code.split('\n')
    issues = []
    suggestions = []
    
    in_balanced_packing = False
    for i, line in enumerate(lines):
        if 'def balanced_packing' in line:
            in_balanced_packing = True
        elif in_balanced_packing and line.startswith('def '):
            in_balanced_packing = False
        elif in_balanced_packing and 'for group in indices' in line:
            issues.append(f"Line {i}: O(n^2) nested loop detected")
            suggestions.append(f"Line {i}: Replace with torch.argmin + scatter")
            suggestions.append(f"Alternative: weights_sorted = weight.float().sort(-1, descending=True).indices")
            suggestions.append(f"Alternative: Use torch.bincount for packing")
            break
    
    note = f"Algorithm analysis: {'Yes' if issues else 'No obvious bottlenecks'}"
    if suggestions:
        note += "\nOptimization suggestions:\n" + "\n".join(suggestions)
    return {"notes": note, "complexity_level": 2 if issues else 0,
            "vectorized_alternatives": len(suggestions)}
