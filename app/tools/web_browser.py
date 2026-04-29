from ddgs import DDGS
from langchain_core.tools import tool

@tool
def duckduckgo_browser(query: str) -> str:
    """Busca información en internet para datos actuales, noticias y eventos, he indica al usuario que estas buscando por navegador."""
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)
            if not results:
                return "No se encontraron resultados en DuckDuckGo."
            return "\n\n".join([f"{r['title']}: {r['body']}" for r in results])
    except Exception as e:
        return f"Error al buscar en DuckDuckGo: {str(e)}"
