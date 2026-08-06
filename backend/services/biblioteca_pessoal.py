from services.pdf_processor import PDFProcessor
from services.ai_analyzer import AIAnalyzer
from models.marca_profile import MarcaProfile
import aiofiles
import os
from typing import Dict, List
import json
from datetime import datetime

class BibliotecaPessoal:
    def __init__(self):
        self.processor = PDFProcessor()
        self.analyzer = AIAnalyzer()
        self.livros_carregados = {}
    
    async def carregar_livro_escritora(self, file_path: str, titulo_livro: str, sinopse: str = "") -> Dict:
        """Carrega e analisa UM dos seus livros profundamente"""
        
        try:
            # Extrai texto completo
            texto_completo = await self.processor.extract_text_from_pdf(file_path)
            
            if not texto_completo.strip():
                raise Exception("PDF não contém texto legível para análise")
            
            # Extrai metadados
            metadados = self.processor.extract_metadata(texto_completo)
            
            # Cria perfil padrão para análise
            profile_analise = MarcaProfile.create_default("escritora", titulo_livro)
            
            # Análise profunda específica para escritora
            analise_profunda = await self.analyzer.analyze_text_with_identity(texto_completo, profile_analise)
            
            # Salva no cache da biblioteca
            self.livros_carregados[titulo_livro] = {
                "titulo": titulo_livro,
                "sinopse": sinopse,
                "texto_completo": texto_completo,
                "metadados": metadados,
                "analise": analise_profunda,
                "trechos_extraidos": analise_profunda["trechos_selecionados"],
                "carregado_em": datetime.now().isoformat(),
                "status": "analisado"
            }
            
            return self.livros_carregados[titulo_livro]
            
        except Exception as e:
            raise Exception(f"Erro ao carregar livro '{titulo_livro}': {str(e)}")
    
    async def get_biblioteca_completa(self) -> Dict:
        """Retorna todos os seus livros carregados"""
        return self.livros_carregados
    
    async def get_trechos_aleatorios(self, quantidade: int = 5) -> List:
        """Seleciona trechos aleatórios de todos os livros"""
        todos_trechos = []
        for livro_titulo, dados in self.livros_carregados.items():
            if "trechos_extraidos" in dados:
                for trecho in dados["trechos_extraidos"]:
                    trecho["fonte_livro"] = livro_titulo
                    todos_trechos.append(trecho)
        
        import random
        return random.sample(todos_trechos, min(quantidade, len(todos_trechos)))
    
    async def buscar_trechos_por_tema(self, tema: str) -> List:
        """Busca trechos por tema específico"""
        trechos_encontrados = []
        
        for livro_titulo, dados in self.livros_carregados.items():
            if "trechos_extraidos" in dados:
                for trecho in dados["trechos_extraidos"]:
                    if tema.lower() in trecho.get("tema", "").lower():
                        trecho["fonte_livro"] = livro_titulo
                        trechos_encontrados.append(trecho)
        
        return trechos_encontrados
    
    async def get_estatisticas_biblioteca(self) -> Dict:
        """Retorna estatísticas da biblioteca"""
        total_livros = len(self.livros_carregados)
        total_trechos = 0
        temas_unicos = set()
        
        for dados in self.livros_carregados.values():
            if "trechos_extraidos" in dados:
                total_trechos += len(dados["trechos_extraidos"])
            if "analise" in dados and "temas_principais" in dados["analise"]:
                for tema in dados["analise"]["temas_principais"]:
                    temas_unicos.add(tema)
        
        return {
            "total_livros": total_livros,
            "total_trechos": total_trechos,
            "total_temas": len(temas_unicos),
            "temas_principais": list(temas_unicos)[:10]
        }
    
    async def remover_livro(self, titulo_livro: str) -> bool:
        """Remove um livro da biblioteca"""
        if titulo_livro in self.livros_carregados:
            del self.livros_carregados[titulo_livro]
            return True
        return False
