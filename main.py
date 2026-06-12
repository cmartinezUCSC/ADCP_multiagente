import contextlib
import io
import re

from agentes import *
from tasks import crear_tareas
from orchestador import crear_crew

try:
    from sympy import Eq, pretty
    from sympy.parsing.sympy_parser import (
        convert_xor,
        implicit_multiplication_application,
        parse_expr,
        standard_transformations,
    )

    HAS_SYMPY = True
    PARSE_TRANSFORMATIONS = standard_transformations + (
        implicit_multiplication_application,
        convert_xor,
    )
except ImportError:
    HAS_SYMPY = False
    PARSE_TRANSFORMATIONS = ()


MOSTRAR_SOLO_VERDE = True
ANSI_VERDE_RE = re.compile(r"\x1b\[[0-9;]*32m")


def seleccionar_lenguaje() -> str:
    opciones = {
        "1": "Python",
        "2": "Java",
        "3": "C",
        "4": "C++",
        "5": "C#",
        "6": "JavaScript",
        "7": "TypeScript",
        "8": "Go",
        "9": "Rust",
        "10": "Pseint",
        "11": "Otro",
    }
    print("\nSelecciona el lenguaje de programación para la etapa de codificación:")
    for clave, lenguaje in opciones.items():
        print(f"{clave}. {lenguaje}")

    while True:
        seleccion = input("Selecciona una opción (1-11): ").strip()
        if seleccion in opciones:
            if seleccion == "11":
                personalizado = input("Escribe el lenguaje que deseas: ").strip()
                if personalizado:
                    return personalizado
                print("Debes escribir un lenguaje válido.")
                continue
            return opciones[seleccion]

        print("Opción inválida. Intenta de nuevo.")


def _es_candidato_matematico(linea: str) -> bool:
    texto = linea.strip()
    if not texto:
        return False

    # Quitamos prefijos comunes de listas Markdown sin perder la expresión.
    texto = re.sub(r"^[-*]\s+", "", texto)
    texto = re.sub(r"^\d+[.)]\s+", "", texto)

    # Limitamos a líneas "parecidas" a una expresión para evitar falsos positivos.
    if not re.fullmatch(r"[A-Za-z0-9_+\-*/^=().,\s]+", texto):
        return False

    if not re.search(r"[+\-*/^=]", texto):
        return False

    return True


def _formatear_expresion(linea: str):
    if not HAS_SYMPY or not _es_candidato_matematico(linea):
        return None

    texto = linea.strip()
    texto = re.sub(r"^[-*]\s+", "", texto)
    texto = re.sub(r"^\d+[.)]\s+", "", texto)

    try:
        if "=" in texto:
            lhs_text, rhs_text = texto.split("=", 1)
            lhs = parse_expr(lhs_text.strip(), transformations=PARSE_TRANSFORMATIONS)
            rhs = parse_expr(rhs_text.strip(), transformations=PARSE_TRANSFORMATIONS)
            return pretty(Eq(lhs, rhs), use_unicode=False)

        expr = parse_expr(texto, transformations=PARSE_TRANSFORMATIONS)
        return pretty(expr, use_unicode=False)
    except Exception:
        return None


def imprimir_resultado_formateado(resultado):
    contenido = str(resultado)
    for linea in contenido.splitlines():
        print(linea)

        expresion = _formatear_expresion(linea)
        if expresion and expresion.strip() and expresion.strip() != linea.strip():
            print("    [math]")
            for sublinea in expresion.splitlines():
                print(f"    {sublinea}")


def kickoff_mostrando_solo_verde(crew_obj):
    if not MOSTRAR_SOLO_VERDE:
        return crew_obj.kickoff()

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        resultado_local = crew_obj.kickoff()

    for linea in buffer.getvalue().splitlines():
        if ANSI_VERDE_RE.search(linea):
            print(linea)

    return resultado_local


print("ADCP Multiagente - Análisis, Diseño, Codificación y Pruebas")
start = input("Presiona Enter para iniciar...")

lenguajeprograma = seleccionar_lenguaje()
print(f"Lenguaje seleccionado: {lenguajeprograma}\n")

problema = input(
    "Ingrese el problema:\n"
)

tareas = crear_tareas(
    problema,
    lenguajeprograma,
    analista,
    disenador,
    programador,
    tester,
)

etapas = [
    "Análisis de requisitos",
    "Diseño de solución",
    "Implementación",
    "Pruebas y validación",
]

crew = crear_crew(
    [
        analista,
        disenador,
        programador,
        tester
    ],
    tareas,
    etapas
)

resultado = kickoff_mostrando_solo_verde(crew)

print("\n")
print("SOLUCIÓN FINAL")
print("="*50)
imprimir_resultado_formateado(resultado)
