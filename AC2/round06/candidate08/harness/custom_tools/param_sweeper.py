def run(ctx, args):
    import random
    seed = args.get('seed', 42)
    random.seed(seed)
    
    configs = []
    
    # Different combinations based on focus
    if args.get('focus', 'balanced') == 'resolution':
        num_intervals_list = [100, 200, 350, 500, 800, 1000]
        lr_list = [0.05, 0.1, 0.125]
        steps_list = [20000, 40000, 60000]
        warmup_list = [2000, 4000, 8000]
        reinit_frac_list = [0.05, 0.1, 0.15]
        reinit_std_list = [0.01, 0.02, 0.04]
    elif args.get('focus', 'balanced') == 'learning_rate':
        num_intervals_list = [300, 400, 500, 600]
        lr_list = [0.01, 0.05, 0.1, 0.15, 0.2]
        steps_list = [15000, 30000, 45000, 60000]
        warmup_list = [1000, 3000, 6000]
        reinit_frac_list = [0.08, 0.12, 0.18]
        reinit_std_list = [0.015, 0.025, 0.05]
    else:  # balanced
        num_intervals_list = [200, 300, 350, 450, 600]
        lr_list = [0.05, 0.1, 0.125, 0.2]
        steps_list = [20000, 35000, 50000, 70000]
        warmup_list = [2000, 5000, 8000]
        reinit_frac_list = [0.05, 0.1, 0.15]
        reinit_std_list = [0.01, 0.02, 0.04]
    
    for _ in range(args.get('num_combinations', 10)):
        config = {
            'num_intervals': random.choice(num_intervals_list),
            'learning_rate': random.choice(lr_list),
            'num_steps': random.choice(steps_list),
            'warmup_steps': random.choice(warmup_list),
            'reinit_fraction': random.choice(reinit_frac_list),
            'reinit_std': random.choice(reinit_std_list),
        }
        configs.append(config)
    
    return {
        'configs': configs,
        'num_generated': len(configs),
        'focus': args.get('focus', 'balanced')
    }