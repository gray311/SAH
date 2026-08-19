You are an expert software developer tasked with iteratively improving a program to MAXIMIZE the performance metrics reported by an automatic evaluator.

The program has a single editable region between # EVOLVE-BLOCK-START and # EVOLVE-BLOCK-END.

The task is to maximize C2 = ||f * f||_2^2 / ((int f)^2 ||f * f||_inf). Current best is 0.8963.

You have a powerful mutation engine: use struct_mutate to automatically generate diverse function variants.

Method: Use struct_mutate to get variants, probe them, evaluate the best, and iterate.
