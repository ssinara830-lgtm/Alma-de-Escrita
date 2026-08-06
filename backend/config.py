import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    APP_ENV = os.getenv("APP_ENV", "development")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./almadeescrita.db")
    
    # Configurações padrão do Alma de Escrita
    CORES_PADRAO = ["#8B7355", "#F5F1E8", "#5D4037"]
    FONTES_PADRAO = {
        "titulo": "Cormorant Garamond", 
        "texto": "Inter"
    }
    
    @classmethod
    def validate_config(cls):
        """Valida se todas as configurações necessárias estão presentes"""
        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY == "sua_chave_aqui":
            print("⚠️  AVISO: OPENAI_API_KEY não configurada. Configure no arquivo .env")
            return False
        return True
