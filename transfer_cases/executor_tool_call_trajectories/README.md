# Executor tool-call trajectories

These are raw, unedited NexAU trajectories from matched Qwen-235B transfer
experiments. Each directory contains a readable JSON file and its original
gzip-compressed byte stream.

## Qwen-235B x AHC058

- Proposal: `edc3cd56c71a43f79303f2eb02429470`
- Generated skill loaded: `smart-cascade-search`
- Executor tool call: `action_analyzer({})`
- Tool result: prunes 40 possible actions to 20 and recommends 100-turn
  lookahead.
- The executor then rewrites the idea into its own C++ heuristic and records:
  `Use action_analyzer to get pruned list - replaced with internal heuristic`.
- Frozen-evaluator result: `combined_score = 1.3438`, validity `1.0`, total
  score `604710331`.

This is the cleaner skill/tool internalization example: the tool supplies an
analysis primitive rather than a complete answer.

## Qwen-235B x Circle Packing

- Proposal: `3bc2d83ddd4a419989d932a886a7f359`
- Executor tool call:
  `hexagonal_construction({"row_counts":[5,5,5,5,6],"refinement_passes":2})`
- The resulting program is probed and evaluated by the frozen evaluator.

This is intentionally labeled tool-mediated transfer because the tool stages
a complete solver; it is not evidence that Qwen independently derived the
geometry.

## Integrity

See `SHA256SUMS` for hashes of both readable and compressed trajectories.
