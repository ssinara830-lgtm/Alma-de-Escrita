from fastapi import APIRouter, HTTPException
from services.ai_analyzer import AIAnalyzer
from services.identity_applier import IdentityApplier

router = APIRouter(prefix="/api/content", tags=["Content"])

ai_analyzer = AIAnalyzer()
identity_applier = IdentityApplier()

@router.post("/analisar-trecho")
async def analisar_trecho_literario(trecho_data: dict):
    """Analisa um trecho literário específico"""
    
    try:
        trecho = trecho_data.get("texto", "")
        
        if not trecho.strip():
            raise HTTPException(status_code=400, detail="Trecho vazio")
        
        # Cria perfil padrão para análise
        from models.marca_profile import MarcaProfile
        profile_analise = MarcaProfile.create_default("escritora", "Análise de Trecho")
        
        # Aplica análise de IA
        analise = await ai_analyzer.analyze_text_with_identity(trecho, profile_analise)
        
        return {
            "success": True,
            "analise": analise
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na análise: {str(e)}")

@router.get("/formatos-disponiveis")
async def get_formatos_conteudo():
    """Retorna todos os formatos de conteúdo disponíveis"""
    
    formatos = {
        "instagram": [
            {"valor": "post_instagram", "label": "Post Único", "descricao": "Post tradicional do feed"},
            {"valor": "carrossel", "label": "Carrossel", "descricao": "Múltiplos cards deslizantes"},
            {"valor": "story", "label": "Story", "descricao": "Conteúdo temporário de 15 segundos"}
        ]
    }
    
    return {
        "formatos_por_plataforma": formatos
    }
