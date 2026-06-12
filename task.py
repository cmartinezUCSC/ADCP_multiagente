try:
    from crewai import Task
except ImportError:
    Task = None

def crear_tareas(
        problema,
        analista,
        disenador,
        programador,
        tester):

    analisis = Task(
        description=f"""
        Analiza este problema:

        {problema}

        Genera:

        - requisitos funcionales
        - entradas
        - salidas
        - restricciones
        - criterios de aceptación
        """,
        expected_output="Documento de análisis",
        agent=analista
    )

    diseno = Task(
        description="""
        Diseña una solución completa.
        Incluye algoritmo y pseudocódigo.
        """,
        expected_output="Documento de diseño",
        context=[analisis],
        agent=disenador
    )

    codigo = Task(
        description="""
        Implementa la solución en Python.
        """,
        expected_output="Código Python",
        context=[diseno],
        agent=programador
    )

    pruebas = Task(
        description="""
        Diseña casos de prueba y valida.
        """,
        expected_output="Informe QA",
        context=[codigo],
        agent=tester
    )

    return [analisis, diseno, codigo, pruebas]