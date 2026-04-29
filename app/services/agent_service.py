from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.prebuilt import create_react_agent
from typing import List, Dict
from core.config import settings
import re
from tools.ven_hour_tool import get_current_time_ven
from tools.web_browser import duckduckgo_browser
from tools.predict_date_tool import calculate_future_date_ven


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
    get_current_time_ven,
    calculate_future_date_ven,
    duckduckgo_browser
]

def agente_executor(session_id: str, question: str) -> str:
    llm = get_llm()
    historial = get_session_history(session_id)
    
    system_prompt = (
        "Eres un asistente inteligente que usa herramientas cuando es necesario. Responde siempre en español.\n"
        "Si necesitas predecir fecha usa la herramienta predict_date_tool con la funcion calculate_future_date_ven.\n"
        "Si necesitas buscar información externa o las herramientas específicas fallan, usa 'web_browser'.\n"
        "IMPORTANTE: Proporciona ÚNICAMENTE la respuesta contextual al usuario final. "
        "NO incluyas tu razonamiento previo, bloques XML de <think>...</think>, ni la palabra 'Thought:' solo incluye la respuesta final al usuario."
        
    )
    
    # Agregar el nuevo mensaje del usuario
    historial.append(HumanMessage(content=question))
    
    # Crear el agente usando LangGraph
    agent = create_react_agent(llm, tools, prompt=system_prompt)
    
    # Ejecutar el agente
    result = agent.invoke({"messages": historial})
    
    # Extraer la respuesta (último mensaje del agente)
    answer = result["messages"][-1].content
    
    # Limpiar la respuesta de bloques de pensamiento o razonamiento
    answer = re.sub(r'<think>.*?</think>', '', answer, flags=re.DOTALL).strip()
    
    # Actualizar la memoria con todos los mensajes devueltos por el agente (incluyendo llamadas a herramientas)
    sesiones[session_id] = result["messages"]
    
    return answer
