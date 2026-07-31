# Agent config comparison — baseline vs evolved (CP round300/cand06)

Full files: `baseline_agent.yaml` · `evolved_agent.yaml` · raw diff: `agent_yaml_diff.txt` (side-by-side), `agent_yaml_diff_unified.txt`

| field | baseline | evolved |
|---|---|---|
| tools | edit_solution, evaluate_solution, probe_solution, finish | edit_solution, evaluate_solution, probe_solution, finish, analyze_geometry **← NEW** |
| skills | discovery-optimization | discovery-optimization, circle-packing-strategies **← NEW** |
| middlewares | budget_reminder, stall_restart, long_tool_output, round_reminder | probe_reminder(new), budget_reminder, stall_restart, long_tool_output, round_reminder **← NEW: probe_reminder** |
| temperature | 0.7 | 1.2 **←** |
| max_iterations | 36 | 60 **←** |
| system_prompt | ./system.md | ./prompt.md **←** |

**Net:** evolved adds `analyze_geometry` (tool), `circle-packing-strategies` (skill), `probe_reminder` (middleware); temp 0.7→1.2; iters 36→60. All four generative axes changed, not just hyperparameters.