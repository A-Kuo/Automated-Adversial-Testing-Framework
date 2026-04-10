"""
RTaaS — Red-Team-as-a-Service
==============================
Automated adversarial testing for LLMs with EU AI Act compliance reporting.

Quick start:
    from rtaas import Evaluator, AttackProfile

    evaluator = Evaluator(target_url="https://api.openai.com/v1/chat/completions")
    report = evaluator.run(
        profile=AttackProfile.FINANCIAL_COMPREHENSIVE,
        compliance_frameworks=["eu_ai_act"],
    )
    print(report.severity_summary())
"""

from rtaas.evaluator import Evaluator
from rtaas.attack_engine.library import AttackProfile

__all__ = ["Evaluator", "AttackProfile"]
__version__ = "0.1.0"
