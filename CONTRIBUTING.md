# Contributing to RTaaS

## Development setup

```bash
git clone https://github.com/A-Kuo/rtaas.git
cd rtaas
pip install -e ".[dev,api]"
```

## Before opening a PR

```bash
pytest tests/ -v
ruff check src/
mypy src/
```

All three must pass; CI runs the same checks.

## Adding an attack

1. Extend the seed list in `src/rtaas/attack_engine/library.py` (there is no
   `attacks/` YAML directory yet — see the Roadmap in `README.md`).
2. Include `attack_id`, `prompt`, `harm_category`, `severity_if_failed`, and
   regulatory mappings.
3. Add or update a test in `tests/` covering the new attack's expected
   classification.
4. Open a PR with a brief justification for the attack's inclusion.
