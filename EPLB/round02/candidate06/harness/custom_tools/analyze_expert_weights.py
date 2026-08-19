def run(ctx, args):
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no task inputs", "weights": {}}
    # Analyze weight tensor if available in ctx
    weight = ctx.get_program()
    # Parse weight tensor structure from program
    return {"weights": str(weight[:200]), "analysis": "check tensor shapes"}