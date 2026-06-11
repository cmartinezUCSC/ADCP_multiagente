"""Pruebas para el backend ADCP (sin llamadas reales a LLM)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Patch crewai before importing main to avoid needing real API keys in CI
_mock_crew_result = MagicMock()
_mock_crew_result.__str__ = lambda self: "resultado simulado del agente"

with patch("crewai.Crew.kickoff", return_value=_mock_crew_result):
    from main import app  # noqa: E402

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_analyze_missing_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    response = client.post("/analyze", json={"project_name": "Test"})
    assert response.status_code == 503
    assert "OPENAI_API_KEY" in response.json()["detail"]


def test_design_missing_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    response = client.post("/design", json={"project_name": "Test"})
    assert response.status_code == 503


def test_construct_missing_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    response = client.post("/construct", json={"project_name": "Test"})
    assert response.status_code == 503


def test_test_phase_missing_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    response = client.post("/test", json={"project_name": "Test"})
    assert response.status_code == 503


def test_analyze_with_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake")
    with patch("main.run_analyze", return_value="análisis simulado") as mock_fn:
        response = client.post(
            "/analyze",
            json={"project_name": "Mi Proyecto", "context": ""},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["phase"] == "Análisis"
    assert data["project_name"] == "Mi Proyecto"
    assert data["result"] == "análisis simulado"
    mock_fn.assert_called_once_with("Mi Proyecto", "")


def test_design_with_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake")
    with patch("main.run_design", return_value="diseño simulado"):
        response = client.post(
            "/design",
            json={"project_name": "Mi Proyecto", "context": "contexto previo"},
        )
    assert response.status_code == 200
    assert response.json()["result"] == "diseño simulado"


def test_construct_with_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake")
    with patch("main.run_construct", return_value="construcción simulada"):
        response = client.post(
            "/construct",
            json={"project_name": "Mi Proyecto"},
        )
    assert response.status_code == 200
    assert response.json()["phase"] == "Construcción"


def test_test_phase_with_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake")
    with patch("main.run_test", return_value="pruebas simuladas"):
        response = client.post(
            "/test",
            json={"project_name": "Mi Proyecto"},
        )
    assert response.status_code == 200
    assert response.json()["phase"] == "Pruebas"


def test_analyze_handles_agent_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake")
    with patch("main.run_analyze", side_effect=RuntimeError("LLM error")):
        response = client.post("/analyze", json={"project_name": "Test"})
    assert response.status_code == 500
    assert "LLM error" in response.json()["detail"]
