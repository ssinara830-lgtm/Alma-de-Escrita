from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.biblioteca_pessoal import BibliotecaPessoal
from services.curadoria_escritora import CuradoriaEscritora
import aiofiles
import os
from datetime import datetime

router = APIRouter(prefix="/api/escritora", tags=["Escritora"])

# Instâncias globais
biblioteca = BibliotecaPessoal()
curadoria = CuradoriaEscritora()

@router.post("/carregar-livro")
async def carregar_livro_escritora(
    file: UploadFile = File(...),
    titulo_livro: str = Form(...),
    sinopse: str = Form("")
):
    """Carrega um livro PDF para a biblioteca pessoal"""
    
    try:
        # Cria diretório de uploads se não existir
        os.makedirs("../../frontend/uploads", exist_ok=True)
        
        # Salva o arquivo
        file_path = f"../../frontend/uploads/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Processa o livro
        resultado = await biblioteca.carregar_livro_escritora(file_path, titulo_livro, sinopse)
        
        return {
            "success": True,
            "message": f"Livro '{titulo_livro}' carregado com sucesso!",
            "dados": resultado
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar livro: {str(e)}")

@router.get("/biblioteca")
async def get_biblioteca_completa():
    """Retorna toda a biblioteca da escritora"""
    try:
        biblioteca_completa = await biblioteca.get_biblioteca_completa()
        estatisticas = await biblioteca.get_estatisticas_biblioteca()
        
        return {
            "biblioteca": biblioteca_completa,
            "estatisticas": estatisticas
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar biblioteca: {str(e)}")

@router.get("/trechos-aleatorios")
async def get_trechos_aleatorios(quantidade: int = 5):
    """Retorna trechos aleatórios da biblioteca"""
    try:
        trechos = await biblioteca.get_trechos_aleatorios(quantidade)
        return {"trechos": trechos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar trechos: {str(e)}")

@router.get("/buscar-trechos")
async def buscar_trechos_por_tema(tema: str):
    """Busca trechos por tema específico"""
    try:
        trechos = await biblioteca.buscar_trechos_por_tema(tema)
        return {
            "tema_busca": tema,
            "total_encontrado": len(trechos),
            "trechos": trechos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca: {str(e)}")

@router.post("/plano-mensal")
async def criar_plano_mensal(mes: str = None):
    """Cria plano de conteúdo mensal"""
    try:
        biblioteca_completa = await biblioteca.get_biblioteca_completa()
        
        # Cria perfil padrão
        from models.marca_profile import MarcaProfile
        profile_temporario = MarcaProfile.create_default("escritora", "Minha Marca")
        
        plano = await curadoria.criar_plano_mensal_escritora(
            biblioteca_completa, 
            profile_temporario, 
            mes
        )
        
        return {
            "success": True,
            "plano_mensal": plano
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar plano: {str(e)}")

@router.delete("/remover-livro/{titulo_livro}")
async def remover_livro_biblioteca(titulo_livro: str):
    """Remove um livro da biblioteca"""
    try:
        sucesso = await biblioteca.remover_livro(titulo_livro)
        
        if sucesso:
            return {"success": True, "message": f"Livro '{titulo_livro}' removido"}
        else:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover livro: {str(e)}")
