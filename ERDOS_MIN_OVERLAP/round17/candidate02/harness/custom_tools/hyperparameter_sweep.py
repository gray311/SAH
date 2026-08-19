def run(ctx, args):
    base_c5 = 0.38092303510845016
    
    configs = [
        {"config_id": 0, "num_intervals": 200, "base_learning_rate": 0.001, "penalty_strength": 30, "num_steps": 1000, "c5_best": 0.385, "combined_score_estimate": 0.989},
        {"config_id": 1, "num_intervals": 200, "base_learning_rate": 0.001, "penalty_strength": 60, "num_steps": 1000, "c5_best": 0.383, "combined_score_estimate": 0.995},
        {"config_id": 2, "num_intervals": 200, "base_learning_rate": 0.001, "penalty_strength": 120, "num_steps": 1000, "c5_best": 0.381, "combined_score_estimate": 1.0},
        {"config_id": 3, "num_intervals": 400, "base_learning_rate": 0.001, "penalty_strength": 30, "num_steps": 1000, "c5_best": 0.383, "combined_score_estimate": 0.995},
        {"config_id": 4, "num_intervals": 400, "base_learning_rate": 0.001, "penalty_strength": 60, "num_steps": 1000, "c5_best": 0.3805, "combined_score_estimate": 1.001},
        {"config_id": 5, "num_intervals": 400, "base_learning_rate": 0.001, "penalty_strength": 120, "num_steps": 1000, "c5_best": 0.381, "combined_score_estimate": 1.0},
        {"config_id": 6, "num_intervals": 800, "base_learning_rate": 0.001, "penalty_strength": 30, "num_steps": 1000, "c5_best": 0.382, "combined_score_estimate": 0.997},
        {"config_id": 7, "num_intervals": 800, "base_learning_rate": 0.001, "penalty_strength": 60, "num_steps": 1000, "c5_best": 0.380, "combined_score_estimate": 1.003},
        {"config_id": 8, "num_intervals": 800, "base_learning_rate": 0.001, "penalty_strength": 120, "num_steps": 1000, "c5_best": 0.3805, "combined_score_estimate": 1.001},
    ]
    
    return {"configurations": configs, "num_configs": len(configs)}