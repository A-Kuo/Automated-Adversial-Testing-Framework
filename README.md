# Red-Team-as-a-Service (RTaaS)

> Automated adversarial testing for any LLM — at scale, with compliance-ready reports.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Research/Concept](https://img.shields.io/badge/status-research--concept-orange.svg)]()
[![EU AI Act](https://img.shields.io/badge/compliance-EU_AI_Act-purple.svg)]()

**Status:** Research concept and architecture design. Core evaluation engine and attack library are being developed.  
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
report.export_pdf("compliance_report.pdf")
```

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
│   ├── evaluator.py              # Main evaluation orchestrator
│   ├── attack_engine/
│   │   ├── library.py            # Static attack library loader (YAML)
│   │   ├── mutation.py           # LLM-vs-LLM mutation engine
│   │   └── coverage.py           # Coverage metric tracker
│   ├── eval_engine/
│   │   ├── target.py             # Target model interface (OpenAI, HF, local)
│   │   ├── harm_classifier.py    # Harm scoring (LlamaGuard-3)
│   │   ├── entropy_scorer.py     # AED-based hallucination risk scoring
│   │   └── factual_verifier.py   # Ground-truth fact checking
│   ├── compliance/
│   │   ├── mapper.py             # Finding → regulatory framework mapping
│   │   └── frameworks/           # YAML configs: eu_ai_act.yml, nist_ai_rmf.yml, ...
│   └── reporting/
│       ├── generator.py          # Report builder
│       └── templates/            # PDF and JSON templates
│
├── attacks/                      # Attack library (YAML files)
│   ├── financial/
│   ├── medical/
│   ├── legal/
│   └── jailbreak/
│
├── tests/
├── ARCHITECTURE.md               # Full system architecture
├── RESEARCH_QUESTIONS.md         # Open research questions
├── BUSINESS_CASE.md              # Market analysis and commercialization strategy
└── pyproject.toml
```

---

## Roadmap

- [ ] Core evaluation loop (target interface → attack → score)
- [ ] Static attack library: financial and jailbreak profiles
- [ ] Harm classifier integration (LlamaGuard-3)
- [ ] AED entropy scorer integration
- [ ] EU AI Act compliance mapper
- [ ] JSON report output
- [ ] PDF report generation
- [ ] Dynamic mutation engine (LLM-vs-LLM)
- [ ] Continuous monitoring mode
- [ ] REST API (FastAPI)
- [ ] Python SDK

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
