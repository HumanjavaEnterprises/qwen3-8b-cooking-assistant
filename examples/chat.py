"""Talk to the model from Python through any OpenAI-compatible server (llama-server, Ollama, LM Studio, vLLM).

    pip install openai
    python chat.py                                  # llama-server on :8080
    BASE_URL=http://127.0.0.1:11434/v1 MODEL=cooking python chat.py   # Ollama
"""
import os

from openai import OpenAI

SYSTEM = ("You are a cooking assistant. You answer questions about dishes, ingredients, techniques and food safety. "
          "When you are not sure, you say so.")

client = OpenAI(base_url=os.environ.get("BASE_URL", "http://127.0.0.1:8080/v1"), api_key="not-needed")
model = os.environ.get("MODEL", "cooking")


def ask(question, recipe=None):
    """Put the recipe in the same turn as the question. Without one, the model asks for it instead of guessing."""
    content = f"{recipe}\n\n{question}" if recipe else question
    r = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": content}],
        max_tokens=400,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )
    return r.choices[0].message.content


if __name__ == "__main__":
    recipe = "Pancakes: 200 g flour, 2 eggs, 300 ml milk, a pinch of salt. Whisk, rest 30 minutes, fry in butter."
    print("With the recipe:\n", ask("I want to make three times as much. How much milk?", recipe), "\n")
    print("Without it:\n", ask("If I triple my pancake recipe, how much milk do I need?"))
