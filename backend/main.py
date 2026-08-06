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
import re
from collections import Counter

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

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

# Stopwords em português para a análise heurística (sem IA)
_STOPWORDS = {
    "a", "o", "e", "de", "do", "da", "das", "dos", "que", "em", "um", "uma", "para",
    "com", "não", "se", "na", "no", "por", "as", "os", "à", "ao", "aos", "às", "seu",
    "sua", "seus", "suas", "ele", "ela", "eles", "elas", "eu", "tu", "você", "nós",
    "me", "te", "lhe", "meu", "minha", "mais", "mas", "como", "quando", "onde", "porque",
    "isso", "isto", "aquilo", "este", "esta", "esse", "essa", "the", "of", "and", "to",
    "foi", "era", "são", "ser", "estar", "ter", "há", "já", "só", "também", "muito",
    "seus", "suas", "num", "numa", "pelo", "pela", "entre", "até", "sobre", "seu",
    "havia", "pelos", "pelas", "cada", "ainda", "sempre", "nunca", "todo", "toda",
    "tambem", "apenas", "mesmo", "assim", "então", "entao", "depois", "antes", "sem",
    "aqui", "ali", "lá", "tão", "tao", "era", "foram", "tinha", "tinham", "esta",
}


class SimpleAnalyzer:
    """
    Análise real de textos literários.

    - Se houver OPENAI_API_KEY no ambiente, usa a OpenAI para uma análise rica.
    - Sem chave (ou em caso de erro), faz uma análise heurística DE VERDADE sobre
      o texto enviado (temas por frequência, frases extraídas do próprio texto),
      em vez de respostas fixas.
    """

    def analyze_text(self, text: str):
        text = (text or "").strip()
        if not text:
            return {"trechos_selecionados": [], "temas_principais": [], "frases_instagramaveis": []}

        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if api_key and not api_key.lower().startswith("sua_"):
            try:
                return self._analyze_with_openai(text, api_key)
            except Exception as e:
                # Não quebra a aplicação: cai para a análise heurística
                print(f"[IA] Falha na OpenAI, usando análise heurística: {e}")

        return self._analyze_heuristic(text)

    # ---------- Análise com IA (OpenAI) ----------
    def _analyze_with_openai(self, text: str, api_key: str):
        import openai
        client = openai.OpenAI(api_key=api_key)
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        prompt = (
            "Você é uma curadora literária que ajuda escritoras a transformar suas obras "
            "em conteúdo para redes sociais. Analise o trecho abaixo e responda SOMENTE com "
            "um JSON válido, sem texto extra, no formato:\n"
            '{"temas_principais": ["..."], "frases_instagramaveis": ["..."], '
            '"trechos_selecionados": [{"texto": "...", "tema": "...", "tom_recomendado": "...", '
            '"pergunta_engajadora": "...", "hashtags_sugeridas": ["#..."]}]}\n\n'
            "As 'frases_instagramaveis' devem ser extraídas ou inspiradas no próprio texto. "
            f"Texto:\n\"\"\"\n{text[:4000]}\n\"\"\""
        )

        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"},
        )
        data = json.loads(resp.choices[0].message.content)

        # Garante as chaves esperadas
        data.setdefault("temas_principais", [])
        data.setdefault("frases_instagramaveis", [])
        data.setdefault("trechos_selecionados", [])
        data["_fonte_analise"] = f"openai:{model}"
        return data

    # ---------- Análise heurística (sem IA, mas real) ----------
    def _analyze_heuristic(self, text: str):
        # Frases reais do texto
        frases = [f.strip() for f in re.split(r"(?<=[.!?…])\s+", text) if len(f.strip()) > 15]

        # Temas por frequência de palavras significativas
        palavras = re.findall(r"[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÓÔÕÖÚÇÑ]{4,}", text.lower())
        significativas = [p for p in palavras if p not in _STOPWORDS]
        temas = [w.capitalize() for w, _ in Counter(significativas).most_common(5)] or ["Literatura"]

        # "Frases instagramáveis": frases curtas e completas extraídas do texto
        instagramaveis = sorted(
            [f for f in frases if 25 <= len(f) <= 130],
            key=lambda f: abs(70 - len(f))
        )[:3] or (frases[:1] if frases else [])

        # Trecho de destaque = a frase de maior "peso" (mais palavras significativas)
        def peso(f):
            return sum(1 for p in re.findall(r"\w{4,}", f.lower()) if p not in _STOPWORDS)
        trecho_destaque = max(frases, key=peso) if frases else text[:200]

        hashtags = []
        for h in ["#Literatura", "#Escrita"] + ["#" + t.replace(" ", "") for t in temas[:3]]:
            if h not in hashtags:
                hashtags.append(h)

        return {
            "estatisticas": {
                "total_palavras": len(palavras),
                "total_frases": len(frases),
                "tempo_leitura_min": max(1, round(len(palavras) / 200)),
            },
            "temas_principais": temas,
            "frases_instagramaveis": instagramaveis,
            "trechos_selecionados": [
                {
                    "texto": trecho_destaque,
                    "tema": temas[0] if temas else "Reflexão",
                    "tom_recomendado": "poético",
                    "potencial_engajamento": min(10, 5 + len(temas)),
                    "formatos_recomendados": ["post_instagram", "story"],
                    "pergunta_engajadora": "O que essa passagem desperta em você?",
                    "hashtags_sugeridas": hashtags,
                }
            ],
            "_fonte_analise": "heuristica",
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
