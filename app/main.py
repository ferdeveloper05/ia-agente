from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import requests
from api.endpoints import router as agent_router
from core.config import settings
from core.database import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB
    await init_db()
    yield
    # Shutdown: Clean up if needed

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# CORS — permitir al frontend React comunicarse con el backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas modulares
app.include_router(agent_router, prefix="/api/v1")

@app.get('/', tags=['home'])
def say_hello():
    return {"message": f"Bienvenido a {settings.PROJECT_NAME}"}

@app.get("/check-ollama", status_code=status.HTTP_200_OK)
def check_ollama():
    try:
        # Usar la URL de la configuración
        response = requests.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
        return {"status": "Ollama activo", "modelos": response.json()}
    except Exception as e:
        return {"status": "Error de conexión", "detalle": str(e)}