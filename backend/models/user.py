from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import uuid4

class User(BaseModel):
    id: str
    email: str
    nome: str
    profissao: str
    marca_profile_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def create(cls, email: str, nome: str, profissao: str):
        return cls(
            id=str(uuid4()),
            email=email,
            nome=nome,
            profissao=profissao,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

class UserResponse(BaseModel):
    """Modelo de resposta para usuários"""
    id: str
    email: str
    nome: str
    profissao: str
    created_at: datetime
    
    class Config:
        from_attributes = True
