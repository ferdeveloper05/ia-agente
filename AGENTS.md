# AGENTS.md — IA Agente (Sirpef Chatbot AI)

> Sistema de chatbot inteligente con agente LangGraph + Ollama, persistencia MongoDB, y doble frontend (Streamlit + React).

---

## Tabla de Contenidos

- [Arquitectura General](#arquitectura-general)
- [Stack Tecnológico](#stack-tecnológico)
- [Servicios Docker](#servicios-docker)
- [Backend (FastAPI)](#backend-fastapi)
  - [Estructura de Archivos](#estructura-de-archivos-backend)
  - [Configuración](#configuración)
  - [Base de Datos (MongoDB)](#base-de-datos-mongodb)
  - [Modelos de Datos](#modelos-de-datos)
  - [API Endpoints](#api-endpoints)
  - [Servicio del Agente](#servicio-del-agente)
  - [Herramientas Personalizadas (Tools)](#herramientas-personalizadas-tools)
- [Frontend Streamlit](#frontend-streamlit)
- [Frontend React (Vite)](#frontend-react-vite)
- [Reglas del Agente (Críticas)](#reglas-del-agente-críticas)
- [Comandos de Ejecución](#comandos-de-ejecución)
- [Variables de Entorno](#variables-de-entorno)
- [Dependencias](#dependencias)

---

## Arquitectura General

```
┌──────────────────────┐     ┌──────────────────────┐
│  Frontend Streamlit  │     │   Frontend React     │
│  (Puerto 8501)       │     │   (Puerto 5173)      │
└─────────┬────────────┘     └──────────┬───────────┘
          │ HTTP                        │ HTTP
          │ http://app:8000             │ http://localhost:8000
          ▼                             ▼
┌─────────────────────────────────────────────────────┐
│              Backend FastAPI (Puerto 8000)           │
│  ┌──────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │  Endpoints   │  │ Agent Svc   │  │   Tools    │ │
│  │  /api/v1/*   │  │ LangGraph   │  │  Hora VEN  │ │
│  │              │  │ ReAct Agent │  │  Fecha     │ │
│  └──────┬───────┘  └──────┬──────┘  │  DuckDuck  │ │
│         │                 │         └────────────┘ │
└─────────┼─────────────────┼────────────────────────┘
          │                 │
          ▼                 ▼
┌──────────────────┐  ┌──────────────────┐
│  MongoDB Atlas   │  │    Ollama LLM    │
│  (Puerto 27017)  │  │  (Puerto 11434)  │
│  agent_ia_db     │  │  llama3.1:8b     │
└──────────────────┘  └──────────────────┘
```

**Networking:** Todos los servicios se comunican a través de la red Docker `agent_network` (bridge). El frontend Streamlit llama al backend vía `http://app:8000` (nombre de servicio Docker). El frontend React llama vía `http://localhost:8000` (desde el navegador del usuario).

---

## Stack Tecnológico

| Capa          | Tecnología                                     |
|---------------|-------------------------------------------------|
| **LLM**       | Ollama (`llama3.1:8b`) — modelo local           |
| **Agente**    | LangGraph (`create_react_agent`) + LangChain    |
| **Backend**   | FastAPI + Uvicorn (Python 3.11)                  |
| **Base de Datos** | MongoDB Atlas Local (Beanie ODM + Motor)     |
| **Frontend 1** | Streamlit (dashboard estilo chat)               |
| **Frontend 2** | React 18 + Vite 5 (SPA moderna)                |
| **Contenedores** | Docker Compose (4 servicios)                  |

---

## Servicios Docker

Definidos en `docker-compose.yml`:

| Servicio            | Imagen / Build       | Container Name                | Puerto Externo | Puerto Interno |
|---------------------|----------------------|-------------------------------|----------------|----------------|
| `app`               | `./app` (build)      | `langchain-ollama`            | `8000`         | `8000`         |
| `ollama`            | `ollama/ollama:0.20.7` | `ollama`                    | `11440`        | `11434`        |
| `agent_mongodb`     | `mongodb/mongodb-atlas-local` | `agent_mongodb_container` | `27017`    | `27017`        |
| `frontend_streamlit`| `./streamlit_app`    | `intelligent_agent_dashboard` | `8501`         | `8501`         |
| `frontend_react`    | `./react_app`        | `intelligent_agent_react_ui`  | `5173`         | `5173`         |

**Volúmenes persistentes:** `ollama_data`, `db`, `configdb`, `mongot`, `streamlit_data_v1`

**Dependencias:** Ambos frontends dependen de `app` y `agent_mongodb`. El backend depende de `ollama` y `agent_mongodb`.

---

## Backend (FastAPI)

### Estructura de Archivos (Backend)

```
app/
├── main.py                  # Entry point FastAPI, CORS, lifespan (init DB)
├── Dockerfile               # Python 3.11-bullseye, uvicorn con --reload
├── requirements.txt         # Dependencias Python
├── api/
│   └── endpoints.py         # Rutas REST: /ask, /validate-email
├── core/
│   ├── config.py            # Settings con pydantic-settings (.env)
│   └── database.py          # Inicialización MongoDB con Beanie/Motor
├── models/
│   └── schemas.py           # Documentos Beanie: User, Conversation, UserRole
├── services/
│   └── agent_service.py     # Lógica del agente LangGraph ReAct
└── tools/
    ├── custom_tools.py      # Tool genérico de fecha/hora (no usado activamente)
    ├── ven_hour_tool.py     # Hora actual de Venezuela (UTC-4)
    ├── predict_date_tool.py # Cálculo de fechas futuras/pasadas (relativedelta)
    └── web_browser.py       # Búsqueda en DuckDuckGo
```

### Configuración

Archivo: `app/core/config.py` — Usa `pydantic-settings` con soporte para `.env`.

| Variable          | Default                                          | Descripción                          |
|-------------------|--------------------------------------------------|--------------------------------------|
| `PROJECT_NAME`    | `ia-agente`                                      | Nombre del proyecto                  |
| `DEBUG`           | `False`                                          | Modo debug                           |
| `OLLAMA_BASE_URL` | `http://ollama:11434`                            | URL interna de Ollama (Docker)       |
| `MODEL_NAME`      | `llama3.1:8b`                                    | Modelo LLM a utilizar                |
| `TEMPERATURE`     | `0.7`                                            | Temperatura de generación            |
| `HOST`            | `0.0.0.0`                                        | Host del servidor                    |
| `PORT`            | `8000`                                           | Puerto del servidor                  |
| `MONGODB_URL`     | `mongodb://agent_mongodb:27017/?directConnection=true` | URL de MongoDB (Docker)        |
| `DATABASE_NAME`   | `agent_ia_db`                                    | Nombre de la base de datos           |

### Base de Datos (MongoDB)

- **Motor:** Motor (async driver para MongoDB)
- **ODM:** Beanie (Object Document Mapper)
- **Inicialización:** Al arrancar FastAPI vía `lifespan`, se llama `init_db()` que:
  1. Crea el cliente Motor
  2. Inicializa Beanie con los modelos de documentos
  3. Crea roles por defecto (`admin`, `user`) si no existen

### Modelos de Datos

Archivo: `app/models/schemas.py`

#### `User` (colección: `usuarios`)
| Campo             | Tipo              | Descripción                              |
|-------------------|-------------------|------------------------------------------|
| `nombre_usuario`  | `str`             | Nombre del usuario                       |
| `password`        | `str`             | Hash bcrypt de la contraseña             |
| `email`           | `EmailStr` (opt)  | Email único, indexado, sparse            |
| `tipo_rol`        | `str`             | Rol del usuario (default: `"user"`)      |
| `status`          | `bool`            | Activo/inactivo (default: `True`)        |
| `sessions`        | `List[str]`       | IDs de sesiones del usuario              |
| `settings`        | `UserSettings`    | Preferencias: `theme` y `max_context`    |
| `created_at`      | `datetime`        | Fecha de creación                        |
| `updated_at`      | `datetime`        | Última actualización                     |

**Métodos:** `verify_password()`, `get_password_hash()` (bcrypt vía passlib)

#### `Conversation` (colección: `conversaciones`)
| Campo         | Tipo                | Descripción                       |
|---------------|---------------------|-----------------------------------|
| `usuario_id`  | `str` (opt)         | ID del usuario (opcional)         |
| `session_id`  | `str` (indexado)    | Identificador de sesión           |
| `messages`    | `List[Dict]`        | Lista de mensajes (role, content, timestamp) |
| `metadata`    | `Dict`              | Metadata adicional                |
| `created_at`  | `datetime`          | Fecha de creación                 |

#### `UserRole` (colección: `roles_usuarios`)
| Campo         | Tipo     | Descripción                       |
|---------------|----------|-----------------------------------|
| `nombre_rol`  | `str`    | Nombre del rol (único, indexado)  |

### API Endpoints

Prefijo base: `/api/v1`

#### `POST /api/v1/ask`
Envía una pregunta al agente IA.

**Request Body:**
```json
{
  "session_id": "uuid-string",
  "question": "¿Qué hora es en Venezuela?"
}
```

**Response:**
```json
{
  "response": "Son las 3:19 PM en Venezuela.",
  "session_id": "uuid-string"
}
```

**Flujo interno:**
1. Ejecuta `agente_executor(session_id, question)`
2. Busca/crea la conversación en MongoDB por `session_id`
3. Guarda mensajes de usuario y asistente con timestamps
4. Retorna la respuesta del agente

#### `POST /api/v1/validate-email`
Valida y registra un email de usuario.

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "Nombre del Usuario"
}
```

**Validaciones:**
- Nombre: mínimo 2 caracteres
- Email: formato válido (Pydantic `EmailStr`)
- Dominio: verificación de registros MX vía `dnspython`

**Flujo:** Crea o actualiza el usuario en MongoDB.

#### `GET /`
Endpoint de bienvenida. Retorna `{"message": "Bienvenido a ia-agente"}`.

#### `GET /check-ollama`
Verifica conectividad con Ollama. Retorna estado y modelos disponibles.

### CORS

Orígenes permitidos: `http://localhost:5173`, `http://127.0.0.1:5173` (frontend React).

### Servicio del Agente

Archivo: `app/services/agent_service.py`

**Componentes:**
- **LLM:** `ChatOllama` configurado con modelo, URL base y temperatura desde settings
- **Framework:** LangGraph `create_react_agent` (patrón ReAct: Reasoning + Acting)
- **Memoria:** Diccionario en memoria `sesiones: Dict[str, List[BaseMessage]]` (temporal, por sesión)

**Herramientas registradas:**
1. `get_current_time_ven` — Hora actual de Venezuela
2. `calculate_future_date_ven` — Cálculo de fechas
3. `duckduckgo_browser` — Búsqueda web

**System Prompt:**
```
Eres un asistente inteligente que usa herramientas cuando es necesario. Responde siempre en español.
Si necesitas predecir fecha usa la herramienta predict_date_tool con la función calculate_future_date_ven.
Si necesitas buscar información externa o las herramientas específicas fallan, usa 'web_browser'.
IMPORTANTE: Proporciona ÚNICAMENTE la respuesta contextual al usuario final.
NO incluyas tu razonamiento previo, bloques XML de <think>...</think>, ni la palabra 'Thought:'
```

**Post-procesamiento:** Limpia bloques `<think>...</think>` de la respuesta con regex.

### Herramientas Personalizadas (Tools)

Todas las herramientas usan el decorador `@tool` de LangChain.

#### `get_current_time_ven` → `ven_hour_tool.py`
- **Sin parámetros** requeridos
- Calcula hora de Venezuela manualmente: `UTC - 4 horas`
- Retorna `dict` con:
  - `datetime`: objeto datetime con timezone
  - `info_hoy`: texto formateado ("Lunes, 27 de abril del 2026\nHora: 03:19:44 PM\nZona: UTC-4")
- Formato de hora: **12 horas** (AM/PM) vía `%I:%M:%S %p`
- Días y meses en **español**

#### `calculate_future_date_ven` → `predict_date_tool.py`
- **Parámetros:** `years`, `months`, `weeks`, `days` (todos `int`, default `0`)
- Usa `dateutil.relativedelta` para cálculos precisos con meses/años
- Invoca internamente `get_current_time_ven` para obtener la fecha actual
- Indica si la fecha resultado es **futuro**, **pasado** o **presente (hoy)**
- Ejemplo de uso: "¿Qué día será en 3 meses y 2 semanas?" → `months=3, weeks=2`

#### `duckduckgo_browser` → `web_browser.py`
- **Parámetro:** `query: str`
- Usa la librería `ddgs` para buscar en DuckDuckGo
- Retorna los **5 primeros resultados** formateados (`título: descripción`)
- Fallback cuando las herramientas específicas fallan

#### `get_current_datetime` → `custom_tools.py` (no activo en el agente)
- Tool genérico de fecha/hora con timezone configurable (IANA)
- Incluye lógica de fallback: si falla, instruye al agente a buscar la hora por web
- **No está registrado** en la lista de herramientas del agente actual

---

## Frontend Streamlit

**Puerto:** `8501` | **Container:** `intelligent_agent_dashboard`

### Estructura

```
streamlit_app/
├── app.py                    # Entry point, configuración de página y CSS
├── Dockerfile                # Python 3.11-slim, healthcheck incluido
├── requirements.txt          # streamlit, pymongo, requests, pandas
├── .streamlit/
│   └── config.toml           # Tema dark mode personalizado
├── components/
│   ├── chat_area.py          # Área de chat con streaming al backend
│   └── sidebar.py            # Sidebar con historial, nueva conversación, email
├── utils/
│   └── session.py            # Gestión de sesiones/conversaciones en memoria
├── assets/                   # Logos e imágenes
└── data/                     # Datos persistidos (volumen Docker)
```

### Características

- **Tema oscuro** personalizado (config.toml + CSS overrides)
- **Gestión de conversaciones:** Crear, cambiar, eliminar conversaciones
- **Título automático:** Se genera del primer mensaje del usuario (primeros 20 caracteres)
- **Conexión email:** Modal para vincular correo electrónico (simulado)
- **API URL:** Configurable vía `API_URL` env var, default `http://app:8000/api/v1/ask`
- **Timeout:** 120 segundos por request al backend

### Paleta de Colores (config.toml)

| Elemento          | Color      |
|-------------------|------------|
| Primary           | `#2563EB`  |
| Background        | `#0E1117`  |
| Secondary BG      | `#1E293B`  |
| Text              | `#FAFAFA`  |

---

## Frontend React (Vite)

**Puerto:** `5173` | **Container:** `intelligent_agent_react_ui`

### Estructura

```
react_app/
├── index.html               # HTML shell
├── Dockerfile               # Node 20 Alpine, npm run dev
├── package.json             # React 18, Vite 5
├── vite.config.js           # host: true para Docker
└── src/
    ├── main.jsx             # Entry point React
    ├── App.jsx              # Componente principal, estado global
    ├── index.css            # Estilos globales (dark theme completo)
    ├── components/
    │   ├── ChatArea.jsx     # Área de chat, envío de mensajes al backend
    │   ├── Sidebar.jsx      # Sidebar con historial, búsqueda, kebab menu
    │   ├── EmailModal.jsx   # Modal de registro/validación de email
    │   └── SettingsModal.jsx # Modal de configuración (tema, idioma, gestión chats)
    └── utils/
        └── oauth.js         # Utilidades OAuth2 (Google PKCE, preparado)
```

### Características

- **SPA moderna** con React 18 + Vite (HMR)
- **Dark mode completo** con CSS vanilla
- **Gestión de conversaciones:** Crear, renombrar (inline edit), eliminar con confirmación
- **Sidebar colapsable:** Vista compacta con íconos SVG (estilo ChatGPT)
- **Modal de Email:** Validación frontend + backend (verifica registros MX del dominio)
- **Modal de Configuración:** Pestañas (General, Chats, Account) — tema, idioma, importar/exportar/eliminar chats
- **Persistencia de usuario:** `localStorage` para nombre de usuario
- **OAuth2 preparado:** Utilidades PKCE para Google Auth (no activo aún)
- **Auto-scroll:** Los mensajes hacen scroll automático al último mensaje
- **Indicador de escritura:** "Escribiendo..." mientras el backend procesa
- **API directa:** Llama a `http://localhost:8000/api/v1/ask` desde el navegador

### Prevención de duplicados

Al crear nueva conversación, verifica si ya existe una conversación vacía y la reutiliza en lugar de crear otra.

---

## Reglas del Agente (Críticas)

Definidas en `app/services/agent_service.py:40-47`:

1. **Siempre responder en español**
2. **Consultas de fecha/hora:** DEBE llamar a `get_current_time_ven` PRIMERO, luego calcular con `calculate_future_date_ven`
3. **Búsqueda web:** Usar `duckduckgo_browser` como fallback cuando las herramientas específicas fallan
4. **Salida limpia:** Eliminar bloques `<think>...</think>` de la respuesta final (regex post-procesamiento)
5. **Sin razonamiento visible:** NO incluir "Thought:", bloques XML, ni razonamiento previo en la respuesta al usuario
6. **Solo respuesta final:** Proporcionar ÚNICAMENTE la respuesta contextual al usuario

---

## Comandos de Ejecución

```bash
# Build y arrancar todos los servicios
docker-compose up --build

# Arranque rápido (sin rebuild)
docker-compose up

# Detener todos los servicios
docker-compose down

# Ver logs en tiempo real
docker-compose logs -f

# Rebuild solo un servicio
docker-compose up --build app
docker-compose up --build frontend_react
```

### URLs de Acceso

| Servicio          | URL                          |
|-------------------|------------------------------|
| **Backend API**   | http://localhost:8000        |
| **API Docs**      | http://localhost:8000/docs   |
| **Streamlit**     | http://localhost:8501        |
| **React**         | http://localhost:5173        |
| **Ollama API**    | http://localhost:11440       |
| **Check Ollama**  | http://localhost:8000/check-ollama |

### Testing de Componentes Individuales

```bash
# Backend solamente
cd app && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend Streamlit solamente
cd streamlit_app && streamlit run app.py

# Frontend React solamente
cd react_app && npm run dev
```

---

## Variables de Entorno

Crear archivo `.env` en la raíz de `app/` para sobrescribir valores:

```env
OLLAMA_BASE_URL=http://ollama:11434
MODEL_NAME=llama3.1:8b
TEMPERATURE=0.7
MONGODB_URL=mongodb://agent_mongodb:27017/?directConnection=true
DATABASE_NAME=agent_ia_db
DEBUG=False
```

Frontend React (opcional):
```env
VITE_GOOGLE_CLIENT_ID=tu-client-id-de-google
```

---

## Dependencias

### Backend (`app/requirements.txt`)

| Paquete               | Versión      | Propósito                          |
|-----------------------|--------------|------------------------------------|
| `langchain`           | ≥1.1.0       | Framework de agentes LLM           |
| `langchain-core`      | ≥1.1.3       | Core de LangChain                  |
| `langchain-ollama`    | ≥1.0.0       | Integración con Ollama             |
| `langchain-chroma`    | ≥1.1.0       | Vector store (preparado)           |
| `langchain-community` | ≥0.4.1       | Herramientas comunitarias          |
| `langgraph`           | ≥1.1.0       | Grafos de agentes (ReAct)          |
| `fastapi`             | 0.122.0      | Framework web                      |
| `uvicorn`             | 0.38.0       | Servidor ASGI                      |
| `beanie`              | 1.27.0       | ODM para MongoDB                   |
| `motor`               | 3.3.2        | Driver async MongoDB               |
| `pymongo`             | 4.6.1        | Driver sync MongoDB                |
| `ddgs`                | 9.11.3       | DuckDuckGo search                  |
| `duckduckgo-search`   | ≥6.0.0       | Búsqueda DuckDuckGo                |
| `dnspython`           | 2.7.0        | Verificación DNS/MX de emails      |
| `email-validator`     | ≥2.1.0       | Validación de emails               |
| `passlib[bcrypt]`     | ≥1.7.4       | Hash de contraseñas                |
| `pydantic-settings`   | ≥2.4.0       | Configuración tipada               |
| `requests`            | 2.32.5       | HTTP client                        |
| `python-dotenv`       | 1.2.1        | Variables de entorno                |

### Frontend Streamlit (`streamlit_app/requirements.txt`)

| Paquete      | Versión         | Propósito              |
|--------------|-----------------|------------------------|
| `streamlit`  | 1.55.0          | Framework dashboard    |
| `pymongo`    | 4.16.0          | Acceso a MongoDB       |
| `requests`   | 2.32.5          | HTTP client            |
| `pandas`     | ≥2.0.0, <3.0.0  | Manipulación de datos  |

### Frontend React (`react_app/package.json`)

| Paquete              | Versión  | Propósito             |
|----------------------|----------|-----------------------|
| `react`              | ^18.2.0  | UI library            |
| `react-dom`          | ^18.2.0  | DOM rendering         |
| `vite`               | ^5.2.0   | Bundler + dev server  |
| `@vitejs/plugin-react` | ^4.2.1 | Plugin React para Vite |