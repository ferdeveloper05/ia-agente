from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Llamada al servidor del modelo (OllamaLLM)
llm = OllamaLLM(
    model="gpt-oss:20b", 
    base_url="http://10.90.20.12:11440",
    temperature=0.7
)

# Plantilla base para proporcionar informacion al modelo
prompt = PromptTemplate(
    input_variables=["question"], 
    template="Eres un experto en {question} responde con claridad",
)

# Enviar al chat y guardar en el historial la conversacion 
chat_prompt = ChatPromptTemplate([
    ("system", "Eres un asistente util responde con claridad"),
    MessagesPlaceholder(variable_name="historial"),
    ("human", "{question}")
])

historial = []

# Establece la cadena de conversacion
chain = chat_prompt | llm

def agente(question: str) -> str:
    global historial
    
    response = chain.invoke({"question": question, "historial":historial}) 
    
    historial.append(HumanMessage(content=question))
    historial.append(AIMessage(content=str(response)))   
    return response

