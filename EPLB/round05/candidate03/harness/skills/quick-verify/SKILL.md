---
name: quick-verify
description: Quick checklist before submitting code. Ensure balanced_packing uses argsort, integer division, and modulo for pack assignment. Call this before finish.
---

# Quick Verification Checklist for balanced_packing()

## Before finishing, verify:

1. **Imports**: torch is imported at top of file
2. **Function**: balanced_packing(weight, num_packs) exists with same signature
3. **Sorting**: Uses torch.argsort(-weight, dim=-1) or similar
4. **Packing assignment**: pack_index = sorted_idx // groups_per_pack (integer division)
5. **Rank assignment**: rank_in_pack = sorted_idx % groups_per_pack (modulo)
6. **No bad loops**: No `for group in indices:` loops
7. **No list comps**: No `[p for p in range(num_packs)]` patterns
8. **Returns**: Returns torch.Tensor, torch.Tensor (or list of Tensors)

## Common failures:
- Forgetting // or using / (float division)
- Using list comprehension for pack selection
- Changing sorting criterion (must be descending)
- Not pre-allocating output tensors
- Forgetting device handling

## If check_implementation reports issues:
- Fix the specific issues listed
- Re-run check_implementation
- Only call finish when status is "valid"
