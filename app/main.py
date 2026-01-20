from fastapi import FastAPI,HTTPException       
from pydantic import BaseModel
from langchain_agent import agente
import requests


app = FastAPI()

@app.get('/', tags=['home'])
def say_hello():
    return "Hola Mundo"

class Query(BaseModel):
    question: str 


@app.get("/check-ollama")
def check_ollama():
    try:
        response = requests.get("http://10.90.20.12:11440/api/tags")
        return {"status": "Ollama activo", "modelos": response.json()}
    except Exception as e:
        return {"status": "Error de conexión", "detalle": str(e)}

@app.post("/ask")
def ask(query: Query):
    answer = agente(query.question)
    return {"response": answer}

# Funcion encargada de obtener la pregunta del usuario
@app.post("/pregunta", tags=['Pruebas'])
def pregunta(query: Query):
    respuesta = agente(query.question)
    return {"respuesta":respuesta}