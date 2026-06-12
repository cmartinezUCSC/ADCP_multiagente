try:
    from crewai import Task
except ImportError:
    Task = None

def crear_tareas(
        problema,
        lenguajeprograma,
        analista,
        disenador,
        programador,
        tester):

    analisis = Task(
        description=f"""
        Analiza este problema:

        {problema}

        Genera:
        - entradas
        - proceso mental para resolverlo (incluye pasos, decisiones, formulas, criterios de aceptación, según corresponda)
        - salidas
        - restricciones
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
        description=f"""
        Implementa la solución en código {lenguajeprograma} sin usar atajos ni librerías externas.
        """,
        expected_output=f"Código fuente en {lenguajeprograma}",
        context=[diseno],
        agent=programador
    )

    pruebas = Task(
        description="""
        Diseña casos de prueba y validación.
            - Cubre casos normales, límites y errores.
            - Explica cómo validar cada caso.
            - Indica el estado de la prueba (aprobada, fallida).
            """,    
        expected_output="Informe QA o pruebas",
        context=[codigo],
        agent=tester
    )

    return [analisis, diseno, codigo, pruebas]