def run(ctx, args):
    import random
    random.seed(42)
    seed_program = ctx.get_program()
    
    mutations = []
    
    # Mutation 1: Height perturbation (increase peaks)
    mut1_code = seed_program.replace('set(1.40)', 'set(1.50)').replace('set(1.50)', 'set(1.60)').replace('set(1.60)', 'set(1.70)')
    mutations.append(('height_increase', mut1_code))
    
    # Mutation 2: Height perturbation (decrease valleys)
    mut2_code = seed_program.replace('set(0.60)', 'set(0.70)').replace('set(0.70)', 'set(0.80)')
    mutations.append(('valley_decrease', mut2_code))
    
    # Mutation 3: Position shift (widen support)
    mut3_code = seed_program.replace('int(0.10 * n)', 'int(0.08 * n)').replace('int(0.90 * n)', 'int(0.92 * n)')
    mutations.append(('widen_support', mut3_code))
    
    # Mutation 4: Asymmetric levels (different left/right)
    mut4_code = seed_program.replace('set(1.20)', 'set(1.30)').replace('set(1.40)', 'set(1.45)')
    mutations.append(('asymmetric_left', mut4_code))
    
    # Mutation 5: Level splitting (add intermediate level)
    mut5_code = seed_program.replace('set(1.30)', 'set(1.35)').replace('set(1.40)', 'set(1.42)')
    mutations.append(('intermediate_level', mut5_code))
    
    return {'mutations': [{'type': t, 'code': c} for t, c in mutations]}
