import openai
import json
from config import Config
from models.marca_profile import MarcaProfile

class AIAnalyzer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    
    async def analyze_text_with_identity(self, text: str, marca_profile: MarcaProfile):
        """Analisa texto considerando identidade visual do cliente"""
        
        # Versão simplificada para demonstração
        sample_text = text[:200] + "..." if len(text) > 200 else text
        
        return {
            "trechos_selecionados": [
                {
                    "texto": sample_text,
                    "tema": "Reflexão Profunda",
                    "tom_recomendado": "poético",
                    "potencial_engajamento": 8,
                    "formatos_recomendados": ["post_instagram", "story"],
                    "pergunta_engajadora": "O que essa reflexão desperta em você?",
                    "dica_visual": f"Use {marca_profile.cores_primarias[0]} para destaques",
                    "hashtags_sugeridas": ["#Literatura", "#Escritora", "#Reflexão"]
                }
            ],
            "temas_principais": ["Reflexão", "Crescimento Pessoal", "Emoções"],
            "frases_instagramaveis": [
                "Há silêncios que falam mais que palavras.",
                "A solidão era sua companheira mais honesta."
            ],
            "analise_identidade": f"Conteúdo alinha-se com estilo {marca_profile.estilo_preferido}"
        }
    
    async def generate_content_ideas(self, tema: str, marca_profile: MarcaProfile):
        """Gera ideias de conteúdo baseadas em um tema"""
        return f"Ideias de conteúdo para: {tema}\n\n1. Post sobre o tema principal\n2. Story com perguntas\n3. Carrossel com citações"
