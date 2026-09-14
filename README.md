# Red-Team-as-a-Service (RTaaS)

> Automated adversarial testing for any LLM — at scale, with compliance-ready reports.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Pre-Alpha](https://img.shields.io/badge/status-pre--alpha-orange.svg)]()
[![EU AI Act](https://img.shields.io/badge/compliance-EU_AI_Act-purple.svg)]()

**Status:** Pre-alpha. The core evaluation loop, seed attack library, heuristic
harm classifier, compliance mapper, JSON reporting, and a minimal REST API +
dashboard are implemented and tested. Entropy/hallucination scoring,
LlamaGuard integration, PDF export, and the dynamic mutation engine are not
yet built — see the Roadmap below for exact status.  
**Rooted in:** [AI-Safety-Benchmarking-RedTeam-Framework](https://github.com/A-Kuo/AI-Safety-Benchmarking-RedTeam-Framework) and [Language-Model-Hallucination-Detection-via-Entropy-Divergence](https://github.com/A-Kuo/Language-Model-Hallucination-Detection-via-Entropy-Divergence)

---

## The Problem

Every organization deploying an LLM in 2026 faces the same liability question: *"How do we know it won't say something catastrophic — and how do we prove we checked?"*

Regulators have answered: they must check, systematically, and document the results.

- **EU AI Act** (enforcement August 2026): LLMs in healthcare, legal, HR, and public infrastructure are classified "high-risk AI systems" requiring documented conformity assessments including adversarial testing under Article 9.
- **NIST AI RMF 1.0**: Organizations must "identify and analyze potential harms" including adversarial inputs.
- **White House EO on AI Safety**: Federal agencies must conduct red-team exercises before deployment.

The gap: **a scalable, API-accessible red-teaming service that produces structured vulnerability assessments and compliance-ready reports, without requiring in-house red-teaming expertise.**

---

## What RTaaS Does

RTaaS accepts a model endpoint (or HuggingFace model ID), runs a comprehensive adversarial evaluation, and returns:

1. **Structured vulnerability report** — findings mapped to harm categories and regulatory frameworks
2. **Severity scores** — per finding, using a multi-dimensional rubric (harm severity × confidence × exploitability)
3. **Entropy-divergence scores** — hallucination-severity scoring alongside harm classification (from the [AED methodology](https://github.com/A-Kuo/Language-Model-Hallucination-Detection-via-Entropy-Divergence))
4. **Compliance mapping** — EU AI Act Articles, NIST AI RMF functions, and domain-specific regulations
5. **Remediation recommendations** — specific prompt engineering or fine-tuning suggestions per vulnerability class

---

## Architecture

```
Attack Library ──► Attacker LLM ──► Target Model
     │                  │               │
Mutation Engine    Coverage Guide   Response Logger
                        │               │
                   ◄────┘               ▼
                                  Scoring Engine
                                        │
                                  Entropy Scorer
                                  Harm Classifier
                                  Compliance Mapper
                                        │
                                  Report Generator
                                  PDF + JSON + API
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for full component specifications.

---

## Quick Start

```bash
git clone https://github.com/A-Kuo/rtaas.git
cd rtaas
pip install -e ".[dev]"

# Run a quick evaluation against any OpenAI-compatible endpoint
python -m rtaas.cli evaluate \
  --target-url https://api.openai.com/v1/chat/completions \
  --target-model gpt-4o-mini \
  --attack-profile financial_basic \
  --output report.json
```

### Python API

```python
from rtaas import Evaluator, AttackProfile

evaluator = Evaluator(target_url="https://your-model-api.com/v1/chat")

report = evaluator.run(
    profile=AttackProfile.FINANCIAL_COMPREHENSIVE,
    compliance_frameworks=["eu_ai_act", "nist_ai_rmf"],
    max_attacks=500,
)

print(report.severity_summary())
report.export_json("compliance_report.json")
```

### REST API + Dashboard

```bash
pip install -e ".[dev,api]"
./run_dashboard.sh        # or: uvicorn rtaas.api:app --reload
```

Then open **`http://localhost:8000/` in a browser** for a minimal
dashboard: kick off an evaluation, watch past runs, and inspect severity
distribution and compliance gaps for a selected run. `POST /evaluate`,
`GET /reports`, and `GET /reports/{run_id}` are also usable directly.

> Open the app via that `http://` URL — never open
> `src/rtaas/static/dashboard.html` directly as a local file. Its
> `fetch()` calls are relative and need to be served from the running
> app's origin; loaded as a bare file they resolve against `file://` and
> fail.

---

## Attack Coverage

| Category | Examples | Regulatory Hook |
|----------|----------|-----------------|
| **Jailbreak & Safety Bypass** | DAN variants, roleplay, persona injection, multi-turn erosion | EU AI Act Art. 9 |
| **Hallucination & Factual Reliability** | Numeric facts, citations, medical contraindications | EU AI Act Art. 13 |
| **Medical Risk** | Diagnosis prompts, drug dosing, treatment recommendations | FDA AI/ML-SaMD guidance |
| **Financial Risk** | Investment advice, tax guidance, regulatory queries | SEC AI guidance, FINRA Notice 24-09 |
| **Legal Risk** | Legal advice provision, case law fabrication | ABA Formal Opinion 512 |
| **Adversarial Robustness** | Typographic attacks, paraphrase, few-shot priming, language switching | NIST AI RMF MAP |

---

## Sample Report Output

```
VULNERABILITY ASSESSMENT REPORT
================================
Target: gpt-4o-financial-finetuned
Date: 2026-04-10
Profile: financial_llm_comprehensive (500 attacks)
Failures: 23/500 (4.6%)

SEVERITY DISTRIBUTION:
  Critical:  3 (0.6%)  — Requires immediate remediation
  High:      8 (1.6%)  — Remediate before production
  Medium:   12 (2.4%)  — Address within 30 days

EU AI ACT STATUS:
  Art. 9 (Risk Management):  PARTIAL — 2 high-risk gaps
  Art. 10 (Data Governance): PASS
  Art. 13 (Transparency):    FAIL — AI not identified in 18% of responses

NIST AI RMF:
  GOVERN: PARTIAL | MAP: PASS | MEASURE: FAIL | MANAGE: PARTIAL
```

---

## Integration With the Entropy Divergence Work

RTaaS integrates the AED (Attention Entropy Divergence) hallucination detection system as a complementary scoring dimension. Where traditional red-teaming only asks *"is this harmful?"*, RTaaS also asks *"is this uncertain?"* — a critical distinction for:

- **Financial LLMs**: High-entropy responses about market data or regulatory rules should trigger compliance review
- **Medical LLMs**: High-entropy responses about drug dosing are a patient safety risk independent of harm label
- **Legal LLMs**: Fabricated case citations are both high-entropy and high-harm

This gives customers a two-dimensional risk matrix: `(harm_severity, hallucination_risk)`.

---

## Repository Structure

```
rtaas/
├── src/rtaas/
│   ├── __init__.py
│   ├── cli.py                    # CLI entry point
│   ├── api.py                    # Minimal FastAPI REST API + dashboard route
│   ├── evaluator.py              # Main evaluation orchestrator
│   ├── static/
│   │   └── dashboard.html        # Single-page results viewer (served by api.py)
│   ├── attack_engine/
│   │   ├── library.py            # Attack library (hardcoded seed list; YAML loading path exists but unused)
│   │   └── coverage.py           # Coverage metric tracker
│   ├── eval_engine/
│   │   ├── target.py             # Target model interface (OpenAI-compatible)
│   │   └── harm_classifier.py    # Heuristic harm scoring (LlamaGuard-3 path stubbed)
│   └── compliance/
│       └── mapper.py             # Finding → regulatory framework mapping (EU AI Act, NIST AI RMF)
│
├── tests/
├── ARCHITECTURE.md               # Full (partly aspirational) system architecture
├── RESEARCH_QUESTIONS.md         # Open research questions
├── BUSINESS_CASE.md              # Market analysis and commercialization strategy
├── CONTRIBUTING.md               # Dev setup and contribution guide
├── .env.example                  # Environment variables (OPENAI_API_KEY)
└── pyproject.toml
```

Not yet implemented (see Roadmap): `attack_engine/mutation.py`,
`eval_engine/entropy_scorer.py`, `eval_engine/factual_verifier.py`,
`compliance/frameworks/*.yml`, `reporting/` (PDF/JSON templates), and the
`attacks/` YAML directory.

---

## Roadmap

- [x] Core evaluation loop (target interface → attack → score)
- [x] Static attack library: financial, medical, and jailbreak seed attacks
      (hardcoded seed list; YAML-file loading is wired but no `attacks/`
      directory exists yet)
- [ ] Harm classifier integration (LlamaGuard-3) — heuristic keyword
      classifier only; LlamaGuard path is a stub (`NotImplementedError`)
- [ ] AED entropy scorer integration — not implemented
- [x] EU AI Act / NIST AI RMF compliance mapper (wired into `Evaluator.run()`)
- [x] JSON report output
- [ ] PDF report generation
- [ ] Dynamic mutation engine (LLM-vs-LLM)
- [ ] Continuous monitoring mode
- [x] Minimal REST API (FastAPI) + static dashboard — single-process,
      in-memory only; no queue/worker, no persistence
- [ ] Python SDK (beyond the `Evaluator`/`AttackProfile` library import)

---

## Related Work

This project productizes and extends:

- **[AI-Safety-Benchmarking-RedTeam-Framework](https://github.com/A-Kuo/AI-Safety-Benchmarking-RedTeam-Framework)** — the existing benchmark collection, evaluation harnesses, and scoring rubrics that form the core attack library and methodology.
- **[Language-Model-Hallucination-Detection-via-Entropy-Divergence](https://github.com/A-Kuo/Language-Model-Hallucination-Detection-via-Entropy-Divergence)** — the AED hallucination detection system integrated as the entropy scoring dimension.

---

## Contributing

Attack library contributions are especially welcome. To add an attack:

1. Create a YAML file in the appropriate `attacks/` subdirectory
2. Follow the schema in `attacks/README.md`
3. Include: `attack_id`, `prompt`, `harm_category`, `severity_if_failed`, regulatory mappings
4. Open a PR with a brief justification for the attack's inclusion

See [CONTRIBUTING.md](CONTRIBUTING.md) for full contribution guidelines.

---

*April 2026 — A-Kuo*
