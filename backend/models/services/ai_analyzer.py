import openai
import json
from config import Config
from models.marca_profile import MarcaProfile

openai.api_key = Config.OPENAI_API_KEY

class AIAnalyzer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    
    async def analyze_text_with_identity(self, text: str, marca_profile: MarcaProfile):
        """Analisa texto considerando identidade visual do cliente"""
        
        prompt = f"""
        VOCÊ É: Especialista em curadoria literária e marketing para escritoras.

        IDENTIDADE VISUAL DA ESCRITORA:
        - ESTILO: {marca_profile.estilo_preferido}
        - CORES: {marca_profile.cores_primarias}
        - FONTES: {marca_profile.fontes}

        TEXTO PARA ANALISAR (obra literária):
        {text[:3000]}

        SUA TAREFA ESPECÍFICA PARA ESCRITORA:
        1. Identifique os trechos mais impactantes PARA ESSA IDENTIDADE
        2. Foque em: frases poéticas, insights profundos, momentos emocionais
        3. Sugira formatos que combinem com o estilo visual
        4. Mantenha tom que reforce a marca autoral da escritora

        CRITÉRIOS PARA SELEÇÃO:
        - Potencial de engajamento em redes sociais
        - Valor literário e profundidade
        - Capacidade de gerar reflexão
        - Conexão emocional com leitores

        RETORNE APENAS JSON:
        {{
            "trechos_selecionados": [
                {{
                    "texto": "trecho completo",
                    "tema": "tema principal (ex: solidão, tempo, amor, identidade)",
                    "tom_recomendado": "poético/reflexivo/emocional/profundo",
                    "potencial_engajamento": 8,
                    "formatos_recomendados": ["post_instagram", "story", "carrossel"],
                    "pergunta_engajadora": "pergunta que gera comentários",
                    "dica_visual": "sugestão de aplicação visual baseada nas cores {marca_profile.cores_primarias}",
                    "hashtags_sugeridas": ["#LiteraturaBrasileira", "#Escritora", "#Poesia"]
                }}
            ],
            "temas_principais": ["tema1", "tema2", "tema3"],
            "frases_instagramaveis": ["frase curta e impactante", "outra frase"],
            "analise_identidade": "breve análise de como o conteúdo se alinha com a identidade visual"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            
            analysis_text = response.choices[0].message.content.strip()
            return json.loads(analysis_text)
            
        except Exception as e:
            print(f"Erro na análise com IA: {e}")
            # Fallback para demonstração
            return self.get_fallback_analysis_escritora(text, marca_profile)
    
    def get_fallback_analysis_escritora(self, text: str, marca_profile: MarcaProfile):
        """Análise de fallback específica para escritoras"""
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
                    "dica_visual": f"Use {marca_profile.cores_primarias[0]} para destaques sobre fundo {marca_profile.cores_primarias[1]}",
                    "hashtags_sugeridas": ["#Literatura", "#Escritora", "#Reflexão"]
                }
            ],
            "temas_principais": ["Reflexão", "Crescimento Pessoal", "Emoções"],
            "frases_instagramaveis": [
                "Há silêncios que falam mais que palavras.",
                "A solidão era sua companheira mais honesta."
            ],
            "analise_identidade": f"Conteúdo alinha-se perfeitamente com estilo {marca_profile.estilo_preferido}"
        }
    
    async def generate_content_ideas(self, tema: str, marca_profile: MarcaProfile):
        """Gera ideias de conteúdo baseadas em um tema"""
        prompt = f"""
        Gere ideias de conteúdo para uma escritora com identidade {marca_profile.estilo_preferido}.
        Tema: {tema}
        
        Sugira 3 ideias criativas que combinem com as cores {marca_profile.cores_primarias}.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8
            )
            return response.choices[0].message.content
        except:
            return "Ideias de conteúdo serão geradas aqui."

