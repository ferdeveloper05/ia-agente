from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

llm = OllamaLLM(
    model="gpt-oss:20b", 
    base_url="http://10.50.95.144:11440",
    temperature=0.7
)

prompt = PromptTemplate(
    input_variables=["question"], 
    template="Eres un experto en {question} responde con claridad",
)

chat_prompt = ChatPromptTemplate([
    ("system", "Eres un asistente util responde con claridad"),
    MessagesPlaceholder(variable_name="historial"),
    ("human", "{question}")
])

historial = []

chain = chat_prompt | llm

def agente(question: str) -> str:
    global historial
    #if historial is None: 
        #historial = [] 
    response = chain.invoke({"question": question, "historial":historial}) 
    
    historial.append(HumanMessage(content=question))
    historial.append(AIMessage(content=str(response)))   
    return response

