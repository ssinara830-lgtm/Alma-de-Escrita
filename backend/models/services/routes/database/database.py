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
    cores_primarias = Column(JSON, nullable=False)  # Lista de cores em JSON
    fontes = Column(JSON, nullable=False)          # Dicionário de fontes em JSON
    logo_url = Column(Text)
    estilo_preferido = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class BibliotecaModel(Base):
    __tablename__ = "biblioteca_pessoal"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    titulo_livro = Column(String(255), nullable=False)
    sinopse = Column(Text)
    arquivo_path = Column(Text, nullable=False)
    metadados = Column(JSON)  # Metadados extraídos em JSON
    analise_ia = Column(JSON) # Análise da IA em JSON
    status = Column(String(50), default="processando")
    created_at = Column(DateTime, default=func.now())

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
    
    async def get_session(self) -> AsyncSession:
        """Retorna uma sessão de banco de dados"""
        if not self.async_session:
            await self.init_db()
        return self.async_session()
    
    async def save_user(self, user_data: dict):
        """Salva um usuário no banco de dados"""
        async with await self.get_session() as session:
            user = UserModel(**user_data)
            session.add(user)
            await session.commit()
            return user
    
    async def get_user(self, user_id: str):
        """Busca um usuário por ID"""
        async with await self.get_session() as session:
            user = await session.get(UserModel, user_id)
            return user
    
    async def save_marca_profile(self, profile_data: dict):
        """Salva um perfil de marca no banco"""
        async with await self.get_session() as session:
            profile = MarcaProfileModel(**profile_data)
            session.add(profile)
            await session.commit()
            return profile
    
    async def get_marca_profile(self, user_id: str):
        """Busca perfil de marca por user_id"""
        async with await self.get_session() as session:
            from sqlalchemy import select
            result = await session.execute(
                select(MarcaProfileModel).where(MarcaProfileModel.user_id == user_id)
            )
            return result.scalar_one_or_none()
    
    async def save_livro_biblioteca(self, livro_data: dict):
        """Salva um livro na biblioteca pessoal"""
        async with await self.get_session() as session:
            livro = BibliotecaModel(**livro_data)
            session.add(livro)
            await session.commit()
            return livro
    
    async def get_biblioteca_user(self, user_id: str):
        """Busca todos os livros de um usuário"""
        async with await self.get_session() as session:
            from sqlalchemy import select
            result = await session.execute(
                select(BibliotecaModel).where(BibliotecaModel.user_id == user_id)
            )
            return result.scalars().all()

# Instância global do banco de dados
database = Database()

