def before_model(hook_input):
    if hook_input.get("evaluations_left", 0) <= 5:
        return "HIGH PRIORITY: You have few evals left. Call probe_solution to rank remaining variant ideas before spending evals."
    return "REMEMBER: Use probe_solution to quickly compare 2-3 pattern variants before calling evaluate_solution. Probes are cheap and fast."