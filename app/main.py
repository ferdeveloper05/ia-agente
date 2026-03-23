from fastapi import FastAPI, status

import requests
from api.endpoints import router as agent_router
from core.config import settings


app = FastAPI(title=settings.PROJECT_NAME)


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
