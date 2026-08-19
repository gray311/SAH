def run(ctx, args):
    import numpy as np
    variant_id = args.get("variant_id", 0)
    
    # Generate variant
    if variant_id == 0:
        # Aggressive learning, more restarts
        edit = """
        num_intervals: int = 800
        base_learning_rate: float = 0.01
        num_steps: int = 59000
        penalty_strength: float = 40.0
        num_restarts: int = 5
        seed_start: int = 0
        """
        description = "High LR, low penalty, more restarts"
    elif variant_id == 1:
        # Coarse grid, faster evaluation
        edit = """
        num_intervals: int = 400
        base_learning_rate: float = 0.006
        num_steps: int = 59000
        penalty_strength: float = 60.0
        num_restarts: int = 5
        seed_start: int = 0
        """
        description = "Coarse grid (400 intervals)"
    elif variant_id == 2:
        # Fine grid, more accurate
        edit = """
        num_intervals: int = 1600
        base_learning_rate: float = 0.003
        num_steps: int = 59000
        penalty_strength: float = 60.0
        num_restarts: int = 3
        seed_start: int = 0
        """
        description = "Fine grid (1600 intervals)"
    elif variant_id == 3:
        # High penalty for constraints
        edit = """
        num_intervals: int = 800
        base_learning_rate: float = 0.006
        num_steps: int = 59000
        penalty_strength: float = 100.0
        num_restarts: int = 5
        seed_start: int = 0
        """
        description = "High penalty for integral constraint"
    elif variant_id == 4:
        # Balanced approach
        edit = """
        num_intervals: int = 800
        base_learning_rate: float = 0.006
        num_steps: int = 59000
        penalty_strength: float = 80.0
        num_restarts: int = 5
        seed_start: int = 0
        """
        description = "Balanced: moderate LR and penalty"
    else:
        edit = ""
        description = "No edit"
    
    return {
        "edit_block": edit,
        "description": description,
        "variant_id": variant_id,
        "note": f"Variant {variant_id}: {description}. This variant should be evaluated with evaluate_solution."
    }
