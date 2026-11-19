#!/usr/bin/env bash
# 8 GB tier: Q4_K_M + Qwen3-0.6B draft (speculative decoding, 1 drafted token per step), 8,192-token context, one slot.
# Measured: 7.13 GiB GPU memory, 68.7 tokens/s (llama.cpp 08c252e2, RTX PRO 4000 Blackwell SFF). The draft GGUF is
# not part of this release: see README.md. Send "chat_template_kwargs": {"enable_thinking": false} per request.
set -euo pipefail
MODEL=${MODEL:-qwen3-8b-cooking-assistant-v1-Q4_K_M.gguf}
MD=${MD:-qwen3-0.6b-Q4_K_M.gguf}   # the draft model GGUF
exec llama-server -m "$MODEL" --jinja -c 8192 -np 1 \
  -md "$MD" -ngld all --spec-type draft-simple --spec-draft-n-max 1 \
  --port "${PORT:-8080}" "$@"
