from typing import List, Optional, Dict, Any
from datetime import datetime
from beanie import Document, Indexed
from pydantic import BaseModel, Field, EmailStr
from passlib.context import CryptContext

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserSettings(BaseModel):
    theme: str = "dark"
    max_context: int = 4096

class User(Document):
    nombre_usuario: str
    password: str
    email: Optional[EmailStr] = Field(None, index=True, unique=True, sparse=True)
    tipo_rol: str = "user"
    status: bool = True
    sessions: List[str] = []
    settings: UserSettings = UserSettings()
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "usuarios"

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

class Conversation(Document):
    usuario_id: Optional[str] = None
    session_id: str = Indexed()
    messages: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "conversaciones"

class UserRole(Document):
    nombre_rol: str = Indexed(unique=True)

    class Settings:
        name = "roles_usuarios"

# List of models to be initialized by Beanie
document_models = [User, Conversation, UserRole]
