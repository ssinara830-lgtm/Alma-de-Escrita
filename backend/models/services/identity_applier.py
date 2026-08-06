from models.marca_profile import MarcaProfile
from typing import Dict, Any
import random

class IdentityApplier:
    def aplicar_identidade_post(self, conteudo: dict, marca_profile: MarcaProfile, formato: str) -> Dict[str, Any]:
        """Aplica identidade visual a um post específico"""
        
        templates = {
            "post_instagram": self._template_instagram,
            "story": self._template_story,
            "carrossel": self._template_carrossel,
            "video": self._template_video
        }
        
        template_func = templates.get(formato, self._template_instagram)
        return template_func(conteudo, marca_profile)
    
    def _template_instagram(self, conteudo: dict, marca_profile: MarcaProfile) -> Dict[str, Any]:
        """Template para post do Instagram"""
        
        # Gera hashtags combinando as sugeridas com as padrão
        hashtags_base = ["#LiteraturaBrasileira", "#Escritora", "#Livros", "#Leitura"]
        hashtags_sugeridas = conteudo.get("hashtags_sugeridas", [])
        todas_hashtags = list(set(hashtags_sugeridas + hashtags_base))[:8]
        
        return {
            "platform": "instagram",
            "tipo": "post_unico",
            "conteudo": {
                "imagem_descricao": self._gerar_descricao_imagem(conteudo, marca_profile),
                "copy": self._formatar_copy_instagram(conteudo, marca_profile),
                "hashtags": todas_hashtags,
                "localizacao": None,  # Pode ser personalizado
                "menciones": [],     # Pode adicionar menções
                "estilo_aplicado": {
                    "cor_fundo": marca_profile.cores_primarias[1],
                    "cor_texto": marca_profile.cores_primarias[2],
                    "cor_destaque": marca_profile.cores_primarias[0],
                    "fonte_titulo": marca_profile.fontes["titulo"],
                    "fonte_texto": marca_profile.fontes["texto"],
                    "estilo_visual": marca_profile.estilo_preferido
                }
            },
            "preview_html": self._gerar_html_preview(conteudo, marca_profile),
            "dicas_implementacao": self._gerar_dicas_implementacao(conteudo, marca_profile)
        }
    
    def _template_story(self, conteudo: dict, marca_profile: MarcaProfile) -> Dict[str, Any]:
        """Template para story do Instagram"""
        
        return {
            "platform": "instagram_story",
            "tipo": "story",
            "conteudo": {
                "script": self._gerar_script_story(conteudo),
                "cores": marca_profile.cores_primarias,
                "fontes": marca_profile.fontes,
                "elementos_visuais": self._sugerir_elementos_visuais(conteudo, marca_profile),
                "duracao_sugerida": 15,  # segundos
                "interatividade": self._sugerir_interatividade_story(conteudo)
            },
            "call_to_action": conteudo.get("pergunta_engajadora", "O que você achou?")
        }
    
    def _template_carrossel(self, conteudo: dict, marca_profile: MarcaProfile) -> Dict[str, Any]:
        """Template para carrossel do Instagram"""
        
        # Divide o conteúdo em cards para carrossel
        cards = self._dividir_em_cards(conteudo, 3)
        
        return {
            "platform": "instagram",
            "tipo": "carrossel",
            "conteudo": {
                "cards": cards,
                "titulo_geral": f"{conteudo.get('tema', 'Reflexão')} - {marca_profile.nome_marca}",
                "cores_cards": [
                    marca_profile.cores_primarias[1],  # Card 1
                    marca_profile.cores_primarias[0],  # Card 2  
                    marca_profile.cores_primarias[2]   # Card 3
                ],
                "transicao": "slide",
                "hashtags": conteudo.get("hashtags_sugeridas", []) + ["#Carrossel", "#Reflexão"]
            }
        }
    
    def _template_video(self, conteudo: dict, marca_profile: MarcaProfile) -> Dict[str, Any]:
        """Template para vídeo/reels"""
        
        return {
            "platform": "instagram",
            "tipo": "video",
            "conteudo": {
                "roteiro": self._gerar_roteiro_video(conteudo),
                "duracao_sugerida": 30,  # segundos
                "trilha_sonora": "Instrumental suave ou som ambiente",
                "legenda": self._formatar_copy_instagram(conteudo, marca_profile),
                "elementos_visuais": self._sugerir_elementos_video(conteudo, marca_profile),
                "hashtags": conteudo.get("hashtags_sugeridas", []) + ["#Video", "#Literatura"]
            }
        }
    
    def _gerar_descricao_imagem(self, conteudo: dict, marca_profile: MarcaProfile) -> str:
        """Gera descrição para a imagem do post"""
        estilo = marca_profile.estilo_preferido
        cor_principal = marca_profile.cores_primarias[0]
        
        descricoes = {
            "minimalista": f"Fundo limpo em {marca_profile.cores_primarias[1]} com texto centralizado em {cor_principal}",
            "elegante": f"Composição sofisticada com {cor_principal} como destaque sobre fundo {marca_profile.cores_primarias[1]}",
            "criativo": f"Design orgânico com elementos texturizados nas cores {', '.join(marca_profile.cores_primarias)}"
        }
        
        return descricoes.get(estilo, f"Imagem no estilo {estilo} com cores {marca_profile.cores_primarias}")
    
    def _formatar_copy_instagram(self, conteudo: dict, marca_profile: MarcaProfile) -> str:
        """Formata o texto para Instagram"""
        texto_principal = conteudo['texto']
        pergunta = conteudo.get('pergunta_engajadora', '')
        
        # Formatações baseadas no estilo
        if marca_profile.estilo_preferido == "minimalista":
            copy = f"{texto_principal}"
        elif marca_profile.estilo_preferido == "elegante":
            copy = f"✧ {texto_principal} ✧"
        else:  # criativo
            copy = f"✨ {texto_principal} ✨"
        
        # Adiciona pergunta engajadora
        if pergunta:
            copy += f"\n\n{pergunta}"
        
        # Adiciona assinatura
        copy += f"\n\n— {marca_profile.nome_marca}"
        
        return copy
    
    def _gerar_html_preview(self, conteudo: dict, marca_profile: MarcaProfile) -> str:
        """Gera HTML para preview do post"""
        
        return f"""
        <div class="post-preview" style="
            background: {marca_profile.cores_primarias[1]}; 
            padding: 25px; 
            border-radius: 12px;
            border-left: 5px solid {marca_profile.cores_primarias[0]};
            font-family: {marca_profile.fontes['texto']}, sans-serif;
            max-width: 500px;
            margin: 20px auto;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        ">
            <div style="text-align: center; margin-bottom: 15px;">
                <div style="
                    background: {marca_profile.cores_primarias[0]};
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    display: inline-block;
                    font-size: 0.9em;
                    font-family: {marca_profile.fontes['titulo']}, serif;
                ">
                    {marca_profile.nome_marca}
                </div>
            </div>
            
            <h3 style="
                color: {marca_profile.cores_primarias[0]};
                font-family: {marca_profile.fontes['titulo']}, serif;
                margin-bottom: 20px;
                text-align: center;
                font-size: 1.4em;
            ">
                {conteudo.get('tema', 'Reflexão')}
            </h3>
            
            <p style="
                color: {marca_profile.cores_primarias[2]};
                line-height: 1.7;
                font-size: 1.1em;
                text-align: center;
                margin-bottom: 20px;
            ">
                "{conteudo['texto']}"
            </p>
            
            <div style="
                border-top: 1px solid {marca_profile.cores_primarias[0]};
                padding-top: 15px;
                text-align: center;
            ">
                <p style="
                    color: {marca_profile.cores_primarias[0]};
                    font-size: 0.9em;
                    margin: 0;
                ">
                    {', '.join(conteudo.get('hashtags_sugeridas', ['#Literatura', '#Escritora'])[:3])}
                </p>
            </div>
        </div>
        """
    
    def _gerar_script_story(self, conteudo: dict) -> list:
        """Gera script para stories"""
        return [
            {
                "tela": 1,
                "conteudo": "Pergunta ou chamada inicial",
                "duracao": 3,
                "elementos": ["Texto central", "Fundo colorido"]
            },
            {
                "tela": 2, 
                "conteudo": conteudo['texto'][:100] + "...",
                "duracao": 5,
                "elementos": ["Trecho do livro", "Música suave"]
            },
            {
                "tela": 3,
                "conteudo": conteudo.get('pergunta_engajadora', 'O que achou?'),
                "duracao": 4,
                "elementos": ["Enquete ou pergunta", "CTA para comentários"]
            }
        ]
    
    def _dividir_em_cards(self, conteudo: dict, numero_cards: int) -> list:
        """Divide conteúdo em cards para carrossel"""
        texto = conteudo['texto']
        palavras = texto.split()
        palavras_por_card = len(palavras) // numero_cards
        
        cards = []
        for i in range(numero_cards):
            inicio = i * palavras_por_card
            fim = (i + 1) * palavras_por_card if i < numero_cards - 1 else len(palavras)
            card_texto = ' '.join(palavras[inicio:fim])
            
            cards.append({
                "numero": i + 1,
                "conteudo": card_texto,
                "titulo": f"Parte {i + 1}",
                "dica_visual": f"Card {i + 1} - Foco na legibilidade"
            })
        
        return cards
    
    def _gerar_roteiro_video(self, conteudo: dict) -> list:
        """Gera roteiro para vídeos/reels"""
        return [
            {
                "tempo": "0-3s",
                "acao": "Abertura com pergunta impactante",
                "visual": "Texto animado"
            },
            {
                "tempo": "3-10s", 
                "acao": "Leitura do trecho com expressão",
                "visual": "Vídeo da escritora lendo"
            },
            {
                "tempo": "10-25s",
                "acao": "Reflexão sobre o trecho",
                "visual": "Imagens relacionadas ao tema"
            },
            {
                "tempo": "25-30s",
                "acao": "Chamada para ação",
                "visual": "Texto final com CTA"
            }
        ]
    
    def _sugerir_elementos_visuais(self, conteudo: dict, marca_profile: MarcaProfile) -> list:
        """Sugere elementos visuais baseados no conteúdo"""
        tema = conteudo.get('tema', '').lower()
        elementos = []
        
        if any(palavra in tema for palavra in ['natureza', 'flor', 'árvore']):
            elementos.extend(["Folhas sutis", "Texturas orgânicas"])
        elif any(palavra in tema for palavra in ['tempo', 'memória']):
            elementos.extend(["Relógio estilizado", "Elementos vintage"])
        elif any(palavra in tema for palavra in ['amor', 'emoção']):
            elementos.extend(["Formas orgânicas", "Degradê suave"])
        
        # Elementos baseados no estilo
        if marca_profile.estilo_preferido == "minimalista":
            elementos.append("Espaço em branco generoso")
        elif marca_profile.estilo_preferido == "elegante":
            elementos.append("Bordas douradas sutis")
        else:  # criativo
            elementos.append("Formas abstratas coloridas")
        
        return elementos
    
    def _sugerir_interatividade_story(self, conteudo: dict) -> dict:
        """Sugere elementos interativos para stories"""
        return {
            "tipo": "enquete",
            "pergunta": conteudo.get('pergunta_engajadora', 'Essa reflexão ressoa com você?'),
            "opcoes": ["Sim, totalmente!", "Em partes", "Me fez pensar..."],
            "posicao": "meio"
        }
    
    def _gerar_dicas_implementacao(self, conteudo: dict, marca_profile: MarcaProfile) -> list:
        """Gera dicas para implementação do post"""
        dicas = [
            f"Use a fonte {marca_profile.fontes['titulo']} para títulos",
            f"Destque com a cor {marca_profile.cores_primarias[0]}",
            f"Fundo em {marca_profile.cores_primarias[1]} para contraste"
        ]
        
        # Dicas específicas por formato
        if len(conteudo['texto']) > 200:
            dicas.append("Quebre o texto em parágrafos curtos para melhor legibilidade")
        
        if conteudo.get('pergunta_engajadora'):
            dicas.append("Destaque a pergunta para incentivar comentários")
        
        return dicas
    
    def _sugerir_elementos_video(self, conteudo: dict, marca_profile: MarcaProfile) -> list:
        """Sugere elementos para vídeos"""
        return [
            "Transições suaves",
            "Texto legível com contraste",
            f"Paleta de cores: {', '.join(marca_profile.cores_primarias)}",
            "Música ambiente suave"
        ]
