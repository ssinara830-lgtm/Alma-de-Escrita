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
        contexto = trecho_data.get("contexto", "geral")
        
        if not trecho.strip():
            raise HTTPException(status_code=400, detail="Trecho vazio")
        
        # Cria perfil padrão para análise
        from models.marca_profile import MarcaProfile
        profile_analise = MarcaProfile.create_default("escritora", "Análise de Trecho")
        
        # Aplica análise de IA
        analise = await ai_analyzer.analyze_text_with_identity(trecho, profile_analise)
        
        return {
            "success": True,
            "analise": analise,
            "contexto": contexto
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na análise: {str(e)}")

@router.post("/gerar-ideias")
async def gerar_ideias_conteudo(ideias_data: dict):
    """Gera ideias de conteúdo baseadas em um tema"""
    
    try:
        tema = ideias_data.get("tema", "")
        estilo = ideias_data.get("estilo", "elegante")
        
        if not tema.strip():
            raise HTTPException(status_code=400, detail="Tema não especificado")
        
        # Cria perfil temporário
        from models.marca_profile import MarcaProfile
        profile_temporario = MarcaProfile(
            id="temp",
            user_id="temp",
            nome_marca="Escritora",
            cores_primarias=ideias_data.get("cores", ["#8B7355", "#F5F1E8", "#5D4037"]),
            fontes=ideias_data.get("fontes", {"titulo": "Cormorant Garamond", "texto": "Inter"}),
            estilo_preferido=estilo,
            created_at=None,
            updated_at=None
        )
        
        # Gera ideias
        ideias = await ai_analyzer.generate_content_ideas(tema, profile_temporario)
        
        return {
            "success": True,
            "tema": tema,
            "ideias": ideias
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar ideias: {str(e)}")

@router.post("/otimizar-post")
async def otimizar_post_redes_sociais(post_data: dict):
    """Otimiza um post para redes sociais aplicando identidade"""
    
    try:
        texto_original = post_data.get("texto", "")
        formato = post_data.get("formato", "post_instagram")
        plataforma = post_data.get("plataforma", "instagram")
        
        if not texto_original.strip():
            raise HTTPException(status_code=400, detail="Texto do post vazio")
        
        # Cria perfil de identidade
        from models.marca_profile import MarcaProfile
        marca_profile = MarcaProfile(
            id="temp",
            user_id="temp",
            nome_marca=post_data.get("nome_marca", "Escritora"),
            cores_primarias=post_data.get("cores_primarias", ["#8B7355", "#F5F1E8", "#5D4037"]),
            fontes=post_data.get("fontes", {"titulo": "Cormorant Garamond", "texto": "Inter"}),
            estilo_preferido=post_data.get("estilo_preferido", "elegante"),
            created_at=None,
            updated_at=None
        )
        
        # Prepara conteúdo para aplicação de identidade
        conteudo_base = {
            "texto": texto_original,
            "tema": post_data.get("tema", "Literatura"),
            "pergunta_engajadora": post_data.get("pergunta_engajadora", ""),
            "hashtags_sugeridas": post_data.get("hashtags", [])
        }
        
        # Aplica identidade visual
        conteudo_otimizado = identity_applier.aplicar_identidade_post(
            conteudo_base, marca_profile, formato
        )
        
        return {
            "success": True,
            "post_original": texto_original,
            "post_otimizado": conteudo_otimizado,
            "plataforma": plataforma,
            "formato": formato
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao otimizar post: {str(e)}")

@router.get("/formatos-disponiveis")
async def get_formatos_conteudo():
    """Retorna todos os formatos de conteúdo disponíveis"""
    
    formatos = {
        "instagram": [
            {"valor": "post_instagram", "label": "Post Único", "descricao": "Post tradicional do feed"},
            {"valor": "carrossel", "label": "Carrossel", "descricao": "Múltiplos cards deslizantes"},
            {"valor": "story", "label": "Story", "descricao": "Conteúdo temporário de 15 segundos"},
            {"valor": "reels", "label": "Reels", "descricao": "Vídeos curtos e engajadores"}
        ],
        "twitter": [
            {"valor": "tweet_simples", "label": "Tweet Simples", "descricao": "Postagem rápida no Twitter"},
            {"valor": "thread", "label": "Thread", "descricao": "Série de tweets conectados"}
        ],
        "linkedin": [
            {"valor": "post_linkedin", "label": "Post LinkedIn", "descricao": "Conteúdo profissional"},
            {"valor": "article", "label": "Artigo", "descricao": "Conteúdo longo formatado"}
        ]
    }
    
    return {
        "formatos_por_plataforma": formatos,
        "todas_plataformas": list(formatos.keys())
    }

@router.post("/preview-html")
async def gerar_preview_html(preview_data: dict):
    """Gera HTML de preview para um conteúdo"""
    
    try:
        from services.identity_applier import IdentityApplier
        
        identity_applier = IdentityApplier()
        
        # Cria perfil temporário
        from models.marca_profile import MarcaProfile
        marca_profile = MarcaProfile(
            id="temp",
            user_id="temp",
            nome_marca=preview_data.get("nome_marca", "Escritora"),
            cores_primarias=preview_data.get("cores_primarias", ["#8B7355", "#F5F1E8", "#5D4037"]),
            fontes=preview_data.get("fontes", {"titulo": "Cormorant Garamond", "texto": "Inter"}),
            estilo_preferido=preview_data.get("estilo_preferido", "elegante"),
            created_at=None,
            updated_at=None
        )
        
        conteudo = preview_data.get("conteudo", {})
        formato = preview_data.get("formato", "post_instagram")
        
        # Aplica identidade para obter o HTML de preview
        conteudo_com_identidade = identity_applier.aplicar_identidade_post(
            conteudo, marca_profile, formato
        )
        
        html_preview = conteudo_com_identidade.get("conteudo", {}).get("preview_html", "")
        
        return {
            "success": True,
            "html_preview": html_preview,
            "css_inline": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar preview: {str(e)}")
