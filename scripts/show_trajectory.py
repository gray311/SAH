#!/usr/bin/env python3
"""Pretty-print the full M_phi+H1 -> H2 -> inner chain for a round's candidates.

Usage:
  show_trajectory.py <round_dir> [task_id] [k]

With no k: lists every candidate's one-line summary.
With a k: dumps that candidate's full chain —
  1. the H1 user message (task context + inheritance + feedback + analyst notes)
  2. the H1 agent trajectory (M_phi designing the spec, tool call by tool call)
  3. the submitted spec (raw YAML)
  4. generated tools + reviewer repair log
  5. the materialized agent.yaml tool set (proof of structural divergence)
  6. the inner rollout outcome (score, evals, whether custom tools were called)
"""
import json
import sys
from collections import Counter
from pathlib import Path


def _text(content):
    if isinstance(content, list):
        return " ".join(b.get("text", "") for b in content if isinstance(b, dict))
    return content or ""


def _custom_tool_calls(result):
    builtins = {
        "LoadSkill",
        "edit_solution",
        "evaluate_solution",
        "probe_solution",
        "finish",
    }
    calls = Counter()
    for message in result.get("trajectory") or []:
        if not isinstance(message, dict):
            continue
        for block in message.get("content") or []:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            name = str(block.get("name") or "")
            if name and name not in builtins:
                calls[name] += 1
    return calls


def main() -> None:
    rd = Path(sys.argv[1])
    meta = json.loads((rd / "round.json").read_text())
    trajs = {(t["task_id"], t["k"]): t
             for t in json.loads((rd / "trajectories.json").read_text())}
    prompts = json.loads((rd / "prompts.json").read_text())

    tasks = meta["tasks_order"]
    if len(sys.argv) >= 3:
        tasks = [sys.argv[2]]

    if len(sys.argv) < 4:  # summary mode
        for tid in tasks:
            print(f"\n=== {tid} ===")
            for c in meta["per_task"][tid]["candidates"]:
                rl = c.get("review_log") or []
                tools = ",".join(x["name"] + ("/ok" if x["ok"] else "/drop") for x in rl)
                changed = [f.split(".")[-1] for f in c.get("changed_fields", [])]
                print(f"  cand{c['k']:02d} valid={int(c['valid'])} "
                      f"changed={changed} tools=[{tools}] "
                      f"stop={c.get('stop_reason')}")
        print("\nrun with a k to see one candidate's full chain.")
        return

    tid, k = sys.argv[2], int(sys.argv[3])
    cdir = rd / "tasks" / tid / f"cand{k:02d}"
    cand = next(c for c in meta["per_task"][tid]["candidates"] if c["k"] == k)

    print("#" * 78)
    print(f"# {tid}  cand{k:02d}   round {meta['round']}   valid={cand['valid']}")
    print("#" * 78)

    print("\n===== 1. H1 USER MESSAGE (what M_phi was conditioned on) =====")
    print(prompts.get(tid, "")[:6000])

    print("\n===== 2. H1 TRAJECTORY (M_phi designing the harness) =====")
    for i, m in enumerate(trajs.get((tid, k), {}).get("trajectory", [])):
        role = m.get("role", "?")
        tc = [x["function"]["name"] for x in (m.get("tool_calls") or [])]
        body = _text(m.get("content"))
        head = f"[{i}] {role}"
        if tc:
            print(f"{head}  ->tools {tc}")
        if body.strip():
            print(f"{head}: {body.strip()[:1400]}")

    print("\n===== 3. SUBMITTED SPEC (raw) =====")
    print((trajs.get((tid, k), {}).get("raw_submission") or "")[:4000])

    print("\n===== 4. REVIEW LOG (gate + repair per tool) =====")
    for r in (cand.get("review_log") or []):
        print(f"  {r['name']}: ok={r['ok']} rounds={r['rounds']} "
              f"error={r.get('error')}")
        for h in r.get("history", []):
            print(f"      {h}")

    if (cdir / "custom_tools").exists():
        print("\n===== 4b. GENERATED TOOL CODE =====")
        for f in sorted((cdir / "custom_tools").glob("*.py")):
            print(f"--- {f.name} ---")
            print(f.read_text())

    if (cdir / "agent.yaml").exists():
        import yaml
        cfg = yaml.safe_load((cdir / "agent.yaml").read_text())
        print("\n===== 5. MATERIALIZED agent.yaml TOOL SET =====")
        for t in cfg["tools"]:
            print(f"  {t['name']:22s} -> {t['binding']}")

    print("\n===== 6. INNER ROLLOUT OUTCOME =====")
    rollout_root = rd / "rollouts" / tid / f"cand{k:02d}"
    adaptive = meta.get("protocol") == "adaptive_v1"
    hits = list(
        rollout_root.rglob("results/*.json")
        if adaptive
        else rollout_root.glob("*/results/*.json")
    )
    if not hits:
        hits = list(
            rollout_root.rglob("checkpoints/*.json")
            if adaptive
            else rollout_root.glob("*/checkpoints/*.json")
        )
    if hits:
        hits = sorted(hits)
        if adaptive:
            channel_scores = {}
            channel_complete = Counter()
            channel_errors = Counter()
            custom_calls = Counter()
            for result_path in hits:
                result = json.loads(result_path.read_text())
                channel = next(
                    (
                        name
                        for name in ("outcome", "promotion")
                        if name in result_path.parts
                    ),
                    "unknown",
                )
                channel_scores.setdefault(channel, []).append(
                    result.get("best_score")
                )
                if result.get("stop_reason") == "completed" and not result.get(
                    "error"
                ):
                    channel_complete[channel] += 1
                else:
                    channel_errors[channel] += 1
                custom_calls.update(_custom_tool_calls(result))
            print(f"  rollout_results={len(hits)}")
            for channel in sorted(channel_scores):
                print(
                    f"  {channel}: scores={channel_scores[channel]} "
                    f"completed={channel_complete[channel]} "
                    f"errors={channel_errors[channel]}"
                )
            print(f"  custom_tool_calls={dict(custom_calls)}")
        d = json.loads(hits[-1].read_text())
        led = d.get("ledger") or {}
        print(f"  best_score={d.get('best_score')} evals={led.get('evaluator_calls')} "
              f"probes={led.get('probe_calls')} stop={d.get('stop_reason')}")
        if adaptive:
            inner_trace = d.get("trajectory") or []
            print(f"  inner_trajectory_messages={len(inner_trace)} "
                  f"roles={[str(m.get('role', '?')) for m in inner_trace]}")
        notes = [s for s in (d.get("steps") or [])
                 if isinstance(s, dict) and s.get("kind") == "note"]
        if notes:
            print(f"  custom-tool notes: {len(notes)}")
            for n in notes[:5]:
                print(f"    - {n.get('edit_note','')[:120]}")
    else:
        print("  (no rollout output yet)")


if __name__ == "__main__":
    main()
