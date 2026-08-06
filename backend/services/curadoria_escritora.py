from models.marca_profile import MarcaProfile
from services.identity_applier import IdentityApplier
from datetime import datetime, timedelta
import random
from typing import Dict, List

class CuradoriaEscritora:
    def __init__(self):
        self.identity_applier = IdentityApplier()
    
    async def criar_plano_mensal_escritora(self, biblioteca: Dict, marca_profile: MarcaProfile, mes: str = None) -> Dict:
        """Cria plano de 1 mês de conteúdo personalizado para escritora"""
        
        if not mes:
            mes = datetime.now().strftime("%Y-%m")
        
        if not biblioteca:
            raise Exception("Nenhum livro carregado na biblioteca")
        
        # Coleta todos os trechos
        todos_trechos = []
        for livro_titulo, dados in biblioteca.items():
            if "trechos_extraidos" in dados:
                for trecho in dados["trechos_extraidos"]:
                    trecho["fonte_livro"] = livro_titulo
                    trecho["livro_titulo"] = livro_titulo
                    todos_trechos.append(trecho)
        
        if not todos_trechos:
            raise Exception("Nenhum trecho estratégico encontrado")
        
        # Seleciona trechos para o mês
        random.shuffle(todos_trechos)
        trechos_mes = todos_trechos[:10]  # Reduzido para demonstração
        
        # Cria calendário
        calendario = self._estruturar_calendario_mensal(trechos_mes, mes, marca_profile)
        
        return {
            "mes": mes,
            "total_posts": len(trechos_mes),
            "livros_utilizados": list(biblioteca.keys()),
            "calendario": calendario,
            "estrategia_geral": {
                "objetivo_principal": "Fortalecer marca autoral",
                "abordagem": "Conteúdo autêntico e reflexivo",
                "tom_de_voz": "Empático e literário"
            }
        }
    
    def _estruturar_calendario_mensal(self, trechos: List, mes: str, marca_profile: MarcaProfile) -> Dict:
        """Estrutura os trechos em semanas"""
        semanas = {}
        
        for i, trecho in enumerate(trechos):
            semana_num = (i // 2) + 1  # 2 posts por semana
            
            if semana_num not in semanas:
                semanas[semana_num] = {
                    "tema_principal": "Reflexões Literárias",
                    "dias": {}
                }
            
            data_post = datetime.now() + timedelta(days=i)
            
            semanas[semana_num]["dias"][data_post.strftime("%Y-%m-%d")] = {
                "trecho_original": trecho,
                "formato_recomendado": "post_instagram",
                "horario_sugerido": "14:00",
                "hashtags_sugeridas": trecho.get("hashtags_sugeridas", []),
                "pergunta_engajadora": trecho.get("pergunta_engajadora", "")
            }
        
        return semanas
