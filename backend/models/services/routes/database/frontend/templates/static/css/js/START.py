#!/usr/bin/env python3
"""
ALMA DE ESCRITORA - INICIALIZADOR CORRIGIDO
Execute este arquivo primeiro!
"""
import os
import sys
import subprocess
import webbrowser
from time import sleep

def criar_estrutura():
    """Cria toda a estrutura de pastas e arquivos"""
    print("🔄 Criando estrutura do projeto...")
    
    pastas = [
        "backend/models",
        "backend/services",
        "backend/routes", 
        "backend/database",
        "frontend/templates",
        "frontend/static/css",
        "frontend/static/js",
        "frontend/uploads"
    ]
    
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)
        # Criar arquivos __init__.py
        with open(os.path.join(pasta, "__init__.py"), "w") as f:
            pass
    
    print("✅ Estrutura de pastas criada!")

def criar_arquivos_configuracao():
    """Cria arquivos de configuração"""
    print("⚙️ Criando arquivos de configuração...")
    
    # requirements.txt ATUALIZADO para Python 3.13
    with open("backend/requirements.txt", "w") as f:
        f.write("""fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
PyPDF2==3.0.1
python-dotenv==1.0.0
jinja2==3.1.2
aiofiles==23.2.1
requests==2.31.0
""")
    
    # .env
    with open("backend/.env", "w") as f:
        f.write("""OPENAI_API_KEY=sua_chave_aqui
APP_ENV=development
DATABASE_URL=sqlite+aiosqlite:///./almadeescrita.db
""")
    
    print("✅ Arquivos de configuração criados!")

def criar_main_py():
    """Cria o arquivo main.py do backend"""
    print("📝 Criando backend/main.py...")
    
    content = '''from fastapi import FastAPI, Request, UploadFile, File, Form
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
                text += page.extract_text() + "\\n"
            
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
'''
    
    with open("backend/main.py", "w", encoding="utf-8") as f:
        f.write(content)

def criar_templates():
    """Cria os templates HTML simplificados"""
    print("📝 Criando templates HTML...")
    
    # index.html
    index_content = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alma de Escritora</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
</head>
<body class="alma-system">
    <header class="alma-header">
        <div class="container">
            <div class="logo">✍️ Alma de Escritora</div>
            <p class="tagline">Sua identidade literária, transformada em conteúdo</p>
        </div>
    </header>

    <section class="hero-section">
        <div class="container">
            <div class="hero-content">
                <h1>Dê voz à sua <span class="text-primary">essência literária</span></h1>
                <p class="hero-description">
                    Transforme seus textos em conteúdo autêntico que conecta, inspira e constrói sua comunidade leitora.
                </p>
                <div class="hero-actions">
                    <a href="/dashboard-escritora" class="btn btn-primary">Começar Minha Jornada</a>
                    <a href="/identity-setup" class="btn btn-secondary">Criar Identidade</a>
                </div>
            </div>
        </div>
    </section>

    <section class="features-section">
        <div class="container">
            <h2 class="section-title">Como o Alma Transforma sua Escrita</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">📚</div>
                    <h3>Biblioteca Inteligente</h3>
                    <p>Carregue seus livros e extraia trechos impactantes automaticamente.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🎨</div>
                    <h3>Identidade Visual</h3>
                    <p>Crie uma identidade única que reflete sua essência literária.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📅</div>
                    <h3>Curadoria Mensal</h3>
                    <p>Receba um plano completo de conteúdo para suas redes sociais.</p>
                </div>
            </div>
        </div>
    </section>

    <script src="/static/js/main.js"></script>
</body>
</html>'''
    
    with open("frontend/templates/index.html", "w", encoding="utf-8") as f:
        f.write(index_content)
    
    # dashboard_escritora.html
    dashboard_content = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Alma de Escritora</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
</head>
<body class="alma-system">
    <header class="alma-header">
        <div class="container">
            <div class="header-content">
                <div class="logo">✍️ Alma de Escritora</div>
                <nav class="header-nav">
                    <a href="/" class="nav-link">Início</a>
                    <a href="/identity-setup" class="nav-link">Identidade</a>
                    <a href="/dashboard-escritora" class="nav-link active">Dashboard</a>
                </nav>
            </div>
        </div>
    </header>

    <main class="dashboard-main">
        <div class="container">
            <section class="welcome-section">
                <h1>Bem-vinda à sua Oficina Literária! ✨</h1>
                <p class="welcome-subtitle">Aqui sua obra ganha vida e conexão com seus leitores.</p>
            </section>

            <section class="stats-section">
                <div class="biblioteca-status" id="bibliotecaStats">
                    <p><strong id="totalLivros">0</strong><span>Livros Carregados</span></p>
                    <p><strong id="totalTrechos">0</strong><span>Trechos Extraídos</span></p>
                    <p><strong id="totalTemas">0</strong><span>Temas Identificados</span></p>
                </div>
            </section>

            <section class="actions-grid">
                <div class="action-card" onclick="showSection('uploadSection')">
                    <div class="action-icon">📚</div>
                    <h3>Carregar Novo Livro</h3>
                    <p>Adicione sua obra à biblioteca para análise</p>
                </div>
                
                <div class="action-card" onclick="showSection('bibliotecaSection')">
                    <div class="action-icon">📖</div>
                    <h3>Minha Biblioteca</h3>
                    <p>Veja todos seus livros e trechos extraídos</p>
                </div>
                
                <div class="action-card" onclick="showSection('trechosSection')">
                    <div class="action-icon">💫</div>
                    <h3>Trechos em Destaque</h3>
                    <p>Seleções especiais da sua obra</p>
                </div>
            </section>

            <!-- Upload Section -->
            <section id="uploadSection" class="content-section" style="display: none;">
                <div class="section-header">
                    <h2 class="section-title">📚 Carregar Novo Livro</h2>
                    <button class="btn btn-secondary" onclick="hideSection('uploadSection')">Fechar</button>
                </div>
                
                <div class="upload-area" id="uploadArea">
                    <div class="upload-icon">📄</div>
                    <h3>Arraste seu livro aqui</h3>
                    <p>Formatos suportados: PDF</p>
                    <input type="file" id="fileInput" accept=".pdf" style="display: none;">
                    <button class="btn btn-primary" onclick="document.getElementById('fileInput').click()">
                        Selecionar Arquivo
                    </button>
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="tituloLivro">Título do Livro</label>
                    <input type="text" id="tituloLivro" class="form-input" placeholder="Ex: O Jardim das Memórias">
                </div>
                
                <button class="btn btn-primary" onclick="carregarLivro()" id="carregarBtn">
                    🚀 Processar Livro
                </button>
            </section>

            <!-- Biblioteca Section -->
            <section id="bibliotecaSection" class="content-section" style="display: none;">
                <div class="section-header">
                    <h2 class="section-title">📖 Minha Biblioteca Pessoal</h2>
                    <button class="btn btn-secondary" onclick="hideSection('bibliotecaSection')">Fechar</button>
                </div>
                
                <div id="bibliotecaContent">
                    <p>Carregue seu primeiro livro para ver sua biblioteca aqui.</p>
                </div>
            </section>

            <!-- Trechos Section -->
            <section id="trechosSection" class="content-section" style="display: none;">
                <div class="section-header">
                    <h2 class="section-title">💫 Trechos em Destaque</h2>
                    <button class="btn btn-secondary" onclick="hideSection('trechosSection')">Fechar</button>
                </div>
                
                <button class="btn btn-primary" onclick="carregarTrechosAleatorios()">🎲 Carregar Trechos Aleatórios</button>
                
                <div class="trechos-grid" id="trechosGrid">
                    <!-- Trechos carregados via JavaScript -->
                </div>
            </section>
        </div>
    </main>

    <script src="/static/js/dashboard_escritora.js"></script>
</body>
</html>'''
    
    with open("frontend/templates/dashboard_escritora.html", "w", encoding="utf-8") as f:
        f.write(dashboard_content)
    
    # identity_setup.html
    identity_content = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Identidade Visual - Alma de Escritora</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
</head>
<body class="alma-system">
    <header class="alma-header">
        <div class="container">
            <div class="logo">✍️ Alma de Escritora</div>
        </div>
    </header>

    <main class="identity-main">
        <div class="container">
            <section class="identity-header">
                <h1>🎨 Crie Sua Identidade Visual Única</h1>
                <p class="identity-subtitle">
                    Sua essência literária merece uma expressão visual que conecta e encanta.
                </p>
            </section>

            <div class="setup-step active">
                <h2 class="section-title">👑 Sua Marca Pessoal</h2>
                
                <div class="form-group">
                    <label class="form-label" for="nomeMarca">Nome da Sua Marca Autoral</label>
                    <input type="text" id="nomeMarca" class="form-input" placeholder="Ex: Literatura & Essência">
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="estiloPreferido">Estilo Visual Preferido</label>
                    <select id="estiloPreferido" class="form-select">
                        <option value="elegante">Elegante & Sofisticado</option>
                        <option value="minimalista">Minimalista & Clean</option>
                        <option value="criativo">Criativo & Expressivo</option>
                    </select>
                </div>
                
                <button class="btn btn-primary" onclick="salvarIdentidade()">
                    💫 Salvar Minha Identidade
                </button>
            </div>

            <div class="preview-container">
                <div id="identityPreview">
                    <p>Preview da sua identidade aparecerá aqui após salvar.</p>
                </div>
            </div>
        </div>
    </main>

    <script src="/static/js/identity.js"></script>
</body>
</html>'''
    
    with open("frontend/templates/identity_setup.html", "w", encoding="utf-8") as f:
        f.write(identity_content)

def criar_static():
    """Cria os arquivos estáticos"""
    print("📝 Criando arquivos estáticos...")
    
    # style.css
    css_content = '''/* ALMA DE ESCRITORA - Sistema de Design */
:root {
    --alma-primaria: #8B7355;
    --alma-secundaria: #F5F1E8;
    --alma-texto: #5D4037;
    --alma-destaque: #6B5B45;
    --alma-borda: #E8DFD2;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.alma-system {
    font-family: 'Inter', sans-serif;
    background-color: var(--alma-secundaria);
    color: var(--alma-texto);
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.alma-header {
    background: var(--alma-primaria);
    color: white;
    padding: 2rem 0;
    text-align: center;
}

.logo {
    font-size: 2.5rem;
    font-weight: 300;
    margin-bottom: 0.5rem;
}

.tagline {
    font-style: italic;
    opacity: 0.9;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header-nav {
    display: flex;
    gap: 2rem;
}

.nav-link {
    color: white;
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    transition: background 0.3s ease;
}

.nav-link:hover, .nav-link.active {
    background: rgba(255, 255, 255, 0.1);
}

.hero-section {
    padding: 4rem 0;
    text-align: center;
}

.hero-content h1 {
    font-size: 3rem;
    margin-bottom: 1.5rem;
    line-height: 1.2;
}

.hero-description {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    opacity: 0.8;
}

.hero-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

.features-section {
    padding: 4rem 0;
    background: white;
}

.section-title {
    color: var(--alma-primaria);
    margin-bottom: 3rem;
    font-size: 2.2rem;
    text-align: center;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
}

.feature-card {
    background: var(--alma-secundaria);
    padding: 2rem;
    border-radius: 12px;
    border-left: 4px solid var(--alma-primaria);
    transition: transform 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.feature-card h3 {
    margin-bottom: 1rem;
    color: var(--alma-primaria);
}

/* Dashboard Styles */
.dashboard-main {
    padding: 2rem 0;
}

.welcome-section {
    text-align: center;
    margin-bottom: 3rem;
}

.welcome-section h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.welcome-subtitle {
    font-size: 1.2rem;
    opacity: 0.8;
}

.biblioteca-status {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}

.biblioteca-status p {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    border-left: 3px solid var(--alma-primaria);
}

.biblioteca-status strong {
    display: block;
    font-size: 2rem;
    color: var(--alma-primaria);
    margin-bottom: 0.5rem;
}

.actions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 3rem;
}

.action-card {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.action-card:hover {
    border-color: var(--alma-primaria);
    transform: translateY(-3px);
}

.action-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.action-card h3 {
    margin-bottom: 1rem;
    color: var(--alma-primaria);
}

.content-section {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    flex-wrap: wrap;
    gap: 1rem;
}

.upload-area {
    border: 2px dashed var(--alma-primaria);
    border-radius: 12px;
    padding: 3rem;
    text-align: center;
    transition: all 0.3s ease;
    background: rgba(139, 115, 85, 0.05);
    margin-bottom: 2rem;
}

.upload-area:hover {
    border-color: var(--alma-destaque);
    background: rgba(139, 115, 85, 0.1);
}

.upload-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: var(--alma-primaria);
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.form-input, .form-select {
    width: 100%;
    padding: 12px;
    border: 2px solid var(--alma-borda);
    border-radius: 6px;
    font-family: inherit;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}

.form-input:focus, .form-select:focus {
    outline: none;
    border-color: var(--alma-primaria);
}

.btn {
    display: inline-block;
    padding: 12px 30px;
    border: none;
    border-radius: 6px;
    font-family: inherit;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    text-align: center;
    font-weight: 500;
}

.btn-primary {
    background: var(--alma-primaria);
    color: white;
}

.btn-primary:hover {
    background: var(--alma-destaque);
    transform: translateY(-2px);
}

.btn-secondary {
    background: transparent;
    color: var(--alma-primaria);
    border: 2px solid var(--alma-primaria);
}

.btn-secondary:hover {
    background: var(--alma-primaria);
    color: white;
    transform: translateY(-2px);
}

.trechos-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-top: 1.5rem;
}

.trecho-card {
    background: var(--alma-secundaria);
    border: 1px solid var(--alma-borda);
    border-radius: 12px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
}

.trecho-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: var(--alma-primaria);
}

.trecho-texto {
    font-style: italic;
    margin-bottom: 1rem;
    line-height: 1.6;
}

.text-primary {
    color: var(--alma-primaria);
}

.preview-container {
    background: var(--alma-secundaria);
    padding: 2rem;
    border-radius: 12px;
    margin-top: 2rem;
}

@media (max-width: 768px) {
    .biblioteca-status {
        grid-template-columns: 1fr;
    }
    
    .hero-content h1 {
        font-size: 2rem;
    }
    
    .header-content {
        flex-direction: column;
        gap: 1rem;
    }
}'''
    
    with open("frontend/static/css/style.css", "w", encoding="utf-8") as f:
        f.write(css_content)
    
    # main.js
    main_js_content = '''// ALMA DE ESCRITORA - JavaScript
class AlmaDeEscritora {
    constructor() {
        this.init();
    }

    init() {
        console.log('🎨 Alma de Escritora - Sistema inicializado');
    }

    mostrarNotificacao(mensagem, tipo = 'info') {
        alert(mensagem);
    }

    async fazerRequisicao(url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            return await response.json();
        } catch (error) {
            console.error('Erro na requisição:', error);
            this.mostrarNotificacao('Erro de conexão');
            throw error;
        }
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    window.almaApp = new AlmaDeEscritora();
});'''
    
    with open("frontend/static/js/main.js", "w", encoding="utf-8") as f:
        f.write(main_js_content)
    
    # dashboard_escritora.js
    dashboard_js_content = '''// Dashboard da Escritora
class DashboardEscritora {
    constructor() {
        this.init();
    }

    init() {
        console.log('📚 Dashboard inicializado');
        this.carregarBiblioteca();
    }

    async carregarBiblioteca() {
        try {
            const response = await window.almaApp.fazerRequisicao('/api/escritora/biblioteca');
            if (response.estatisticas) {
                this.atualizarEstatisticas(response.estatisticas);
            }
        } catch (error) {
            console.error('Erro ao carregar biblioteca:', error);
        }
    }

    atualizarEstatisticas(estatisticas) {
        document.getElementById('totalLivros').textContent = estatisticas.total_livros;
        document.getElementById('totalTrechos').textContent = estatisticas.total_trechos;
        document.getElementById('totalTemas').textContent = estatisticas.total_temas;
    }

    async carregarLivro() {
        const fileInput = document.getElementById('fileInput');
        const tituloInput = document.getElementById('tituloLivro');

        if (!fileInput.files.length) {
            window.almaApp.mostrarNotificacao('Selecione um arquivo PDF');
            return;
        }

        if (!tituloInput.value.trim()) {
            window.almaApp.mostrarNotificacao('Informe o título do livro');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('titulo_livro', tituloInput.value.trim());

        try {
            const response = await fetch('/api/escritora/carregar-livro', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            
            if (data.success) {
                window.almaApp.mostrarNotificacao(data.message);
                fileInput.value = '';
                tituloInput.value = '';
                this.carregarBiblioteca();
            } else {
                window.almaApp.mostrarNotificacao(data.error);
            }
        } catch (error) {
            console.error('Erro:', error);
            window.almaApp.mostrarNotificacao('Erro ao carregar livro');
        }
    }

    async carregarTrechosAleatorios() {
        try {
            const response = await window.almaApp.fazerRequisicao('/api/escritora/trechos-aleatorios?quantidade=6');
            this.renderizarTrechos(response.trechos);
        } catch (error) {
            console.error('Erro ao carregar trechos:', error);
        }
    }

    renderizarTrechos(trechos) {
        const container = document.getElementById('trechosGrid');
        
        if (!trechos || trechos.length === 0) {
            container.innerHTML = '<p>Nenhum trecho encontrado. Carregue um livro primeiro.</p>';
            return;
        }

        let html = '';
        trechos.forEach(trecho => {
            html += `
                <div class="trecho-card">
                    <div class="trecho-texto">
                        "${trecho.texto}"
                    </div>
                    <div class="trecho-metadata">
                        <strong>Tema:</strong> ${trecho.tema} | 
                        <strong>Engajamento:</strong> ⭐ ${trecho.potencial_engajamento}/10
                    </div>
                    <small>Fonte: ${trecho.fonte_livro}</small>
                </div>
            `;
        });
        
        container.innerHTML = html;
    }
}

// Funções globais
function showSection(sectionId) {
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'block';
}

function hideSection(sectionId) {
    document.getElementById(sectionId).style.display = 'none';
}

function carregarLivro() {
    window.dashboardApp.carregarLivro();
}

function carregarTrechosAleatorios() {
    window.dashboardApp.carregarTrechosAleatorios();
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    window.dashboardApp = new DashboardEscritora();
});'''
    
    with open("frontend/static/js/dashboard_escritora.js", "w", encoding="utf-8") as f:
        f.write(dashboard_js_content)
    
    # identity.js
    identity_js_content = '''// Identity Setup
class IdentitySetup {
    constructor() {
        this.init();
    }

    init() {
        console.log('🎨 Identity Setup inicializado');
    }

    async salvarIdentidade() {
        const nomeMarca = document.getElementById('nomeMarca').value;
        const estiloPreferido = document.getElementById('estiloPreferido').value;

        if (!nomeMarca.trim()) {
            window.almaApp.mostrarNotificacao('Informe o nome da sua marca');
            return;
        }

        const identityData = {
            user_id: 'user_' + Date.now(),
            nome_marca: nomeMarca,
            estilo_preferido: estiloPreferido,
            cores_primarias: ["#8B7355", "#F5F1E8", "#5D4037"],
            fontes: {"titulo": "Cormorant Garamond", "texto": "Inter"}
        };

        try {
            const response = await window.almaApp.fazerRequisicao('/api/identity/criar-perfil', {
                method: 'POST',
                body: JSON.stringify(identityData)
            });

            if (response.success) {
                window.almaApp.mostrarNotificacao('Identidade salva com sucesso!');
                
                // Mostrar preview
                const preview = document.getElementById('identityPreview');
                preview.innerHTML = `
                    <h3>Preview da Sua Identidade</h3>
                    <div style="background: ${response.perfil.cores_primarias[1]}; padding: 20px; border-radius: 10px; border-left: 5px solid ${response.perfil.cores_primarias[0]};">
                        <h4 style="color: ${response.perfil.cores_primarias[0]};">${response.perfil.nome_marca}</h4>
                        <p style="color: ${response.perfil.cores_primarias[2]};">"Há silêncios que falam mais que palavras..."</p>
                        <small>Estilo: ${response.perfil.estilo_preferido}</small>
                    </div>
                `;
                
                setTimeout(() => {
                    window.location.href = '/dashboard-escritora';
                }, 3000);
            }
        } catch (error) {
            console.error('Erro:', error);
            window.almaApp.mostrarNotificacao('Erro ao salvar identidade');
        }
    }
}

function salvarIdentidade() {
    window.identityApp.salvarIdentidade();
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    window.identityApp = new IdentitySetup();
});'''
    
    with open("frontend/static/js/identity.js", "w", encoding="utf-8") as f:
        f.write(identity_js_content)

def instalar_dependencias():
    """Instala dependências automaticamente"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na instalação: {e}")
        print("💡 Execute manualmente: pip install -r backend/requirements.txt")
        return False

def main():
    print("""
    🎨 ALMA DE ESCRITORA - Sistema Simplificado
    ===========================================
    """)
    
    # Criar estrutura
    criar_estrutura()
    criar_arquivos_configuracao()
    
    # Criar arquivos de código
    print("\n📝 Criando arquivos de código...")
    criar_main_py()
    criar_templates()
    criar_static()
    
    print("✅ TODOS os arquivos criados!")
    
    # Instalar dependências
    if instalar_dependencias():
        print("\n🚀 Iniciando servidor...")
        sleep(2)
        
        # Abrir navegador
        webbrowser.open("http://localhost:8000")
        
        # Iniciar servidor
        os.chdir("backend")
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    else:
        print("\n⚠️  Execute manualmente: cd backend && python main.py")

if __name__ == "__main__":
    main()
    