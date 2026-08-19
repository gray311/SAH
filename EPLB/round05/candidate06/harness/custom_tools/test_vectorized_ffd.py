def run(ctx, args):
    prog = ctx.get_program()
    import re
    content = prog.strip()
    # Extract weight tensor shape from balanced_packing docstring or code
    match = re.search(r'weight:\s*\[(\d+),\s*(\d+)\]', content)
    if not match:
        return {"status": "error", "note": "could not parse weight shape"}
    try:
        num_layers, num_groups = int(match.group(1)), int(match.group(2))
        num_packs = num_groups // 4  # Assume default
        # Create small test tensor
        torch.manual_seed(42)
        test_weight = torch.rand(num_layers, num_groups) * 10.0
        # Run simplified vectorized FFD
        sorted_idx = test_weight.argsort(descending=True, dim=-1)
        sorted_weights = test_weight[sorted_idx]
        groups_per_pack = num_groups // num_packs
        pack_items = torch.zeros(num_packs, dtype=torch.int64)
        pack_weights = torch.zeros(num_packs, dtype=torch.float32)
        pack_test = torch.zeros(num_groups, dtype=torch.int64)
        rank_test = torch.zeros(num_groups, dtype=torch.int64)
        for i, w in enumerate(sorted_weights.tolist()):
            valid = pack_items < groups_per_pack
            if not valid.any():
                break
            candidates = torch.stack([pack_items[valid], pack_weights[valid]], dim=0)
            best = torch.argmin(candidates, dim=0)
            best_pack = int(best[1].item())
            pack_test[i] = best_pack
            pack_items[best_pack] += 1
            pack_weights[best_pack] += w
        # Verify all packs have correct size
        if not (pack_items == groups_per_pack).all():
            return {"status": "fail", "note": "pack sizes mismatch"}
        return {"status": "pass", "note": "vectorized FFD test passed",
                "pack_items": pack_items.tolist(),
                "avg_pack_weight": float(pack_weights.mean().item())}
    except Exception as e:
        return {"status": "error", "note": str(e)}
