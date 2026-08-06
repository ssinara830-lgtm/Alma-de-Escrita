#!/usr/bin/env python3
"""
ATUALIZAÇÃO DO ALMA DE ESCRITORA
Adiciona redes sociais e sistema de visualização de posts
"""
import os
import json

def atualizar_main_py():
    """Atualiza o main.py com novas funcionalidades"""
    print("🔄 Atualizando backend/main.py...")
    
    novo_conteudo = '''from fastapi import FastAPI, Request, UploadFile, File, Form
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
import random

app = FastAPI(
    title="Alma de Escritora",
    description="Assistente pessoal de curadoria literária para escritoras",
    version="2.1.0"
)

# Configurar templates e arquivos estáticos
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")

# Simulação de banco de dados em memória
biblioteca = {}
usuarios = {}
posts_gerados = {}

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
        frases = text.split('. ')
        
        # Seleciona trechos variados
        trechos_selecionados = []
        if len(frases) > 3:
            for i in range(min(5, len(frases))):
                if len(frases[i].strip()) > 20:  # Evita frases muito curtas
                    trechos_selecionados.append({
                        "texto": frases[i].strip() + ".",
                        "tema": random.choice(["Reflexão", "Emoção", "Narrativa", "Poesia", "Filosofia"]),
                        "tom_recomendado": random.choice(["poético", "reflexivo", "emocional", "profundo"]),
                        "potencial_engajamento": random.randint(6, 10),
                        "formatos_recomendados": random.sample(["post_instagram", "story", "carrossel", "reels"], 2),
                        "pergunta_engajadora": random.choice([
                            "O que essa reflexão desperta em você?",
                            "Já viveu algo similar?",
                            "Compartilhe sua opinião nos comentários!",
                            "O que você faria nessa situação?"
                        ]),
                        "hashtags_sugeridas": ["#Literatura", "#Escritora", "#Reflexão", "#Livros"]
                    })
        
        return {
            "trechos_selecionados": trechos_selecionados,
            "temas_principais": ["Literatura", "Reflexão", "Crescimento", "Emoções", "Narrativa"],
            "frases_instagramaveis": [
                "Há silêncios que falam mais que palavras.",
                "A vida é feita de encontros e desencontros.",
                "Cada página é uma nova descoberta."
            ]
        }

class PostDesigner:
    @staticmethod
    def criar_design_post(trecho, identidade):
        """Cria design visual para o post"""
        cores = identidade.get("cores_primarias", ["#8B7355", "#F5F1E8", "#5D4037"])
        fontes = identidade.get("fontes", {"titulo": "Cormorant Garamond", "texto": "Inter"})
        
        return {
            "id": f"post_{datetime.now().timestamp()}",
            "trecho_original": trecho,
            "design": {
                "plataforma": trecho.get("formatos_recomendados", ["post_instagram"])[0],
                "copy": PostDesigner._formatar_copy(trecho, identidade),
                "hashtags": trecho.get("hashtags_sugeridas", []) + ["#AlmaDeEscritora"],
                "visual": {
                    "cor_fundo": cores[1],
                    "cor_texto": cores[2],
                    "cor_destaque": cores[0],
                    "fonte_titulo": fontes["titulo"],
                    "fonte_texto": fontes["texto"]
                },
                "preview_html": PostDesigner._gerar_html_preview(trecho, identidade)
            },
            "criado_em": datetime.now().isoformat()
        }
    
    @staticmethod
    def _formatar_copy(trecho, identidade):
        texto = trecho['texto']
        pergunta = trecho.get('pergunta_engajadora', '')
        
        copy = f"{texto}"
        if pergunta:
            copy += f"\\n\\n{pergunta}"
        
        # Adiciona redes sociais se existirem
        redes_sociais = identidade.get("redes_sociais", {})
        if redes_sociais:
            copy += f"\\n\\n---"
            if redes_sociais.get("instagram"):
                copy += f"\\n📱 Instagram: {redes_sociais['instagram']}"
            if redes_sociais.get("site"):
                copy += f"\\n🌐 Site: {redes_sociais['site']}"
        
        copy += f"\\n\\n— {identidade.get('nome_marca', 'Escritora')}"
        
        return copy
    
    @staticmethod
    def _gerar_html_preview(trecho, identidade):
        cores = identidade.get("cores_primarias", ["#8B7355", "#F5F1E8", "#5D4037"])
        fontes = identidade.get("fontes", {"titulo": "Cormorant Garamond", "texto": "Inter"})
        redes_sociais = identidade.get("redes_sociais", {})
        
        redes_html = ""
        if redes_sociais:
            redes_html = "<div style='margin-top: 15px; padding-top: 15px; border-top: 1px solid " + cores[0] + ";'>"
            if redes_sociais.get("instagram"):
                redes_html += f"<div>📱 {redes_sociais['instagram']}</div>"
            if redes_sociais.get("site"):
                redes_html += f"<div>🌐 {redes_sociais['site']}</div>"
            redes_html += "</div>"
        
        return f"""
        <div style="
            background: {cores[1]}; 
            padding: 25px; 
            border-radius: 12px;
            border-left: 5px solid {cores[0]};
            font-family: {fontes['texto']}, sans-serif;
            max-width: 500px;
            margin: 20px auto;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        ">
            <div style="text-align: center; margin-bottom: 15px;">
                <div style="
                    background: {cores[0]};
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    display: inline-block;
                    font-size: 0.9em;
                    font-family: {fontes['titulo']}, serif;
                ">
                    {identidade.get('nome_marca', 'Minha Marca')}
                </div>
            </div>
            
            <h3 style="
                color: {cores[0]};
                font-family: {fontes['titulo']}, serif;
                margin-bottom: 20px;
                text-align: center;
                font-size: 1.4em;
            ">
                {trecho.get('tema', 'Reflexão')}
            </h3>
            
            <p style="
                color: {cores[2]};
                line-height: 1.7;
                font-size: 1.1em;
                text-align: center;
                margin-bottom: 20px;
                font-style: italic;
            ">
                "{trecho['texto']}"
            </p>
            
            <div style="
                color: {cores[0]};
                font-size: 0.9em;
                text-align: center;
                margin-bottom: 15px;
            ">
                {trecho.get('pergunta_engajadora', 'O que achou?')}
            </div>
            
            {redes_html}
            
            <div style="
                border-top: 1px solid {cores[0]};
                padding-top: 15px;
                text-align: center;
            ">
                <p style="
                    color: {cores[0]};
                    font-size: 0.8em;
                    margin: 0;
                ">
                    {', '.join(trecho.get('hashtags_sugeridas', ['#Literatura', '#Escritora'])[:3])}
                </p>
            </div>
        </div>
        """

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

@app.get("/posts-gerados", response_class=HTMLResponse)
async def posts_gerados(request: Request):
    return templates.TemplateResponse("posts_gerados.html", {"request": request})

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
            "texto_completo": texto[:1000],
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
        "total_temas": 5
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
            "redes_sociais": perfil_data.get("redes_sociais", {}),
            "created_at": datetime.now().isoformat()
        }
        
        usuarios[user_id] = perfil
        
        # CSS personalizado
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

@app.post("/api/posts/gerar-posts")
async def gerar_posts_automaticos():
    try:
        # Encontrar identidade do usuário
        user_id = list(usuarios.keys())[0] if usuarios else "default_user"
        identidade = usuarios.get(user_id, {})
        
        if not identidade:
            return JSONResponse({"success": False, "error": "Crie uma identidade primeiro"}, status_code=400)
        
        # Coletar todos os trechos
        todos_trechos = []
        for livro_titulo, dados in biblioteca.items():
            if "trechos_extraidos" in dados:
                for trecho in dados["trechos_extraidos"]:
                    trecho["fonte_livro"] = livro_titulo
                    todos_trechos.append(trecho)
        
        if not todos_trechos:
            return JSONResponse({"success": False, "error": "Nenhum trecho disponível. Carregue um livro primeiro."}, status_code=400)
        
        # Gerar posts para cada trecho
        posts_gerados[user_id] = []
        designer = PostDesigner()
        
        for trecho in todos_trechos[:10]:  # Limitar a 10 posts
            post = designer.criar_design_post(trecho, identidade)
            posts_gerados[user_id].append(post)
        
        return JSONResponse({
            "success": True,
            "message": f"{len(posts_gerados[user_id])} posts gerados com sucesso!",
            "total_posts": len(posts_gerados[user_id])
        })
        
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.get("/api/posts/listar")
async def listar_posts_gerados():
    user_id = list(usuarios.keys())[0] if usuarios else "default_user"
    posts = posts_gerados.get(user_id, [])
    
    return JSONResponse({
        "posts": posts,
        "total": len(posts)
    })

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Alma de Escritora", "version": "2.1.0"}

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
        f.write(novo_conteudo)

def criar_template_posts():
    """Cria template para visualizar posts gerados"""
    print("📝 Criando template de posts...")
    
    conteudo = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Posts Gerados - Alma de Escritora</title>
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
                    <a href="/dashboard-escritora" class="nav-link">Dashboard</a>
                    <a href="/identity-setup" class="nav-link">Identidade</a>
                    <a href="/posts-gerados" class="nav-link active">Posts Gerados</a>
                </nav>
            </div>
        </div>
    </header>

    <main class="dashboard-main">
        <div class="container">
            <section class="welcome-section">
                <h1>📱 Seus Posts Prontos! ✨</h1>
                <p class="welcome-subtitle">Designs personalizados com sua identidade visual</p>
            </section>

            <div class="posts-actions">
                <button class="btn btn-primary" onclick="gerarPosts()">
                    🎨 Gerar Novos Posts
                </button>
                <button class="btn btn-secondary" onclick="carregarPosts()">
                    🔄 Recarregar Posts
                </button>
            </div>

            <div id="postsStatus" class="status-info">
                <p>Clique em "Gerar Novos Posts" para criar designs personalizados.</p>
            </div>

            <div id="postsContainer" class="posts-grid">
                <!-- Posts serão carregados aqui -->
            </div>

            <div id="loadingPosts" class="loading" style="display: none;">
                <div class="loading-spinner"></div>
                <p>Gerando seus posts personalizados...</p>
            </div>
        </div>
    </main>

    <script>
        class PostsManager {
            constructor() {
                this.init();
            }

            init() {
                console.log('📱 Posts Manager inicializado');
            }

            async gerarPosts() {
                const loading = document.getElementById('loadingPosts');
                const status = document.getElementById('postsStatus');
                
                try {
                    loading.style.display = 'block';
                    status.innerHTML = '<p>🔄 Criando designs personalizados...</p>';

                    const response = await fetch('/api/posts/gerar-posts', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    });

                    const data = await response.json();

                    if (data.success) {
                        status.innerHTML = `<p>✅ ${data.message}</p>`;
                        this.carregarPosts();
                    } else {
                        status.innerHTML = `<p>❌ ${data.error}</p>`;
                    }

                } catch (error) {
                    console.error('Erro:', error);
                    status.innerHTML = '<p>❌ Erro ao gerar posts</p>';
                } finally {
                    loading.style.display = 'none';
                }
            }

            async carregarPosts() {
                const container = document.getElementById('postsContainer');
                const status = document.getElementById('postsStatus');
                
                try {
                    const response = await fetch('/api/posts/listar');
                    const data = await response.json();

                    if (data.posts && data.posts.length > 0) {
                        status.innerHTML = `<p>📊 ${data.total} posts gerados</p>`;
                        this.renderizarPosts(data.posts, container);
                    } else {
                        status.innerHTML = '<p>📝 Nenhum post gerado ainda. Clique em "Gerar Novos Posts".</p>';
                        container.innerHTML = '';
                    }

                } catch (error) {
                    console.error('Erro:', error);
                    status.innerHTML = '<p>❌ Erro ao carregar posts</p>';
                }
            }

            renderizarPosts(posts, container) {
                let html = '';

                posts.forEach((post, index) => {
                    html += `
                        <div class="post-card">
                            <div class="post-header">
                                <h3>Post ${index + 1} - ${post.design.plataforma}</h3>
                                <span class="post-date">${new Date(post.criado_em).toLocaleDateString('pt-BR')}</span>
                            </div>
                            
                            <div class="post-preview">
                                ${post.design.preview_html}
                            </div>

                            <div class="post-actions">
                                <button class="btn btn-small btn-primary" onclick="copiarTexto('${post.design.copy.replace(/'/g, "\\'")}')">
                                    📋 Copiar Texto
                                </button>
                                <button class="btn btn-small btn-secondary" onclick="verDetalhesPost(${index})">
                                    🔍 Detalhes
                                </button>
                            </div>

                            <div class="post-metadata">
                                <small><strong>Fonte:</strong> ${post.trecho_original.fonte_livro}</small>
                                <small><strong>Tema:</strong> ${post.trecho_original.tema}</small>
                                <small><strong>Engajamento:</strong> ⭐ ${post.trecho_original.potencial_engajamento}/10</small>
                            </div>
                        </div>
                    `;
                });

                container.innerHTML = html;
            }
        }

        // Funções globais
        function gerarPosts() {
            window.postsManager.gerarPosts();
        }

        function carregarPosts() {
            window.postsManager.carregarPosts();
        }

        function copiarTexto(texto) {
            navigator.clipboard.writeText(texto).then(() => {
                alert('✅ Texto copiado para a área de transferência!');
            }).catch(err => {
                console.error('Erro ao copiar:', err);
                alert('❌ Erro ao copiar texto');
            });
        }

        function verDetalhesPost(index) {
            // Em uma versão futura, poderia abrir um modal com mais detalhes
            alert(`Detalhes do Post ${index + 1}\\n\\nEm desenvolvimento: Modal com análise completa do post.`);
        }

        // Inicialização
        document.addEventListener('DOMContentLoaded', function() {
            window.postsManager = new PostsManager();
            carregarPosts(); // Carrega posts existentes ao abrir a página
        });
    </script>

    <style>
        .posts-actions {
            display: flex;
            gap: 1rem;
            margin: 2rem 0;
            flex-wrap: wrap;
        }

        .posts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }

        .post-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 1px solid var(--alma-borda);
        }

        .post-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--alma-borda);
        }

        .post-header h3 {
            color: var(--alma-primaria);
            margin: 0;
        }

        .post-date {
            font-size: 0.9em;
            color: var(--alma-texto);
            opacity: 0.7;
        }

        .post-preview {
            margin: 1.5rem 0;
        }

        .post-actions {
            display: flex;
            gap: 0.5rem;
            margin: 1rem 0;
        }

        .post-metadata {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.5rem;
            font-size: 0.8em;
            color: var(--alma-texto);
            opacity: 0.8;
        }

        .status-info {
            background: var(--alma-secundaria);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            text-align: center;
        }

        .btn-small {
            padding: 0.5rem 1rem;
            font-size: 0.8rem;
        }

        @media (max-width: 768px) {
            .posts-grid {
                grid-template-columns: 1fr;
            }
            
            .post-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
            }
        }
    </style>
</body>
</html>'''
    
    with open("frontend/templates/posts_gerados.html", "w", encoding="utf-8") as f:
        f.write(conteudo)

def atualizar_identity_setup():
    """Atualiza o identity setup para incluir redes sociais"""
    print("📝 Atualizando identity setup...")
    
    # Primeiro, vamos ler o conteúdo atual
    with open("frontend/templates/identity_setup.html", "r", encoding="utf-8") as f:
        conteudo_atual = f.read()
    
    # Encontrar a parte do formulário e adicionar redes sociais
    novo_conteudo = conteudo_atual.replace(
        '''<div class="form-group">
                    <label class="form-label" for="estiloPreferido">Estilo Visual Preferido</label>
                    <select id="estiloPreferido" class="form-select">
                        <option value="elegante">Elegante & Sofisticado</option>
                        <option value="minimalista">Minimalista & Clean</option>
                        <option value="criativo">Criativo & Expressivo</option>
                    </select>
                </div>''',
        '''<div class="form-group">
                    <label class="form-label" for="estiloPreferido">Estilo Visual Preferido</label>
                    <select id="estiloPreferido" class="form-select">
                        <option value="elegante">Elegante & Sofisticado</option>
                        <option value="minimalista">Minimalista & Clean</option>
                        <option value="criativo">Criativo & Expressivo</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label">🔗 Suas Redes Sociais (Opcional)</label>
                    <div class="redes-sociais-inputs">
                        <div class="rede-social-item">
                            <label>📷 Instagram</label>
                            <input type="text" id="instagram" class="form-input" placeholder="@seu_usuario">
                        </div>
                        <div class="rede-social-item">
                            <label>🌐 Site/Blog</label>
                            <input type="text" id="site" class="form-input" placeholder="https://seusite.com">
                        </div>
                        <div class="rede-social-item">
                            <label>📘 Facebook</label>
                            <input type="text" id="facebook" class="form-input" placeholder="@seu_usuario">
                        </div>
                        <div class="rede-social-item">
                            <label>🐦 Twitter/X</label>
                            <input type="text" id="twitter" class="form-input" placeholder="@seu_usuario">
                        </div>
                    </div>
                </div>'''
    )
    
    # Adicionar CSS para redes sociais
    if "redes-sociais-inputs" not in novo_conteudo:
        # Encontrar o final do style existente e adicionar novo CSS
        style_posicao = novo_conteudo.find("</style>")
        if style_posicao == -1:
            # Se não tem style, adicionar antes do script
            script_posicao = novo_conteudo.find("<script")
            novo_conteudo = novo_conteudo[:script_posicao] + '''
    <style>
        .redes-sociais-inputs {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
            margin-top: 0.5rem;
        }

        .rede-social-item label {
            display: block;
            margin-bottom: 0.25rem;
            font-weight: 500;
            font-size: 0.9em;
        }

        .rede-social-item input {
            width: 100%;
        }

        @media (min-width: 768px) {
            .redes-sociais-inputs {
                grid-template-columns: 1fr 1fr;
            }
        }
    </style>
''' + novo_conteudo[script_posicao:]
    
    with open("frontend/templates/identity_setup.html", "w", encoding="utf-8") as f:
        f.write(novo_conteudo)

def atualizar_identity_js():
    """Atualiza o JavaScript do identity setup"""
    print("📝 Atualizando identity.js...")
    
    novo_js = '''// Identity Setup
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

        // Coletar redes sociais
        const redesSociais = {
            instagram: document.getElementById('instagram').value,
            site: document.getElementById('site').value,
            facebook: document.getElementById('facebook').value,
            twitter: document.getElementById('twitter').value
        };

        // Remover redes sociais vazias
        Object.keys(redesSociais).forEach(key => {
            if (!redesSociais[key]) {
                delete redesSociais[key];
            }
        });

        if (!nomeMarca.trim()) {
            alert('Informe o nome da sua marca');
            return;
        }

        const identityData = {
            user_id: 'user_' + Date.now(),
            nome_marca: nomeMarca,
            estilo_preferido: estiloPreferido,
            cores_primarias: ["#8B7355", "#F5F1E8", "#5D4037"],
            fontes: {"titulo": "Cormorant Garamond", "texto": "Inter"},
            redes_sociais: redesSociais
        };

        try {
            const response = await fetch('/api/identity/criar-perfil', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(identityData)
            });

            const data = await response.json();

            if (data.success) {
                alert('✅ Identidade salva com sucesso! Suas redes sociais foram adicionadas aos posts.');
                
                // Mostrar preview
                const preview = document.getElementById('identityPreview');
                let redesPreview = '';
                
                if (Object.keys(redesSociais).length > 0) {
                    redesPreview = '<div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #8B7355;"><strong>Redes Sociais:</strong><br>';
                    if (redesSociais.instagram) redesPreview += `📷 ${redesSociais.instagram}<br>`;
                    if (redesSociais.site) redesPreview += `🌐 ${redesSociais.site}<br>`;
                    if (redesSociais.facebook) redesPreview += `📘 ${redesSociais.facebook}<br>`;
                    if (redesSociais.twitter) redesPreview += `🐦 ${redesSociais.twitter}<br>`;
                    redesPreview += '</div>';
                }
                
                preview.innerHTML = `
                    <h3>Preview da Sua Identidade</h3>
                    <div style="background: ${data.perfil.cores_primarias[1]}; padding: 20px; border-radius: 10px; border-left: 5px solid ${data.perfil.cores_primarias[0]};">
                        <h4 style="color: ${data.perfil.cores_primarias[0]};">${data.perfil.nome_marca}</h4>
                        <p style="color: ${data.perfil.cores_primarias[2]};">"Há silêncios que falam mais que palavras..."</p>
                        <small>Estilo: ${data.perfil.estilo_preferido}</small>
                        ${redesPreview}
                    </div>
                `;
                
                setTimeout(() => {
                    window.location.href = '/posts-gerados';
                }, 3000);
            } else {
                alert('❌ Erro: ' + data.error);
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('❌ Erro ao salvar identidade');
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
        f.write(novo_js)

def atualizar_dashboard():
    """Adiciona link para posts gerados no dashboard"""
    print("📝 Atualizando dashboard...")
    
    with open("frontend/templates/dashboard_escritora.html", "r", encoding="utf-8") as f:
        conteudo = f.read()
    
    # Adicionar link no header
    novo_conteudo = conteudo.replace
    
    '''<nav class="header-nav">
                    <a href="/" class="nav-link">Início</a>
                    <a href="/identity-setup" class="nav-link">Identidade</a>
                    <a href="/dashboard-escritora" class="nav-link active">Dashboard</a>
                </nav>''',
'''<nav class="header-nav">
<a href="/" class="nav'''



