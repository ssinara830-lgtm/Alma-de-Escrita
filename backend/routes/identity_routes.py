from fastapi import APIRouter, HTTPException
from models.marca_profile import MarcaProfile, MarcaProfileResponse
from services.css_generator import CSSGenerator
from services.template_manager import TemplateManager

router = APIRouter(prefix="/api/identity", tags=["Identity"])

css_generator = CSSGenerator()
template_manager = TemplateManager()

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
        
        # Gera CSS personalizado
        css_personalizado = css_generator.gerar_css_personalizado(marca_profile)
        
        # Sugere templates
        templates_sugeridos = template_manager.get_templates_por_estilo(marca_profile.estilo_preferido)
        
        return {
            "success": True,
            "message": "Perfil de marca criado com sucesso!",
            "perfil": MarcaProfileResponse(**marca_profile.dict()),
            "css_personalizado": css_personalizado,
            "templates_sugeridos": templates_sugeridos
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar perfil: {str(e)}")

@router.get("/templates/{estilo}")
async def get_templates_estilo(estilo: str):
    """Retorna templates disponíveis para um estilo específico"""
    try:
        templates = template_manager.get_templates_por_estilo(estilo)
        
        return {
            "estilo": estilo,
            "templates_gerais": templates
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
        
        return {
            "success": True,
            "css_personalizado": css_personalizado
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar CSS: {str(e)}")
