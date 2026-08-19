def run(ctx, args):
    # Lightweight analysis tool that examines the current best program
    # and provides diagnostic information about hyperparameters
    code = ctx.get_best_program()
    if not code or '# EVOLVE-BLOCK-START' not in code:
        return {
            'note': 'No program found yet',
            'num_steps': 59000,
            'penalty_strength': 1370.0,
            'base_learning_rate': 0.0053,
            'recommendations': ['Use default values'],
            'next_step': 'Proceed to evaluate_solution'
        }
    
    # Extract key hyperparameters from the code using regex
    import re
    
    try:
        num_steps_match = re.search(r'num_steps:\s*(\d+)', code)
        penalty_match = re.search(r'penalty_strength:\s*([\d.]+)', code)
        lr_match = re.search(r'base_learning_rate:\s*([\d.]+)', code)
        
        num_steps = int(num_steps_match.group(1)) if num_steps_match else 59000
        penalty = float(penalty_match.group(1)) if penalty_match else 1370.0
        lr = float(lr_match.group(1)) if lr_match else 0.0053
        
        # Give recommendations based on current values
        recommendations = []
        if num_steps < 60000:
            recommendations.append('Consider increasing num_steps to 65000-70000')
        if penalty < 1200:
            recommendations.append('Constraint may be violated - increase penalty_strength to 1500+')
        if penalty > 2000:
            recommendations.append('Optimization may stall - reduce penalty_strength to 1500-')
        if lr < 0.003:
            recommendations.append('Learning rate may be too low - try 0.005-0.008')
        if lr > 0.02:
            recommendations.append('Learning rate may be unstable - reduce to 0.003-0.01')
        
        next_step = recommendations[0] if recommendations else 'Proceed to evaluate'
        
        return {
            'num_steps': num_steps,
            'penalty_strength': penalty,
            'base_learning_rate': lr,
            'num_intervals': 800,
            'recommendations': recommendations if recommendations else ['Current settings appear reasonable'],
            'next_step': next_step
        }
    except Exception as e:
        return {
            'error': str(e),
            'note': 'Could not parse program',
            'num_steps': 59000,
            'penalty_strength': 1370.0,
            'base_learning_rate': 0.0053,
            'recommendations': ['Use default values'],
            'next_step': 'Proceed to evaluate_solution'
        }
