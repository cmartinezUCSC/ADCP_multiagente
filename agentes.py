# ADCP Multiagente — agentes.py
# Autora: Claudia Martínez-Araneda

import os
import warnings
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# CrewAI 0.11.x y algunas dependencias aún mezclan modelos pydantic v1/v2.
# Filtramos solo este warning puntual para mantener salida limpia.
warnings.filterwarnings(
    "ignore",
    message=r"Mixing V1 models and V2 models.*CrewAgentExecutor.*",
    category=UserWarning,
)

try:
    from crewai import Agent
except ImportError:
    raise ImportError("The 'crewai' package is not installed. Please install it using: pip install crewai")


PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env", override=False)


def _build_llm_from_env():
    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    if provider != "openai":
        raise ValueError(
            "LLM_PROVIDER no soportado en esta configuración. "
            "Usa 'openai' para este proyecto."
        )

    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key:
        raise EnvironmentError(
            "Falta OPENAI_API_KEY. Define la variable en .env o en tu entorno."
        )

    return ChatOpenAI(model=model_name, api_key=api_key, temperature=0)


LLM = _build_llm_from_env()

analista = Agent(
    role="Analista de Requisitos",
    goal="""
    Transformar problemas en requisitos precisos.
    """,
    backstory="""
    Especialista en análisis de sistemas.
    """,
    llm=LLM,
    verbose=True,
    language="es"
)

disenador = Agent(
    role="Arquitecto de Software",
    goal="""
    Diseñar algoritmos y estructuras.
    """,
    backstory="""
    Arquitecto de software senior.
    """,
    llm=LLM,
    verbose=True,
    language="es"
)

programador = Agent(
    role="Desarrollador Python",
    goal="""
    Solicitar el lenguaje de programación y generar código en el lenguaje solicitado.
    """,
    backstory="""
    Experto en Python.
    """,
    llm=LLM,
    verbose=True,
    language="es"
)

tester = Agent(
    role="QA Engineer",
    goal="""
    Validar la solución.
    """,
    backstory="""
    Especialista en testing.
    """,
    llm=LLM,
    verbose=True,
    language="es"
)