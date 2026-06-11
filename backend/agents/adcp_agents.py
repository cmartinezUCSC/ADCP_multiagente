"""
ADCP Multiagente — Agentes CrewAI para cada fase del ciclo ADCP.

Cada fase usa un agente especializado y una tarea concreta.
El contexto de fases anteriores se pasa como entrada adicional.
"""

from __future__ import annotations

import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()

_MODEL = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")


def _make_agent(role: str, goal: str, backstory: str) -> Agent:
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        verbose=True,
        llm=_MODEL,
    )


def run_analyze(project_name: str, context: str = "") -> str:
    """Fase Análisis: levantamiento de requisitos y casos de uso."""
    agent = _make_agent(
        role="Analista de Sistemas",
        goal=(
            "Identificar y documentar los requisitos funcionales y no funcionales "
            "del sistema, junto con los principales casos de uso."
        ),
        backstory=(
            "Eres un analista experto con 15 años de experiencia levantando "
            "requisitos para sistemas de software empresariales y educativos."
        ),
    )

    description = (
        f"Proyecto: {project_name}\n"
        "Realiza un análisis completo que incluya:\n"
        "1. Descripción general del sistema\n"
        "2. Stakeholders y sus necesidades\n"
        "3. Requisitos funcionales (al menos 5)\n"
        "4. Requisitos no funcionales (rendimiento, seguridad, usabilidad)\n"
        "5. Casos de uso principales (diagrama textual)\n"
        "6. Restricciones y supuestos"
    )
    if context:
        description += f"\n\nContexto previo:\n{context}"

    task = Task(
        description=description,
        expected_output=(
            "Documento de análisis estructurado en secciones claras con "
            "todos los puntos solicitados."
        ),
        agent=agent,
    )

    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
    result = crew.kickoff()
    return str(result)


def run_design(project_name: str, context: str = "") -> str:
    """Fase Diseño: arquitectura, modelo de datos y diseño de interfaces."""
    agent = _make_agent(
        role="Arquitecto de Software",
        goal=(
            "Diseñar la arquitectura del sistema, el modelo de datos y "
            "las interfaces de usuario a partir de los requisitos analizados."
        ),
        backstory=(
            "Eres un arquitecto de software con experiencia en patrones "
            "MVC, microservicios, y diseño orientado a dominio (DDD)."
        ),
    )

    description = (
        f"Proyecto: {project_name}\n"
        "Elabora el diseño del sistema que incluya:\n"
        "1. Arquitectura del sistema (capas o componentes)\n"
        "2. Diagrama de clases principal (en texto/UML simplificado)\n"
        "3. Modelo de datos (entidades y relaciones)\n"
        "4. Diseño de interfaces de usuario (wireframe textual)\n"
        "5. Diagrama de secuencia para el flujo principal\n"
        "6. Tecnologías y frameworks recomendados"
    )
    if context:
        description += f"\n\nAnálisis previo:\n{context}"

    task = Task(
        description=description,
        expected_output=(
            "Documento de diseño con arquitectura, modelos y diagramas textuales."
        ),
        agent=agent,
    )

    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
    result = crew.kickoff()
    return str(result)


def run_construct(project_name: str, context: str = "") -> str:
    """Fase Construcción: generación de código esqueleto y guía de implementación."""
    agent = _make_agent(
        role="Desarrollador de Software Senior",
        goal=(
            "Generar el código esqueleto del sistema y una guía de implementación "
            "paso a paso para el equipo de desarrollo."
        ),
        backstory=(
            "Eres un desarrollador full-stack con expertise en Python, "
            "TypeScript y buenas prácticas de ingeniería de software."
        ),
    )

    description = (
        f"Proyecto: {project_name}\n"
        "Genera el esqueleto de implementación que incluya:\n"
        "1. Estructura de directorios del proyecto\n"
        "2. Código esqueleto de los módulos principales (con comentarios)\n"
        "3. Configuración del entorno de desarrollo\n"
        "4. Ejemplo de implementación del módulo más crítico\n"
        "5. Guía de estilo y convenciones de código\n"
        "6. Lista de dependencias y su justificación"
    )
    if context:
        description += f"\n\nDiseño previo:\n{context}"

    task = Task(
        description=description,
        expected_output=(
            "Código esqueleto con estructura de proyecto, ejemplos concretos y guía."
        ),
        agent=agent,
    )

    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
    result = crew.kickoff()
    return str(result)


def run_test(project_name: str, context: str = "") -> str:
    """Fase Pruebas: plan de pruebas y casos de prueba unitarios/integración."""
    agent = _make_agent(
        role="Ingeniero de QA y Pruebas",
        goal=(
            "Definir un plan de pruebas completo e implementar casos de prueba "
            "unitarios e integración para el sistema."
        ),
        backstory=(
            "Eres un ingeniero de QA especializado en TDD, BDD y pruebas "
            "automatizadas con pytest y Jest."
        ),
    )

    description = (
        f"Proyecto: {project_name}\n"
        "Elabora el plan de pruebas que incluya:\n"
        "1. Estrategia de pruebas (unitarias, integración, E2E)\n"
        "2. Criterios de aceptación por módulo\n"
        "3. Casos de prueba unitarios (al menos 5, con código)\n"
        "4. Casos de prueba de integración principales\n"
        "5. Métricas de cobertura objetivo\n"
        "6. Plan de pruebas de regresión"
    )
    if context:
        description += f"\n\nImplementación previa:\n{context}"

    task = Task(
        description=description,
        expected_output=(
            "Plan de pruebas completo con casos de prueba en código y métricas."
        ),
        agent=agent,
    )

    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
    result = crew.kickoff()
    return str(result)
