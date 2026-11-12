#!/usr/bin/env bash
# Ask a question about a recipe through llama-server's OpenAI-compatible API.
#   ./ask.sh                      # uses the pancake example below
#   PORT=8080 ./ask.sh "recipe text" "question"
set -euo pipefail
PORT=${PORT:-8080}
RECIPE=${1:-"Pancakes: 200 g flour, 2 eggs, 300 ml milk, a pinch of salt. Whisk, rest 30 minutes, fry in butter."}
QUESTION=${2:-"I want to make three times as much. How much milk?"}
python3 - "$RECIPE" "$QUESTION" <<'PY' | curl -s "http://127.0.0.1:$PORT/v1/chat/completions" -H "content-type: application/json" -d @- \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['choices'][0]['message']['content'])"
import json, sys
recipe, question = sys.argv[1], sys.argv[2]
print(json.dumps({
    "messages": [
        {"role": "system", "content": "You are a cooking assistant. You answer questions about dishes, ingredients, "
                                      "techniques and food safety. When you are not sure, you say so."},
        {"role": "user", "content": f"{recipe}\n\n{question}" if recipe else question},
    ],
    "chat_template_kwargs": {"enable_thinking": False},
    "max_tokens": 400,
}))
PY
