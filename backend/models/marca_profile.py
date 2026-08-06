from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from uuid import uuid4

class MarcaProfile(BaseModel):
    id: str
    user_id: str
    nome_marca: str
    cores_primarias: List[str]  # ["#8B7355", "#F5F1E8", "#5D4037"]
    fontes: Dict[str, str]      # {"titulo": "Cormorant Garamond", "texto": "Inter"}
    logo_url: Optional[str] = None
    estilo_preferido: str       # "minimalista", "elegante", "criativo"
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def create_default(cls, user_id: str, nome_marca: str):
        """Cria perfil padrão do Alma de Escrita"""
        return cls(
            id=str(uuid4()),
            user_id=user_id,
            nome_marca=nome_marca,
            cores_primarias=["#8B7355", "#F5F1E8", "#5D4037"],
            fontes={
                "titulo": "Cormorant Garamond",
                "texto": "Inter"
            },
            estilo_preferido="elegante",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

class MarcaProfileResponse(BaseModel):
    """Modelo de resposta para perfis de marca"""
    id: str
    nome_marca: str
    cores_primarias: List[str]
    fontes: Dict[str, str]
    estilo_preferido: str
    created_at: datetime
    
    class Config:
        from_attributes = True
