from typing import Dict, List
from models.marca_profile import MarcaProfile

class TemplateManager:
    def get_templates_por_estilo(self, estilo: str) -> List[Dict]:
        """Retorna templates que combinam com o estilo visual"""
        
        templates = {
            "minimalista": [
                {
                    "nome": "Clean & Simple",
                    "descricao": "Máximo de espaço em branco, foco no conteúdo",
                    "caracteristicas": ["branco predominante", "tipografia forte"],
                    "elementos_visuais": ["espaço negativo", "fontes sans-serif"],
                    "adequado_para": ["textos longos", "frases impactantes"]
                }
            ],
            "elegante": [
                {
                    "nome": "Serif Sofisticado", 
                    "descricao": "Fontes serifadas clássicas e elementos de luxo",
                    "caracteristicas": ["serifas tradicionais", "margens generosas"],
                    "elementos_visuais": ["bordas ornamentais", "papel texturizado"],
                    "adequado_para": ["trechos clássicos", "reflexões profundas"]
                }
            ],
            "criativo": [
                {
                    "nome": "Colorido Expressivo",
                    "descricao": "Uso ousado de cores e formas orgânicas",
                    "caracteristicas": ["paleta expansiva", "formas fluidas"],
                    "elementos_visuais": ["pinceladas texturizadas", "gradientes"],
                    "adequado_para": ["poesia moderna", "experimentação"]
                }
            ]
        }
        
        return templates.get(estilo, templates["elegante"])
