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
        
        # Coleta todos os trechos de todos os livros
        todos_trechos = []
        for livro_titulo, dados in biblioteca.items():
            if "trechos_extraidos" in dados:
                for trecho in dados["trechos_extraidos"]:
                    trecho["fonte_livro"] = livro_titulo
                    trecho["livro_titulo"] = livro_titulo
                    todos_trechos.append(trecho)
        
        if not todos_trechos:
            raise Exception("Nenhum trecho estratégico encontrado nos livros")
        
        # Embaralha e seleciona trechos para o mês (20-25 posts)
        random.shuffle(todos_trechos)
        trechos_mes = todos_trechos[:25]
        
        # Cria calendário semanal organizado
        calendario = self._estruturar_calendario_mensal(trechos_mes, mes, marca_profile)
        
        # Estratégia geral do mês
        estrategia = self._criar_estrategia_mensal(biblioteca, marca_profile)
        
        return {
            "mes": mes,
            "total_posts": len(trechos_mes),
            "livros_utilizados": list(biblioteca.keys()),
            "calendario": calendario,
            "estrategia_geral": estrategia,
            "marca_aplicada": {
                "nome_marca": marca_profile.nome_marca,
                "estilo": marca_profile.estilo_preferido,
                "cores": marca_profile.cores_primarias
            }
        }
    
    def _estruturar_calendario_mensal(self, trechos: List, mes: str, marca_profile: MarcaProfile) -> Dict:
        """Estrutura os trechos em semanas temáticas"""
        
        semanas = {}
        data_inicio = datetime.now().replace(day=1)  # Começa no primeiro dia do mês
        
        # Define temas para cada semana
        temas_semana = {
            1: "Apresentação e Conexão com a Obra",
            2: "Profundidade e Reflexão", 
            3: "Personagens e Narrativa",
            4: "Processo Criativo e Inspiração",
            5: "Conexão com Leitores"
        }
        
        for i, trecho in enumerate(trechos):
            semana_num = (i // 5) + 1  # 5 posts por semana
            dia_semana = i % 5  # Segunda a Sexta
            
            if semana_num not in semanas:
                semanas[semana_num] = {
                    "tema_principal": temas_semana.get(semana_num, "Reflexões Literárias"),
                    "objetivo": self._definir_objetivo_semana(semana_num),
                    "dias": {}
                }
            
            # Calcula data do post (segunda a sexta)
            data_post = data_inicio + timedelta(days=((semana_num-1)*7 + dia_semana))
            
            # Aplica identidade visual ao conteúdo
            formato_recomendado = trecho.get("formatos_recomendados", ["post_instagram"])[0]
            conteudo_com_identidade = self.identity_applier.aplicar_identidade_post(
                trecho, marca_profile, formato_recomendado
            )
            
            semanas[semana_num]["dias"][data_post.strftime("%Y-%m-%d")] = {
                "trecho_original": trecho,
                "conteudo_pronto": conteudo_com_identidade,
                "formato_recomendado": formato_recomendado,
                "horario_sugerido": self._sugerir_horario_escritora(dia_semana),
                "hashtags_sugeridas": trecho.get("hashtags_sugeridas", []),
                "pergunta_engajadora": trecho.get("pergunta_engajadora", ""),
                "dica_visual": trecho.get("dica_visual", "")
            }
        
        return semanas
    
    def _definir_objetivo_semana(self, semana_num: int) -> str:
        """Define objetivo para cada semana"""
        objetivos = {
            1: "Apresentar a obra e criar conexão inicial",
            2: "Explorar profundidade temática e reflexão",
            3: "Destacar personagens e elementos narrativos", 
            4: "Compartilhar processo criativo e inspiração",
            5: "Fortalecer comunidade de leitores"
        }
        return objetivos.get(semana_num, "Engajar comunidade literária")
    
    def _sugerir_horario_escritora(self, dia_semana: int) -> str:
        """Sugere horários que funcionam para conteúdo literário"""
        horarios_seg_qui = ["09:00", "12:00", "15:00", "19:00", "21:00"]
        horarios_sex = ["10:00", "13:00", "16:00", "18:00", "20:00"]
        horarios_fim_semana = ["11:00", "14:00", "17:00", "19:00"]
        
        if dia_semana in [0, 1, 2, 3]:  # Segunda a Quinta
            return random.choice(horarios_seg_qui)
        elif dia_semana == 4:  # Sexta
            return random.choice(horarios_sex)
        else:  # Fim de semana (não usado normalmente)
            return random.choice(horarios_fim_semana)
    
    def _criar_estrategia_mensal(self, biblioteca: Dict, marca_profile: MarcaProfile) -> Dict:
        """Cria estratégia geral do mês"""
        
        # Coleta temas de todos os livros
        todos_temas = set()
        for dados in biblioteca.values():
            if "analise" in dados and "temas_principais" in dados["analise"]:
                for tema in dados["analise"]["temas_principais"]:
                    todos_temas.add(tema)
        
        return {
            "objetivo_principal": "Fortalecer marca autoral e engajar comunidade leitora",
            "abordagem": "Conteúdo que inspira, reflete e conecta através da autenticidade",
            "tom_de_voz": "Empático, profundo, autêntico e literário",
            "temas_abordados": list(todos_temas)[:8],
            "chamadas_acao_sugeridas": [
                "O que essa reflexão desperta em você?",
                "Compartilhe sua experiência nos comentários...",
                "Salve para reler quando precisar de inspiração",
                "Qual personagem você mais se identifica?",
                "Que trecho do livro mais te marcou?"
            ],
            "dica_estratégica": f"Mantenha consistência visual usando {marca_profile.cores_primarias[0]} como cor de destaque"
        }
    
    async def criar_sequencia_lancamento(self, livro_titulo: str, biblioteca: Dict, marca_profile: MarcaProfile) -> Dict:
        """Cria sequência especial para lançamento de livro"""
        
        if livro_titulo not in biblioteca:
            raise Exception("Livro não encontrado na biblioteca")
        
        livro = biblioteca[livro_titulo]
        trechos_livro = livro.get("trechos_extraidos", [])
        
        sequencia = {
            "pre_lancamento": self._criar_pre_lancamento(trechos_livro, marca_profile),
            "lancamento": self._criar_dia_lancamento(livro, marca_profile),
            "pos_lancamento": self._criar_pos_lancamento(trechos_livro, marca_profile)
        }
        
        return sequencia
    
    def _criar_pre_lancamento(self, trechos: List, marca_profile: MarcaProfile) -> List:
        """Cria sequência de pré-lançamento (7 dias)"""
        sequencia = []
        trechos_pre = trechos[:7]
        
        for i, trecho in enumerate(trechos_pre):
            sequencia.append({
                "dia": f"D-{7-i}",
                "objetivo": "Criar expectativa e curiosidade",
                "conteudo": f"Preview: {trecho['texto'][:100]}...",
                "call_to_action": "Fique atento ao lançamento!",
                "hashtags": ["#EmBreve", "#NovoLivro", "#Lançamento"]
            })
        
        return sequencia
    
    def _criar_dia_lancamento(self, livro: Dict, marca_profile: MarcaProfile) -> Dict:
        """Cria conteúdo para o dia do lançamento"""
        return {
            "dia": "Dia do Lançamento",
            "objetivo": "Celebrar e incentivar compras",
            "conteudos": [
                {
                    "horario": "09:00",
                    "tipo": "anuncio",
                    "texto": "🎉 HOJE É O DIA! Meu novo livro está disponível!",
                    "call_to_action": "Link na bio para adquirir 📚"
                },
                {
                    "horario": "14:00", 
                    "tipo": "depoimento",
                    "texto": "Leitores já estão amando! Veja os primeiros comentários...",
                    "call_to_action": "Compartilhe sua experiência 🎊"
                },
                {
                    "horario": "19:00",
                    "tipo": "agradecimento", 
                    "texto": "Obrigada pelo apoio de sempre! Vocês tornam isso possível 💫",
                    "call_to_action": "Comemore comigo nos comentários!"
                }
            ]
        }
    
    def _criar_pos_lancamento(self, trechos: List, marca_profile: MarcaProfile) -> List:
        """Cria sequência pós-lançamento (7 dias)"""
        sequencia = []
        trechos_pos = trechos[7:14] if len(trechos) > 14 else trechos
        
        for i, trecho in enumerate(trechos_pos):
            sequencia.append({
                "dia": f"D+{i+1}",
                "objetivo": "Manter engajamento e compartilhar conteúdo",
                "conteudo": trecho['texto'],
                "call_to_action": "Já leu? Conte nos comentários!",
                "hashtags": ["#Leitura", "#LivroNovo", "#ComunidadeLeitora"]
            })
        
        return sequencia
    