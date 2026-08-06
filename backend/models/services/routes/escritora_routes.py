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
            "dados": {
                "titulo": resultado["titulo"],
                "metadados": resultado["metadados"],
                "total_trechos": len(resultado["trechos_extraidos"]),
                "temas_principais": resultado["analise"]["temas_principais"]
            }
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
        
        # Cria perfil padrão (na prática, viria do usuário logado)
        profile_temporario = {
            "nome_marca": "Escritora",
            "estilo_preferido": "elegante",
            "cores_primarias": ["#8B7355", "#F5F1E8", "#5D4037"],
            "fontes": {"titulo": "Cormorant Garamond", "texto": "Inter"}
        }
        
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

@router.post("/sequencia-lancamento")
async def criar_sequencia_lancamento(livro_titulo: str):
    """Cria sequência especial para lançamento de livro"""
    try:
        biblioteca_completa = await biblioteca.get_biblioteca_completa()
        
        # Cria perfil padrão
        profile_temporario = {
            "nome_marca": "Escritora",
            "estilo_preferido": "elegante", 
            "cores_primarias": ["#8B7355", "#F5F1E8", "#5D4037"],
            "fontes": {"titulo": "Cormorant Garamond", "texto": "Inter"}
        }
        
        sequencia = await curadoria.criar_sequencia_lancamento(
            livro_titulo, 
            biblioteca_completa, 
            profile_temporario
        )
        
        return {
            "success": True,
            "sequencia_lancamento": sequencia
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar sequência: {str(e)}")

@router.delete("/remover-livro/{titulo_livro}")
async def remover_livro_biblioteca(titulo_livro: str):
    """Remove um livro da biblioteca"""
    try:
        sucesso = await biblioteca.remover_livro(titulo_livro)
        
        if sucesso:
            return {"success": True, "message": f"Livro '{titulo_livro}' removido da biblioteca"}
        else:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover livro: {str(e)}")
Crie backend/routes/identity_routes.py:
python
from fastapi import APIRouter, HTTPException
from models.marca_profile import MarcaProfile, MarcaProfileResponse
from services.css_generator import CSSGenerator
from services.template_manager import TemplateManager
from database.database import Database

router = APIRouter(prefix="/api/identity", tags=["Identity"])

css_generator = CSSGenerator()
template_manager = TemplateManager()
db = Database()

@router.post("/criar-perfil")
async def criar_perfil_marca(perfil_data: dict):
    """Cria um novo perfil de marca para a escritora"""
    
    try:
        # Valida dados obrigatórios
        if not perfil_data.get("user_id") or not perfil_data.get("nome_marca"):
            raise HTTPException(status_code=400, detail="user_id e nome_marca são obrigatórios")
        
        # Cria perfil de marca
        marca_profile = MarcaProfile.create_default(
            perfil_data["user_id"],
            perfil_data["nome_marca"]
        )
        
        # Aplica customizações se fornecidas
        if perfil_data.get("cores_primarias"):
            marca_profile.cores_primarias = perfil_data["cores_primarias"]
        
        if perfil_data.get("fontes"):
            marca_profile.fontes = perfil_data["fontes"]
            
        if perfil_data.get("estilo_preferido"):
            marca_profile.estilo_preferido = perfil_data["estilo_preferido"]
        
        # Salva no banco (simulação)
        # await db.save_marca_profile(marca_profile)
        
        # Gera CSS personalizado
        css_personalizado = css_generator.gerar_css_personalizado(marca_profile)
        css_preview = css_generator.gerar_css_para_preview(marca_profile)
        
        # Sugere templates
        templates_sugeridos = template_manager.get_templates_por_estilo(marca_profile.estilo_preferido)
        template_recomendado = template_manager.sugerir_template(marca_profile, {})
        
        return {
            "success": True,
            "message": "Perfil de marca criado com sucesso!",
            "perfil": MarcaProfileResponse(**marca_profile.dict()),
            "css_personalizado": css_personalizado,
            "css_preview": css_preview,
            "templates_sugeridos": templates_sugeridos,
            "template_recomendado": template_recomendado
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar perfil: {str(e)}")

@router.get("/templates/{estilo}")
async def get_templates_estilo(estilo: str):
    """Retorna templates disponíveis para um estilo específico"""
    try:
        templates = template_manager.get_templates_por_estilo(estilo)
        templates_escritoras = template_manager.get_templates_para_escritoras()
        
        return {
            "estilo": estilo,
            "templates_gerais": templates,
            "templates_escritoras": templates_escritoras
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar templates: {str(e)}")

@router.post("/gerar-css")
async def gerar_css_personalizado(perfil_data: dict):
    """Gera CSS personalizado baseado no perfil"""
    try:
        # Cria objeto de perfil temporário
        marca_profile = MarcaProfile(
            id="temp",
            user_id="temp",
            nome_marca=perfil_data.get("nome_marca", "Minha Marca"),
            cores_primarias=perfil_data.get("cores_primarias", ["#8B7355", "#F5F1E8", "#5D4037"]),
            fontes=perfil_data.get("fontes", {"titulo": "Cormorant Garamond", "texto": "Inter"}),
            estilo_preferido=perfil_data.get("estilo_preferido", "elegante"),
            created_at=None,
            updated_at=None
        )
        
        css_personalizado = css_generator.gerar_css_personalizado(marca_profile)
        css_preview = css_generator.gerar_css_para_preview(marca_profile)
        
        return {
            "success": True,
            "css_personalizado": css_personalizado,
            "css_preview": css_preview
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar CSS: {str(e)}")

@router.post("/aplicar-identidade")
async def aplicar_identidade_conteudo(conteudo_data: dict):
    """Aplica identidade visual a um conteúdo específico"""
    try:
        from services.identity_applier import IdentityApplier
        
        identity_applier = IdentityApplier()
        
        # Cria perfil temporário
        marca_profile = MarcaProfile(
            id="temp",
            user_id="temp", 
            nome_marca=conteudo_data.get("nome_marca", "Escritora"),
            cores_primarias=conteudo_data.get("cores_primarias", ["#8B7355", "#F5F1E8", "#5D4037"]),
            fontes=conteudo_data.get("fontes", {"titulo": "Cormorant Garamond", "texto": "Inter"}),
            estilo_preferido=conteudo_data.get("estilo_preferido", "elegante"),
            created_at=None,
            updated_at=None
        )
        
        conteudo = conteudo_data.get("conteudo", {})
        formato = conteudo_data.get("formato", "post_instagram")
        
        # Aplica identidade
        conteudo_com_identidade = identity_applier.aplicar_identidade_post(
            conteudo, marca_profile, formato
        )
        
        # Sugere template
        template_sugerido = template_manager.sugerir_template(
            marca_profile, conteudo, conteudo_data.get("contexto", "geral")
        )
        
        diretrizes = template_manager.gerar_diretrizes_template(
            template_sugerido, marca_profile
        )
        
        return {
            "success": True,
            "conteudo_pronto": conteudo_com_identidade,
            "template_sugerido": template_sugerido,
            "diretrizes_implementacao": diretrizes
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao aplicar identidade: {str(e)}")

@router.get("/diretrizes-template")
async def get_diretrizes_template(estilo: str, template_nome: str):
    """Retorna diretrizes detalhadas para um template específico"""
    try:
        templates = template_manager.get_templates_por_estilo(estilo)
        template_encontrado = None
        
        for template in templates:
            if template["nome"] == template_nome:
                template_encontrado = template
                break
        
        if not template_encontrado:
            raise HTTPException(status_code=404, detail="Template não encontrado")
        
        # Cria perfil temporário para gerar diretrizes
        marca_profile = MarcaProfile(
            id="temp",
            user_id="temp",
            nome_marca="Escritora",
            cores_primarias=["#8B7355", "#F5F1E8", "#5D4037"],
            fontes={"titulo": "Cormorant Garamond", "texto": "Inter"},
            estilo_preferido=estilo,
            created_at=None,
            updated_at=None
        )
        
        diretrizes = template_manager.gerar_diretrizes_template(
            template_encontrado, marca_profile
        )
        
        return {
            "template": template_encontrado,
            "diretrizes": diretrizes
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar diretrizes: {str(e)}")
