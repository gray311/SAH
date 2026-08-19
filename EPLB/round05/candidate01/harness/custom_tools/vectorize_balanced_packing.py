def run(ctx, args):
    import numpy as np
    num_layers, num_groups = 2, 16
    num_packs = 4
    groups_per_pack = num_groups // num_packs
    
    weight = np.random.rand(num_layers, num_groups)
    
    sorted_idx = np.argsort(-weight, axis=-1)
    pack_index = sorted_idx // groups_per_pack
    rank_in_pack = sorted_idx % groups_per_pack
    
    flat_pack_idx = pack_index.flatten()
    flat_weight = weight.flatten()
    pack_weights = np.zeros(num_packs)
    for p in range(num_packs):
        mask = flat_pack_idx == p
        pack_weights[p] = flat_weight[mask].sum() if mask.any() else 0.0
    
    pack_index = pack_index.reshape(num_layers, num_groups)
    rank_in_pack = rank_in_pack.reshape(num_layers, num_groups)
    
    code_template = '''def balanced_packing(weight: np.ndarray, num_packs: int) -> tuple[np.ndarray, np.ndarray]:
num_layers, num_groups = weight.shape
groups_per_pack = num_groups // num_packs

sorted_idx = np.argsort(-weight, axis=-1)
pack_index = sorted_idx // groups_per_pack
rank_in_pack = sorted_idx % groups_per_pack

flat_pack_idx = pack_index.flatten()
flat_weight = weight.flatten()
pack_weights = np.zeros(num_packs)
for p in range(num_packs):
    mask = flat_pack_idx == p
    pack_weights[p] = flat_weight[mask].sum() if mask.any() else 0.0

return pack_index, rank_in_pack'''
    
    return {
        "full_vectorized_code": code_template,
        "explanation": "Uses argsort for global sort, then bulk division/modulo for pack assignment and ranking. Pack weights computed via boolean indexing."
    }