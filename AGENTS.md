# AGENTS.md - IA Agente

## Run Commands

```bash
docker-compose up --build    # Build and start all services
docker-compose up         # Fast Start
docker-compose down       # Stop all services
```

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:8501
- **Ollama API**: http://localhost:11445 (internal: 11434)

## Architecture

- **app/** - FastAPI backend (LangChain/LangGraph + Ollama)
- **streamlit_app/** - Streamlit frontend dashboard
- Container networking: frontend calls `http://app:8000` (not localhost)

## Agent Rules (Critical)

From `app/services/agent_service.py:40-49`:

1. **Always respond in Spanish**
2. **Date/time queries**: MUST call `get_current_time_ven` FIRST, then calculate, then `calculate_future_date_ven`
3. **Clean output**: Strip `<think>` blocks from final response
4. **No reasoning trace**: Don't include "Thought:" or XML blocks in user output

## Custom Tools

Located in `app/tools/`:
- `ven_hour_tool.py` - Venezuelan timezone (UTC-4)
- `predict_date_tool.py` - Date calculation
- `web_browser.py` - DuckDuckGo search

## Config

Edit `app/core/config.py` or set `.env`:
- `OLLAMA_BASE_URL`: Ollama service URL
- `MODEL_NAME`: Default `llama3.1:8b`
- `TEMPERATURE`: Default `0.7`

## Testing Single Component

```bash
# Test backend only
cd app && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Test frontend only
cd streamlit_app && streamlit run app.py
```