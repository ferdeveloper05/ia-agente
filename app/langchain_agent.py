from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate

llm = OllamaLLM(
    model="gpt-oss:20b", 
    base_url="http://10.50.95.140:11440",
    temperature=0.7
)

prompt = PromptTemplate(
    input_variables=["tema"], 
    template="Eres un experto en {{tema}} responde con claridad"
)

chain = prompt | llm

def agente(question: str) -> str:
    return chain.invoke({"question": question})