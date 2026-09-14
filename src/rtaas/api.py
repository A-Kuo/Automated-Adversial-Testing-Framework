"""
Minimal REST API for RTaaS.

Exposes the evaluation pipeline over HTTP and serves a small static
dashboard for viewing results. Runs and stores evaluations in-memory —
no queue, no database. Start with:

    uvicorn rtaas.api:app --reload
"""

from __future__ import annotations

import uuid
from dataclasses import asdict
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from rtaas.attack_engine.library import AttackProfile
from rtaas.evaluator import EvaluationReport, Evaluator

app = FastAPI(title="RTaaS API", version="0.1.0")

_STATIC_DIR = Path(__file__).parent / "static"

_reports: dict[str, EvaluationReport] = {}


class EvaluateRequest(BaseModel):
    target_url: str
    target_auth: str | None = None
    target_model: str = "unknown"
    profile: str = "general_basic"
    compliance_frameworks: list[str] = ["eu_ai_act", "nist_ai_rmf"]
    max_attacks: int = 50


class EvaluateResponse(BaseModel):
    run_id: str
    report: dict[str, Any]


class RunSummary(BaseModel):
    run_id: str
    target: str
    model: str
    profile: str
    timestamp: str
    total_attacks: int
    failures: int


@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest) -> EvaluateResponse:
    try:
        profile = AttackProfile(req.profile)
    except ValueError:
        valid = [p.value for p in AttackProfile]
        raise HTTPException(400, f"Unknown profile '{req.profile}'. Valid: {valid}")

    evaluator = Evaluator(target_url=req.target_url, target_auth=req.target_auth)
    report = evaluator.run(
        profile=profile,
        compliance_frameworks=req.compliance_frameworks,
        max_attacks=req.max_attacks,
        target_model=req.target_model,
        verbose=False,
    )

    run_id = uuid.uuid4().hex[:12]
    _reports[run_id] = report
    return EvaluateResponse(run_id=run_id, report=asdict(report))


@app.get("/reports", response_model=list[RunSummary])
def list_reports() -> list[RunSummary]:
    summaries = []
    for run_id, report in _reports.items():
        failures = sum(1 for f in report.findings if f.severity != "PASS")
        summaries.append(
            RunSummary(
                run_id=run_id,
                target=report.target,
                model=report.model,
                profile=report.profile,
                timestamp=report.timestamp,
                total_attacks=report.total_attacks,
                failures=failures,
            )
        )
    return summaries


@app.get("/reports/{run_id}")
def get_report(run_id: str) -> dict[str, Any]:
    report = _reports.get(run_id)
    if report is None:
        raise HTTPException(404, f"No report found for run_id '{run_id}'")
    return asdict(report)


@app.get("/")
def dashboard() -> FileResponse:
    return FileResponse(_STATIC_DIR / "dashboard.html")


app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")
