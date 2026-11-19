#!/usr/bin/env bash
# 6 GB tier: Q4_K_M, 8,192-token context, default (f16) KV cache, one slot. Measured: 5.84 GiB GPU memory, 65.1 tokens/s
# (llama.cpp 08c252e2, RTX PRO 4000 Blackwell SFF). Fits a 6 GB card with nothing else on it. If the card also drives a
# display, add -ctk q8_0 -ctv q8_0 (lossy, 5.3 GiB) or use -c 4096. Send "chat_template_kwargs": {"enable_thinking": false}
# per request.
set -euo pipefail
MODEL=${MODEL:-qwen3-8b-cooking-assistant-v1-Q4_K_M.gguf}
exec llama-server -m "$MODEL" --jinja -c 8192 -np 1 --port "${PORT:-8080}" "$@"
