from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate

llm = OllamaLLM(
    model="gpt-oss:20b", 
    base_url="http://10.50.95.144:11440",
    temperature=0.7
)

prompt = PromptTemplate(
    input_variables=["tema"], 
    template="Eres un experto en responde temas sobre soporte tecnico con claridad"
)

chain = prompt | llm

def agente(question: str) -> str:
    return chain.invoke({"question": question})