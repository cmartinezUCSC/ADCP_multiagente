from typing import List, Optional
from crewai import Crew, Process


def _crear_step_callback(etapas: List[str]):
    estado = {"indice": 0, "total": len(etapas)}

    def _callback(step_output):
        # step_callback se ejecuta en cada paso; nos interesa cuando una tarea termina.
        if step_output.__class__.__name__ != "AgentFinish":
            return

        estado["indice"] += 1
        indice = estado["indice"]

        if indice <= estado["total"]:
            etapa = etapas[indice - 1]
            porcentaje = int((indice / estado["total"]) * 100)
            print(f"\n[PROGRESO] [{indice}/{estado['total']}] {etapa} completada ({porcentaje}%)")

    return _callback

def crear_crew(
        agents: List,
        tasks: List,
        etapas: Optional[List[str]] = None) -> Crew:

    step_callback = _crear_step_callback(etapas) if etapas else None

    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        step_callback=step_callback
    )

    return crew