# ADCP Multiagente

Sistema multi-agente de **Análisis, Diseño, Codificación y Pruebas** basado en [CrewAI](https://github.com/joaomdmoura/crewAI).

Dado un problema, cuatro agentes especializados trabajan en secuencia para producir:

1. **Análisis de requisitos** — entradas, salidas, restricciones y proceso mental de resolución.
2. **Diseño de solución** — algoritmo y pseudocódigo.
3. **Implementación** — código fuente en el lenguaje elegido por el usuario.
4. **Pruebas y validación** — casos normales, límites y errores con estado de aprobación.

---

## Autor

**Claudia Martínez-Araneda**

---

## Requisitos

- Python 3.11 (para las versiones más actualizada, CrewAI no es reconocida)
- Librería Python CreawAI
- Clave de API de OpenAI

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd ADCP_multiagente

# 2. Crear y activar entorno virtual
python -m venv .venv311
.\.venv311\Scripts\Activate   # Windows PowerShell

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env
# Editar .env y poner tu OPENAI_API_KEY
```

---

## Uso

```bash
.\.venv311\Scripts\python.exe main.py
```

El programa pedirá:
1. Lenguaje de programación para la solución (menú 1–11 o personalizado).
2. Descripción del problema a resolver.

Al finalizar, muestra la solución completa aplicando ADCP.

---

## Estructura del proyecto

```
ADCP_multiagente/
├── main.py           # Punto de entrada
├── agentes.py        # Definición de los cuatro agentes
├── tasks.py          # Definición de las cuatro tareas
├── orchestador.py    # Creación y configuración del crew
├── .env.example      # Plantilla de variables de entorno
├── requirements.txt  # Dependencias del proyecto
└── README.md
```

---

## Variables de entorno

Copia `.env.example` a `.env` y completa los valores:

Importante:
- No subas `.env` a GitHub.
- La clave de OpenAI debe vivir solo en tu archivo local `.env` o en variables de entorno del sistema.
- Si alguna vez una clave se expuso, revócala y genera una nueva antes de publicar.

| Variable        | Descripción                          | Ejemplo           |
|-----------------|--------------------------------------|-------------------|
| `LLM_PROVIDER`  | Proveedor del modelo (solo `openai`) | `openai`          |
| `OPENAI_MODEL`  | Modelo de OpenAI a usar              | `gpt-4o-mini`     |
| `OPENAI_API_KEY`| Tu clave de API de OpenAI            | `sk-...`          |

---

## Licencia
```
CC0 1.0 Universal
Claudia Martínez-Araneda
```
=======
# ADCP_multiagente
Automatización de ADCP por multiagentes
>>>>>>> b81a2ea48b00209b509237cd1836fd00521cc2c5
