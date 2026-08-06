"""Convert an outer-round grpo_batch.jsonl into Weave/slime GRPO replay format.

We reuse Weave_v2's proven offline-GRPO stack (slime FSDP, Qwen3.5-9B LoRA,
already working on this cluster). Its replay row format
(actions/grpo/grpo_prep.py):

    {"messages": [...], "tools": [...], "metadata": {"advantage": A, ...}}

Our proposer rows carry the FULL H1 agent trajectory (`cat agent.yaml` ->
targeted file inspection/editing -> validate_harness -> submit_harness). We
normalize it with Weave's
common.qwen35_format.normalize_qwen35_messages — the same function Weave uses
on its own NexAU trajectories — and pass the H1 tool schemas so the chat
template renders tool definitions identically at train time.

Loss-mask note: Weave's Qwen35MultiTurnLossMaskGenerator only counts assistant
turns that are CLOSED by a later user/tool message. Tool-calling turns are
closed by their tool results; only a trailing plain-assistant turn would be
unmasked, so we append a terminal user turn ("ok") when the trajectory ends on
an assistant message.

Usage:
    python grpo_to_replay.py --rounds <round_dir> [<round_dir> ...] --out replay.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

WEAVE_ROOT = Path(os.environ.get(
    "WEAVE_ROOT", "/lustre/fsw/portfolios/av/users/yingzim/code/Weave_v2"))
H1_TOOLS_DIR = Path(__file__).resolve().parents[1] / "outer" / "harness" / "tools"
H1_AGENT_YAML = H1_TOOLS_DIR.parent / "agent.yaml"
CLOSE_TURN = {"role": "user", "content": "ok"}


def _h1_tool_schemas() -> list:
    import yaml
    schemas = []
    agent = yaml.safe_load(H1_AGENT_YAML.read_text()) or {}
    mounted = agent.get("tools") or []
    seen = set()
    for row in mounted:
        if not isinstance(row, dict) or not row.get("name") or not row.get("yaml_path"):
            raise ValueError("every mounted H1 tool needs name and yaml_path")
        name = str(row["name"])
        if name in seen:
            raise ValueError(f"duplicate mounted H1 tool: {name}")
        seen.add(name)
        f = (H1_AGENT_YAML.parent / str(row["yaml_path"])).resolve()
        try:
            f.relative_to(H1_AGENT_YAML.parent.resolve())
        except ValueError as exc:
            raise ValueError(f"H1 tool schema escapes package: {f}") from exc
        if not f.is_file():
            raise FileNotFoundError(f"mounted H1 tool schema missing: {f}")
        doc = yaml.safe_load(f.read_text())
        if doc.get("name") != name:
            raise ValueError(
                f"mounted H1 tool {name!r} does not match schema name {doc.get('name')!r}"
            )
        schemas.append({"type": "function", "function": {
            "name": doc["name"], "description": doc.get("description", ""),
            "parameters": doc.get("input_schema", {})}})
    return schemas


def _normalizer():
    if str(WEAVE_ROOT) not in sys.path:
        sys.path.insert(0, str(WEAVE_ROOT))
    from common.qwen35_format import normalize_qwen35_messages  # noqa: E402
    return normalize_qwen35_messages


# Qwen3.5's chat template accepts only these roles. NexAU middlewares inject
# FRAMEWORK-role reminders; the policy saw them as extra instructions, so map
# them to user turns. Anything else is dropped defensively.
_ROLE_MAP = {"system": "system", "user": "user", "assistant": "assistant",
             "tool": "tool", "framework": "user"}


def _sanitize_roles(msgs: list) -> list:
    out = []
    for m in msgs:
        role = _ROLE_MAP.get(str(m.get("role", "")).lower())
        if role is None:
            continue
        out.append({**m, "role": role})
    return out


def convert_row(row: dict, tools: list, normalize) -> dict:
    traj = row.get("trajectory") or []
    if traj and normalize is not None:
        msgs = normalize(traj)
        # the round stores only the run's messages; ensure system turn leads
        if not msgs or str(msgs[0].get("role")).lower() != "system":
            msgs = [{"role": "system", "content": row["system"]}] + msgs
    else:  # fallback: single-turn (system, user, assistant=raw submission)
        msgs = [{"role": "system", "content": row["system"]},
                {"role": "user", "content": row["user"]},
                {"role": "assistant", "content": row["response"]}]
    msgs = _sanitize_roles(msgs)
    if msgs[-1].get("role") == "assistant":
        msgs = msgs + [CLOSE_TURN]  # close the trailing turn for the loss mask
    return {
        "messages": msgs,
        "tools": tools,
        "metadata": {
            "advantage": row["advantage"], "reward": row["reward"],
            "seed": f"r{row['round']:03d}_{row.get('task_id','all')}_c{row['k']:02d}",
            "round": row["round"], "k": row["k"], "task_id": row.get("task_id"),
            "valid": row["valid"], "spec_hash": row.get("spec_hash", ""),
            "tools": tools,
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rounds", nargs="+", required=True,
                    help="round dirs containing grpo_batch.jsonl")
    ap.add_argument("--out", required=True)
    ap.add_argument("--keep-zero", action="store_true",
                    help="keep |advantage| < eps rows (default: drop, matching Weave)")
    ap.add_argument("--eps", type=float, default=1e-6)
    args = ap.parse_args()

    tools = _h1_tool_schemas()
    try:
        normalize = _normalizer()
    except Exception as e:  # Weave repo unavailable -> single-turn fallback
        print(f"[grpo_to_replay] WARNING: no Weave normalizer ({e}); single-turn fallback")
        normalize = None

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    n_in = n_out = 0
    with open(out, "w") as f:
        for rd in args.rounds:
            for line in (Path(rd) / "grpo_batch.jsonl").read_text().splitlines():
                if not line.strip():
                    continue
                n_in += 1
                row = json.loads(line)
                if not (row.get("trajectory") or row.get("response", "").strip()):
                    continue  # nothing to train on
                if not args.keep_zero and abs(row["advantage"]) < args.eps:
                    continue
                f.write(json.dumps(convert_row(row, tools, normalize),
                                   ensure_ascii=False) + "\n")
                n_out += 1
    print(f"[grpo_to_replay] {n_in} rows in -> {n_out} trainable rows -> {out}")


if __name__ == "__main__":
    main()
