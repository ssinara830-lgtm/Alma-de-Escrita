from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import os
import json
from datetime import datetime
import aiofiles
import PyPDF2
import io

app = FastAPI(
    title="Alma de Escritora",
    description="Assistente pessoal de curadoria literária para escritoras",
    version="2.0.0"
)

# Configurar templates e arquivos estáticos
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")

# Simulação de banco de dados em memória
biblioteca = {}
usuarios = {}

class PDFProcessor:
    @staticmethod
    async def extract_text_from_pdf(file_path: str) -> str:
        """Extrai texto de arquivo PDF"""
        try:
            async with aiofiles.open(file_path, 'rb') as file:
                content = await file.read()
                
            reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Erro ao extrair texto: {str(e)}")

class SimpleAnalyzer:
    @staticmethod
    def analyze_text(text: str):
        """Análise simplificada do texto"""
        palavras = text.split()
        trecho = text[:200] + "..." if len(text) > 200 else text
        
        return {
            "trechos_selecionados": [
                {
                    "texto": trecho,
                    "tema": "Reflexão Literária",
                    "tom_recomendado": "poético",
                    "potencial_engajamento": 8,
                    "formatos_recomendados": ["post_instagram", "story"],
                    "pergunta_engajadora": "O que essa reflexão desperta em você?",
                    "hashtags_sugeridas": ["#Literatura", "#Escritora", "#Reflexão"]
                }
            ],
            "temas_principais": ["Literatura", "Reflexão", "Crescimento"],
            "frases_instagramaveis": ["Há silêncios que falam mais que palavras."]
        }

# Rotas principais
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard-escritora", response_class=HTMLResponse)
async def dashboard_escritora(request: Request):
    return templates.TemplateResponse("dashboard_escritora.html", {"request": request})

@app.get("/identity-setup", response_class=HTMLResponse)
async def identity_setup(request: Request):
    return templates.TemplateResponse("identity_setup.html", {"request": request})

# API Routes
@app.post("/api/escritora/carregar-livro")
async def carregar_livro_escritora(
    file: UploadFile = File(...),
    titulo_livro: str = Form(...),
    sinopse: str = Form("")
):
    try:
        # Salvar arquivo
        os.makedirs("../frontend/uploads", exist_ok=True)
        file_path = f"../frontend/uploads/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Processar PDF
        processor = PDFProcessor()
        texto = await processor.extract_text_from_pdf(file_path)
        
        # Analisar texto
        analyzer = SimpleAnalyzer()
        analise = analyzer.analyze_text(texto)
        
        # Salvar na biblioteca
        biblioteca[titulo_livro] = {
            "titulo": titulo_livro,
            "sinopse": sinopse,
            "texto_completo": texto[:1000],  # Limitar para demo
            "analise": analise,
            "trechos_extraidos": analise["trechos_selecionados"],
            "carregado_em": datetime.now().isoformat()
        }
        
        return JSONResponse({
            "success": True,
            "message": f"Livro '{titulo_livro}' carregado com sucesso!",
            "dados": biblioteca[titulo_livro]
        })
        
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.get("/api/escritora/biblioteca")
async def get_biblioteca_completa():
    estatisticas = {
        "total_livros": len(biblioteca),
        "total_trechos": sum(len(livro.get("trechos_extraidos", [])) for livro in biblioteca.values()),
        "total_temas": 5  # Valor fixo para demo
    }
    
    return JSONResponse({
        "biblioteca": biblioteca,
        "estatisticas": estatisticas
    })

@app.get("/api/escritora/trechos-aleatorios")
async def get_trechos_aleatorios(quantidade: int = 5):
    todos_trechos = []
    for livro_titulo, dados in biblioteca.items():
        if "trechos_extraidos" in dados:
            for trecho in dados["trechos_extraidos"]:
                trecho["fonte_livro"] = livro_titulo
                todos_trechos.append(trecho)
    
    import random
    trechos_selecionados = random.sample(todos_trechos, min(quantidade, len(todos_trechos)))
    
    return JSONResponse({"trechos": trechos_selecionados})

@app.post("/api/identity/criar-perfil")
async def criar_perfil_marca(perfil_data: dict):
    try:
        user_id = perfil_data.get("user_id", f"user_{datetime.now().timestamp()}")
        nome_marca = perfil_data.get("nome_marca", "Minha Marca")
        
        perfil = {
            "id": user_id,
            "user_id": user_id,
            "nome_marca": nome_marca,
            "cores_primarias": perfil_data.get("cores_primarias", ["#8B7355", "#F5F1E8", "#5D4037"]),
            "fontes": perfil_data.get("fontes", {"titulo": "Cormorant Garamond", "texto": "Inter"}),
            "estilo_preferido": perfil_data.get("estilo_preferido", "elegante"),
            "created_at": datetime.now().isoformat()
        }
        
        usuarios[user_id] = perfil
        
        # CSS personalizado simples
        css = f"""
:root {{
    --alma-primaria: {perfil['cores_primarias'][0]};
    --alma-secundaria: {perfil['cores_primarias'][1]};
    --alma-texto: {perfil['cores_primarias'][2]};
}}
"""
        
        return JSONResponse({
            "success": True,
            "message": "Perfil criado com sucesso!",
            "perfil": perfil,
            "css_personalizado": css
        })
        
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Alma de Escritora"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
