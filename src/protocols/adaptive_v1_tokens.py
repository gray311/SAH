"""Token-budget guards for Adaptive-only NexAU stages."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence


def conservative_estimate(text: str) -> int:
    ascii_chars = sum(ord(char) < 128 for char in text)
    return (ascii_chars + 2) // 3 + len(text) - ascii_chars


@lru_cache(maxsize=2)
def _tokenizer(path: str):
    from transformers import AutoTokenizer

    return AutoTokenizer.from_pretrained(path, local_files_only=True)


def count_chat_tokens(
    *,
    system: str,
    user: str,
    tools: Optional[Sequence[Mapping[str, Any]]] = None,
    tokenizer_path: Optional[str] = None,
) -> tuple[int, str]:
    """Count the actual Qwen chat template when a local tokenizer is supplied."""
    if tokenizer_path:
        tokenizer = _tokenizer(str(Path(tokenizer_path).resolve()))
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        rendered = tokenizer.apply_chat_template(
            messages,
            tools=list(tools) if tools else None,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
        return (
            len(tokenizer(rendered, add_special_tokens=False)["input_ids"]),
            "local_qwen_tokenizer",
        )
    text = system + "\n" + user
    if tools:
        text += "\n" + json.dumps(list(tools), ensure_ascii=False)
    return conservative_estimate(text), "conservative_estimate"
