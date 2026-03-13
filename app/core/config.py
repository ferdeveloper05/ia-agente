from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "ia-agente"
    DEBUG: bool = False
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = "http://10.90.20.12:11440"
    MODEL_NAME: str = "llama3.1:8b"
    TEMPERATURE: float = 0.7
    
    # API Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
