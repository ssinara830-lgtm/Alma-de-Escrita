from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from config import Config
import uuid

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    nome = Column(String(255), nullable=False)
    profissao = Column(String(255), nullable=False)
    marca_profile_id = Column(String(36))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class MarcaProfileModel(Base):
    __tablename__ = "marca_profiles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    nome_marca = Column(String(255), nullable=False)
    cores_primarias = Column(JSON, nullable=False)
    fontes = Column(JSON, nullable=False)
    logo_url = Column(Text)
    estilo_preferido = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Database:
    def __init__(self):
        self.engine = None
        self.async_session = None
    
    async def init_db(self):
        """Inicializa o banco de dados e cria tabelas"""
        try:
            self.engine = create_async_engine(Config.DATABASE_URL, echo=True)
            self.async_session = sessionmaker(
                self.engine, class_=AsyncSession, expire_on_commit=False
            )
            
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                
            print("✅ Banco de dados inicializado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao inicializar banco de dados: {e}")
            return False

# Instância global do banco de dados
database = Database()
