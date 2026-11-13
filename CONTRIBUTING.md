# Contributing

Thanks for helping. Here is where each kind of report goes.

| You found | Where it goes |
|---|---|
| The model made up a quantity, step or ingredient, or gave unsafe food advice | [Model got something wrong](https://github.com/HumanjavaEnterprises/qwen3-8b-cooking-assistant/issues/new?template=wrong-answer.yml) |
| A wrong memory or speed figure, a broken command, or a bug in `examples/` or `tools/` | [Guide or tool bug](https://github.com/HumanjavaEnterprises/qwen3-8b-cooking-assistant/issues/new?template=bug.yml) |
| A typo, an unclear step, a missing setup | [Docs fix](https://github.com/HumanjavaEnterprises/qwen3-8b-cooking-assistant/issues/new?template=docs.yml), or open a pull request |
| A security problem | **Privately**, see [SECURITY.md](SECURITY.md) |
| You'd like to help check answers | [Label five answers](https://label-test.humanjava.com/?s=cook4&k=cook-9ac741a1e387&src=github-guide) on Label Test (blind, no account) |

## Pull requests

Welcome for the guide, examples and the memory estimator. Keep changes small and focused:

- Run the tests: `python -m pytest -q tests`.
- If you change a memory or speed figure, say what you measured on (GPU, runtime and version, quant, context).
- Code and docs here are MIT; by contributing you agree your contribution is MIT too.

The model weights and training are not developed in this repo, so pull requests can't change model behaviour. A
"model got something wrong" report is the way to influence the next version.
