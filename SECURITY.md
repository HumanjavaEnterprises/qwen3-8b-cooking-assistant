# Security Policy

This project publishes a **cooking assistant model** (weights on Hugging Face and Ollama), the **chat template and
settings** that ship with it, and this guide's **examples and memory estimator**. People run these on their own
machines, so we treat integrity reports as a priority.

> **Verify your download.** Each Hugging Face repo has a `SHA256SUMS` file: `sha256sum -c SHA256SUMS`.
> Use the latest version (or pin a version tag such as `v1`).

## Reporting a vulnerability

**Please report security issues privately. Do not open a public issue.**

- Use GitHub's **private vulnerability reporting** (Security tab → "Report a vulnerability"), or
- email **security@humanjava.com** with details and steps to reproduce.

Please include what you found and its impact, how to reproduce it, and the version you used (Hugging Face revision or
version tag, Ollama tag, and your runtime: Ollama / llama.cpp / LM Studio / vLLM version).

### What to expect
- Acknowledgement within **3 business days**.
- An initial assessment within **7 business days**.
- Coordinated disclosure: we agree a timeline with you before any public detail, and credit you (if you wish) once a
  fix ships.

## Supported versions

| Component | Supported |
|---|---|
| Latest version on Hugging Face and Ollama (`latest`, `v1`) | ✅ |
| This guide on `main` | ✅ |
| Older revisions | ❌ (please update) |

## In scope
- **Weight integrity:** published files that don't match `SHA256SUMS` or the card.
- **Embedded content:** anything in the GGUF metadata, the chat template, or the Ollama `template` / `system` /
  `params` files beyond what is documented.
- **Examples and tools in this repo:** anything that could run unexpected code or expose data on your machine.

## Not security issues (but please tell us)
- **Wrong or unsafe cooking answers** (invented quantities, bad food-safety advice): open a
  ["Model got something wrong"](https://github.com/HumanjavaEnterprises/qwen3-8b-cooking-assistant/issues/new?template=wrong-answer.yml)
  issue. These are quality reports, and they help us improve the next version.
- Jailbreaks or off-topic outputs: the model is a cooking assistant, not a safety system. Report them as a wrong
  answer if they matter to your use.
