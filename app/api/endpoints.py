from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from services.agent_service import agente_executor
import re
import dns.resolver
from models.schemas import User, Conversation
from datetime import datetime

router = APIRouter()

class Query(BaseModel):
    session_id: str
    question: str

class EmailValidation(BaseModel):
    email: EmailStr
    name: str

@router.post("/ask")
async def ask(query: Query):
    try:
        # Get the answer from the agent
        answer = agente_executor(query.session_id, query.question)
        
        # Save to database
        # Find or create conversation for this session
        conversation = await Conversation.find_one(Conversation.session_id == query.session_id)
        if not conversation:
            conversation = Conversation(session_id=query.session_id, messages=[])
        
        # Append new messages
        conversation.messages.append({"role": "user", "content": query.question, "timestamp": datetime.utcnow().isoformat()})
        conversation.messages.append({"role": "assistant", "content": answer, "timestamp": datetime.utcnow().isoformat()})
        
        await conversation.save()
        
        return {"response": answer, "session_id": query.session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate-email")
async def validate_email(payload: EmailValidation):
    email = payload.email.strip().lower()
    name = payload.name.strip()

    if not name or len(name) < 2:
        raise HTTPException(status_code=400, detail="El nombre debe tener al menos 2 caracteres.")

    # Domain verification
    domain = email.split("@")[1]
    try:
        mx_records = dns.resolver.resolve(domain, "MX")
        if not mx_records:
            raise HTTPException(status_code=400, detail=f"El dominio '{domain}' no parece aceptar correos.")
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        raise HTTPException(status_code=400, detail=f"El dominio '{domain}' no es válido o no recibe correos.")
    except Exception:
        raise HTTPException(status_code=400, detail=f"No se pudo verificar el dominio '{domain}'.")

    # Persist user in MongoDB
    user = await User.find_one(User.email == email)
    if not user:
        # Create new user if not exists
        # Note: In a real app, we'd handle password creation here or via a separate register step
        # For now, we follow the requested structure and store the name
        user = User(
            nombre_usuario=name,
            email=email,
            password=User.get_password_hash("default_password") # Fallback password
        )
        await user.create()
    else:
        # Update name if it changed
        user.nombre_usuario = name
        user.updated_at = datetime.utcnow()
        await user.save()

    return {"valid": True, "email": email, "name": name, "user_id": str(user.id)}

