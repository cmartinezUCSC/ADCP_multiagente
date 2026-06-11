# ADCP Multiagente

Automatización del flujo **ADCP** (Análisis, Diseño, Construcción, Pruebas) mediante multiagentes de IA.

Combina una **extensión de VS Code** con un **backend FastAPI + CrewAI** para guiar a equipos o estudiantes a través de cada fase del ciclo de desarrollo de software usando agentes especializados.

---

## Arquitectura

```
┌─────────────────────────┐        HTTP/REST       ┌──────────────────────────┐
│   VS Code Extension     │ ──────────────────────► │  FastAPI Backend         │
│  (TypeScript)           │                         │  (Python + CrewAI)       │
│                         │                         │                          │
│  • Sidebar con fases    │ ◄────────────────────── │  POST /analyze           │
│  • Webview de resultados│   JSON { result: ... }  │  POST /design            │
│  • Estado por workspace │                         │  POST /construct         │
│                         │                         │  POST /test              │
└─────────────────────────┘                         └──────────────────────────┘
                                                              │
                                                              ▼
                                                     Agentes CrewAI (LLM)
                                                     • Analista de Sistemas
                                                     • Arquitecto de Software
                                                     • Desarrollador Senior
                                                     • Ingeniero de QA
```

---

## Requisitos previos

| Herramienta | Versión mínima |
|-------------|----------------|
| Node.js     | 18+            |
| Python      | 3.10+          |
| VS Code     | 1.85+          |
| OpenAI API Key | cualquiera  |

---

## Configuración

### 1. Backend (Python)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar tu OPENAI_API_KEY
```

Iniciar el servidor:

```bash
uvicorn main:app --reload --port 8000
```

El backend quedará disponible en `http://localhost:8000`. Puedes explorar la API en `http://localhost:8000/docs`.

### 2. Extensión VS Code

```bash
cd vscode-extension
npm install
npm run compile
```

Para **instalar en VS Code** (modo desarrollo):

1. Abre VS Code
2. Presiona `F5` dentro de la carpeta `vscode-extension/` para abrir una ventana de extensión de desarrollo
3. O ejecuta `vsce package` para generar el archivo `.vsix` e instalarlo manualmente

---

## Uso

1. **Inicia el backend** antes de usar la extensión (ver arriba), o usa el comando `ADCP: Iniciar Backend` desde la paleta de comandos.
2. En VS Code, haz clic en el ícono **ADCP Multiagente** en la barra de actividad (izquierda).
3. Sigue el flujo secuencial de fases:

| Comando                | Descripción                                          |
|------------------------|------------------------------------------------------|
| `ADCP: Análisis`       | Genera requisitos funcionales/no funcionales y casos de uso |
| `ADCP: Diseño`         | Produce arquitectura, modelo de datos e interfaces    |
| `ADCP: Construcción`   | Genera código esqueleto y guía de implementación     |
| `ADCP: Pruebas`        | Crea plan de pruebas y casos de prueba en código     |
| `ADCP: Mostrar Panel`  | Abre el webview con todos los resultados acumulados  |
| `ADCP: Reiniciar Estado` | Borra el estado del proyecto actual               |

4. Cada fase pasa automáticamente el resultado de la fase anterior como contexto al agente siguiente.
5. Los resultados se persisten en el `workspaceState` de VS Code (sobreviven cierres del editor).

---

## Configuración de la extensión

| Ajuste                  | Por defecto              | Descripción                              |
|-------------------------|--------------------------|------------------------------------------|
| `adcp.backendUrl`       | `http://localhost:8000`  | URL del servidor backend                 |
| `adcp.autoStartBackend` | `false`                  | Verificar el backend al activar la ext. |

---

## Desarrollo y pruebas

### Backend

```bash
cd backend
python3 -m pytest tests/ -v
```

### Extensión

```bash
cd vscode-extension
npm run compile   # Compilar TypeScript
npm run lint      # Verificar estilo
```

---

## Estructura del proyecto

```
ADCP_multiagente/
├── backend/
│   ├── main.py                  # Servidor FastAPI con los 4 endpoints
│   ├── agents/
│   │   └── adcp_agents.py       # Agentes CrewAI por fase
│   ├── tests/
│   │   └── test_main.py         # Pruebas unitarias del backend
│   ├── requirements.txt
│   └── .env.example
│
└── vscode-extension/
    ├── src/
    │   ├── extension.ts         # Punto de entrada de la extensión
    │   ├── stateManager.ts      # Persistencia de estado por workspace
    │   ├── backendClient.ts     # Cliente HTTP hacia el backend
    │   ├── adcpPanel.ts         # Webview con resultados
    │   └── adcpTreeProvider.ts  # Árbol de fases en la barra lateral
    ├── media/
    │   └── adcp-icon.svg
    └── package.json
```

---

## Licencia

MIT — ver [LICENSE](LICENSE)
