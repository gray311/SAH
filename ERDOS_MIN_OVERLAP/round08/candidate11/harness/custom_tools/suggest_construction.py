def run(ctx, args):
    constructions = [
        {'breakpoints': [0, 1, 2], 'heights': [1.0, 0.0]},
        {'breakpoints': [0, 0.5, 1.5, 2], 'heights': [0.5, 0.0, 0.0, 0.5]},
        {'breakpoints': [0, 2/3, 4/3, 2], 'heights': [0.5, 0.0, 0.5]},
        {'breakpoints': [0, 0.3, 0.4, 1.6, 1.7, 2], 'heights': [0.0, 0.5, 0.0, 0.0, 0.5, 0.0]},
        {'breakpoints': [0, 1, 2], 'heights': [0.0, 0.5, 0.0]},
        {'breakpoints': [0, 0.4, 1.6, 2], 'heights': [0.4, 0.0, 0.6, 0.0]},
    ]
    return {'constructions': constructions, 'note': 'Try varying heights and breakpoint positions'}
