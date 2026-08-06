import PyPDF2
import aiofiles
import io
from typing import List
import re

class PDFProcessor:
    @staticmethod
    async def extract_text_from_pdf(file_path: str) -> str:
        """Extrai texto de arquivo PDF de forma assíncrona"""
        try:
            async with aiofiles.open(file_path, 'rb') as file:
                content = await file.read()
                
            reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Erro ao extrair texto do PDF: {str(e)}")
    
    @staticmethod
    def split_into_chunks(text: str, max_length: int = 1500) -> List[str]:
        """Divide texto em pedaços menores para análise"""
        
        # Divide por parágrafos primeiro
        paragraphs = re.split(r'\n\s*\n', text)
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
                
            if len(current_chunk) + len(paragraph) + 2 <= max_length:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = paragraph
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks if chunks else [text[:max_length]]
    
    @staticmethod
    def extract_metadata(text: str) -> dict:
        """Extrai metadados básicos do texto"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        return {
            "total_palavras": len(words),
            "total_sentencas": len([s for s in sentences if s.strip()]),
            "palavras_unicas": len(set(words)),
            "densidade_vocabulario": len(set(words)) / len(words) if words else 0
        }

