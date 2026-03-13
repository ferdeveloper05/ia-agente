from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
from typing import List, Dict
from core.config import settings
from tools.custom_tools import get_current_datetime

# Diccionario para persistencia en memoria (TEMPORAL)
sesiones: Dict[str, List[BaseMessage]] = {}

def get_llm():
    return ChatOllama(
        model=settings.MODEL_NAME, 
        base_url=settings.OLLAMA_BASE_URL,
        temperature=settings.TEMPERATURE
    )

def get_session_history(session_id: str) -> List[BaseMessage]:
    if session_id not in sesiones:
        sesiones[session_id] = []
    return sesiones[session_id]

# Definición de herramientas
tools = [
    DuckDuckGoSearchRun(name="duckduckgo_search", description="Busca información en internet para datos actuales."),
    get_current_datetime
]

def agente_executor(session_id: str, question: str) -> str:
    llm = get_llm()
    historial = get_session_history(session_id)
    
    system_prompt = (
        "Eres un asistente inteligente que usa herramientas cuando es necesario. Responde siempre en español. "
        "Si necesitas saber la hora y falla la herramienta de fecha/hora, o si se te pide buscar un mapa de zonas horarias, "
        "USA inmediatamente la herramienta duckduckgo_search (ej: 'timezonemap venezuela')."
    )
    
    # Agregar el nuevo mensaje del usuario
    historial.append(HumanMessage(content=question))
    
    # Crear el agente usando LangGraph
    agent = create_react_agent(llm, tools, prompt=system_prompt)
    
    # Ejecutar el agente
    result = agent.invoke({"messages": historial})
    
    # Extraer la respuesta (último mensaje del agente)
    answer = result["messages"][-1].content
    
    # Actualizar la memoria con todos los mensajes devueltos por el agente (incluyendo llamadas a herramientas)
    sesiones[session_id] = result["messages"]
    
    return answer
