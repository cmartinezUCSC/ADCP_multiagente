"""
ADCP Multiagente — Backend FastAPI

Expone los endpoints para cada fase del ciclo ADCP.
Cada endpoint acepta el nombre del proyecto y contexto previo opcional.
"""

from __future__ import annotations

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from agents.adcp_agents import run_analyze, run_design, run_construct, run_test

load_dotenv()

app = FastAPI(
    title="ADCP Multiagente Backend",
    description="API REST para el flujo de Análisis, Diseño, Construcción y Pruebas (ADCP) con CrewAI.",
    version="0.1.0",
)

# Permitir peticiones desde la extensión VS Code (localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:*", "vscode-webview://*"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class PhaseRequest(BaseModel):
    project_name: str
    context: str = ""


class PhaseResponse(BaseModel):
    phase: str
    project_name: str
    result: str


def _require_api_key() -> None:
    """Verifica que OPENAI_API_KEY esté configurada antes de llamar a los agentes."""
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail=(
                "OPENAI_API_KEY no configurada. "
                "Copia backend/.env.example a backend/.env y agrega tu clave."
            ),
        )


@app.get("/health")
def health() -> dict[str, str]:
    """Endpoint de salud para verificar que el servidor está en línea."""
    return {"status": "ok", "version": "0.1.0"}


@app.post("/analyze", response_model=PhaseResponse)
def analyze(req: PhaseRequest) -> PhaseResponse:
    """Ejecuta la fase de Análisis con el agente analista de sistemas."""
    _require_api_key()
    try:
        result = run_analyze(req.project_name, req.context)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return PhaseResponse(phase="Análisis", project_name=req.project_name, result=result)


@app.post("/design", response_model=PhaseResponse)
def design(req: PhaseRequest) -> PhaseResponse:
    """Ejecuta la fase de Diseño con el agente arquitecto de software."""
    _require_api_key()
    try:
        result = run_design(req.project_name, req.context)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return PhaseResponse(phase="Diseño", project_name=req.project_name, result=result)


@app.post("/construct", response_model=PhaseResponse)
def construct(req: PhaseRequest) -> PhaseResponse:
    """Ejecuta la fase de Construcción con el agente desarrollador senior."""
    _require_api_key()
    try:
        result = run_construct(req.project_name, req.context)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return PhaseResponse(phase="Construcción", project_name=req.project_name, result=result)


@app.post("/test", response_model=PhaseResponse)
def test_phase(req: PhaseRequest) -> PhaseResponse:
    """Ejecuta la fase de Pruebas con el agente de QA."""
    _require_api_key()
    try:
        result = run_test(req.project_name, req.context)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return PhaseResponse(phase="Pruebas", project_name=req.project_name, result=result)
