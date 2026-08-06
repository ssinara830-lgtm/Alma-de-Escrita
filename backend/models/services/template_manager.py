from typing import Dict, List
from models.marca_profile import MarcaProfile

class TemplateManager:
    def get_templates_por_estilo(self, estilo: str) -> List[Dict]:
        """Retorna templates que combinam com o estilo visual"""
        
        templates_por_estilo = {
            "minimalista": [
                {
                    "nome": "Clean & Simple",
                    "descricao": "Máximo de espaço em branco, foco absoluto no conteúdo",
                    "caracteristicas": ["branco predominante", "tipografia forte", "limpo e organizado"],
                    "elementos_visuais": ["muito espaço negativo", "fontes sans-serif", "alinhamento rigoroso"],
                    "adequado_para": ["textos longos", "frases impactantes", "conteúdo reflexivo"]
                },
                {
                    "nome": "Tipográfico Puro", 
                    "descricao": "Hierarquia clara de fontes como elemento central",
                    "caracteristicas": ["hierarquia tipográfica", "contraste de pesos", "espaçamento generoso"],
                    "elementos_visuais": ["fontes serifadas", "escala tipográfica", "grid invisível"],
                    "adequado_para": ["citações literárias", "trechos poéticos", "pensamentos profundos"]
                }
            ],
            "elegante": [
                {
                    "nome": "Serif Sofisticado",
                    "descricao": "Fontes serifadas clássicas e elementos de luxo sutis",
                    "caracteristicas": ["serifas tradicionais", "dourados discretos", "margens generosas"],
                    "elementos_visuais": ["bordas ornamentais", "capitulares decoradas", "papel texturizado"],
                    "adequado_para": ["trechos clássicos", "reflexões profundas", "conteúdo atemporal"]
                },
                {
                    "nome": "Moderno Elegante",
                    "descricao": "Combina modernidade minimalista com toques de sofisticação",
                    "caracteristicas": ["híbrido serif-sans", "espaçamento calculado", "contraste controlado"],
                    "elementos_visuais": ["linhas finas", "transparências sutis", "geometria suave"],
                    "adequado_para": ["autores contemporâneos", "ensaios modernos", "crítica literária"]
                }
            ],
            "criativo": [
                {
                    "nome": "Colorido Expressivo",
                    "descricao": "Uso ousado e emocional de cores e formas orgânicas",
                    "caracteristicas": ["paleta expansiva", "formas fluidas", "composição assimétrica"],
                    "elementos_visuais": ["pinceladas texturizadas", "sobreposições", "gradientes orgânicos"],
                    "adequado_para": ["poesia moderna", "contos fantásticos", "experimentação literária"]
                },
                {
                    "nome": "Artesanal Autoral",
                    "descricao": "Texturas manuais e elementos que remetem ao processo criativo",
                    "caracteristicas": ["texturas reais", "imperfeições calculadas", "elementos manuais"],
                    "elementos_visuais": ["papel artesanal", "manchas de tinta", "caligrafia"],
                    "adequado_para": ["processo criativo", "cadernos de anotações", "rascunhos autorais"]
                }
            ],
            "profissional": [
                {
                    "nome": "Corporativo Literário",
                    "descricao": "Abordagem profissional mantendo sensibilidade literária",
                    "caracteristicas": ["estrutura clara", "branding consistente", "comunicação direta"],
                    "elementos_visuais": ["logotipo integrado", "paleta corporativa", "fotografia profissional"],
                    "adequado_para": ["escritores estabelecidos", "lançamentos comerciais", "parcerias editoriais"]
                }
            ]
        }
        
        return templates_por_estilo.get(estilo, templates_por_estilo["elegante"])
    
    def sugerir_template(self, marca_profile: MarcaProfile, conteudo: Dict, contexto: str = "geral") -> Dict:
        """Sugere o melhor template baseado no conteúdo e contexto"""
        
        templates = self.get_templates_por_estilo(marca_profile.estilo_preferido)
        
        # Lógica de sugestão baseada em características do conteúdo
        texto = conteudo.get('texto', '')
        tema = conteudo.get('tema', '').lower()
        
        if contexto == "lancamento":
            # Para lançamentos, templates mais impactantes
            return templates[1] if len(templates) > 1 else templates[0]
        
        elif len(texto) > 300:
            # Textos longos: templates mais limpos
            for template in templates:
                if "textos longos" in template.get("adequado_para", []):
                    return template
        
        elif any(palavra in tema for palavra in ['poesia', 'poético', 'verso']):
            # Conteúdo poético: templates mais expressivos
            for template in templates:
                if "poesia" in template.get("adequado_para", []):
                    return template
        
        # Fallback: primeiro template do estilo
        return templates[0]
    
    def gerar_diretrizes_template(self, template: Dict, marca_profile: MarcaProfile) -> List[str]:
        """Gera diretrizes específicas para implementação do template"""
        
        diretrizes = [
            f"Template: {template['nome']}",
            f"Estilo: {marca_profile.estilo_preferido}",
            f"Descrição: {template['descricao']}",
            "",
            "🎨 DIRETRIZES VISUAIS:"
        ]
        
        # Adiciona características
        diretrizes.extend([f"• {caract}" for caract in template['caracteristicas']])
        
        diretrizes.extend([
            "",
            "📐 ELEMENTOS-CHAVE:"
        ])
        
        # Adiciona elementos visuais
        diretrizes.extend([f"• {elemento}" for elemento in template['elementos_visuais']])
        
        diretrizes.extend([
            "",
            "💡 APLICAÇÃO PRÁTICA:"
        ])
        
        # Adiciona adequações
        diretrizes.extend([f"• Ideal para: {adequacao}" for adequacao in template['adequado_para']])
        
        return diretrizes
    
    def get_templates_para_escritoras(self) -> Dict[str, List[Dict]]:
        """Retorna templates especialmente curados para escritoras"""
        
        return {
            "contemporaneas": [
                {
                    "nome": "Voz Autoral Moderna",
                    "descricao": "Para escritoras que exploram temas contemporâneos com sensibilidade",
                    "caracteristicas": ["paleta terrosa", "fontes humanistas", "espaço para respiro"],
                    "elementos_visuais": ["fotografia natural", "texturas sutis", "composição orgânica"],
                    "adequado_para": ["romances contemporâneos", "ensaios pessoais", "crônicas urbanas"]
                }
            ],
            "poeticas": [
                {
                    "nome": "Página de Caderno",
                    "descricao": "Estética de caderno de anotações com toques poéticos",
                    "caracteristicas": ["fundo texturizado", "caligrafia sutil", "margens irregulares"],
                    "elementos_visuais": ["papel envelhecido", "manchas de água", "anotações à mão"],
                    "adequado_para": ["poesia", "microcontos", "pensamentos soltos"]
                }
            ],
            "ficcao": [
                {
                    "nome": "Universal Narrativo",
                    "descricao": "Para histórias que transcendem tempo e espaço",
                    "caracteristicas": ["cores universais", "tipografia atemporal", "composição cinematográfica"],
                    "elementos_visuais": ["elementos simbólicos", "gradientes sutis", "perspectiva dramática"],
                    "adequado_para": ["ficção literária", "romances épicos", "contos universais"]
                }
            ]
        }

