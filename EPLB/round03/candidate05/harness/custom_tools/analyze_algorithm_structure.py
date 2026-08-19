def run(ctx, args):
    code = ctx.get_program()
    report = []
    if "for group in indices:" in code and "pack_items" in code:
        report.append({
            "issue": "Python loop in balanced_packing with pack selection",
            "suggestion": "Replace list-based pack tracking with torch tensors and vectorized argmin",
            "pattern": "pack_items = [0] * num_packs, for group in indices: ... min(pack_items[p]...)",
            "replacement": "Use torch.full for init, torch.argmin for selection, torch.gather for assignment"
        })
    if "redundant_indices = (weight / logcnt).max" in code:
        report.append({
            "issue": "Python loop in replicate_experts for redundant expert selection",
            "suggestion": "Use torch.max on weight/logcnt tensor",
            "pattern": "redundant_indices = (weight / logcnt).max(...)"
        })
    return {"analysis": "Loop analysis", "candidates": report, "note": "Review code manually for Python loops in pack selection." if not report else ""}
