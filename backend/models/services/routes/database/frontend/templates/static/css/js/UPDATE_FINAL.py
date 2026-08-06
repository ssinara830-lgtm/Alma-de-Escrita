#!/usr/bin/env python3
"""
PERSONALIZAÇÃO FINAL - ALMA DE ESCRITA
Configura domínio e redes sociais da Sinarasantos
"""
import os
import json

def personalizar_sistema():
    """Personaliza todo o sistema para a Sinarasantos"""
    print("🎨 Personalizando sistema para Sinarasantos...")
    
    # 1. Atualizar main.py com suas informações
    atualizar_main_py()
    
    # 2. Atualizar templates com suas informações
    atualizar_templates()
    
    # 3. Criar identidade padrão com suas redes
    criar_identidade_padrao()
    
    print("✅ Sistema personalizado com sucesso!")
    print("🌐 Domínio: http://almadeescrita.com.br/")
    print("📷 Instagram: https://www.instagram.com/sinarasantos.l/")

def atualizar_main_py():
    """Atualiza o main.py com informações da Sinarasantos"""
    print("📝 Atualizando backend...")
    
    with open("backend/main.py", "r", encoding="utf-8") as f:
        conteudo = f.read()
    
    # Atualizar título e descrição
    novo_conteudo = conteudo.replace(
        'title="Alma de Escritora"',
        'title="Alma de Escrita - Sinarasantos"'
    ).replace(
        'description="Assistente pessoal de curadoria literária para escritoras"',
        'description="Sistema de curadoria literária personalizado para Sinarasantos"'
    )
    
    with open("backend/main.py", "w", encoding="utf-8") as f:
        f.write(novo_conteudo)

def atualizar_templates():
    """Atualiza todos os templates com suas informações"""
    
    # 1. Atualizar index.html
    print("📝 Personalizando página inicial...")
    index_content = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alma de Escrita - Sinarasantos</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
</head>
<body class="alma-system">
    <header class="alma-header">
        <div class="container">
            <div class="logo">✍️ Alma de Escrita</div>
            <p class="tagline">Sistema pessoal de curadoria literária de Sinarasantos</p>
            <div class="redes-header">
                <a href="https://www.instagram.com/sinarasantos.l/" target="_blank" class="rede-social">📷 @sinarasantos.l</a>
                <a href="http://almadeescrita.com.br/" target="_blank" class="rede-social">🌐 almadeescrita.com.br</a>
            </div>
        </div>
    </header>

    <section class="hero-section">
        <div class="container">
            <div class="hero-content">
                <h1>Bem-vinda ao seu <span class="text-primary">espaço literário</span> pessoal</h1>
                <p class="hero-description">
                    Transforme seus textos em conteúdo autêntico que conecta, inspira e constrói sua comunidade leitora.
                </p>
                <div class="hero-actions">
                    <a href="/dashboard-escritora" class="btn btn-primary">Acessar Minha Biblioteca</a>
                    <a href="/identity-setup" class="btn btn-secondary">Configurar Identidade</a>
                </div>
            </div>
        </div>
    </section>

    <section class="features-section">
        <div class="container">
            <h2 class="section-title">Seu Sistema Pessoal de Curadoria</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">📚</div>
                    <h3>Biblioteca Pessoal</h3>
                    <p>Carregue seus livros e textos para análise e curadoria automática.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🎨</div>
                    <h3>Identidade Sinarasantos</h3>
                    <p>Conteúdo com sua identidade visual única e personalizada.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📱</div>
                    <h3>Posts Prontos</h3>
                    <p>Designs automáticos para Instagram e outras redes sociais.</p>
                </div>
            </div>
        </div>
    </section>

    <footer class="alma-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-brand">
                    <div class="logo">✍️ Alma de Escrita</div>
                    <p>Sistema pessoal de Sinarasantos</p>
                </div>
                <div class="footer-links">
                    <a href="https://www.instagram.com/sinarasantos.l/" target="_blank">Instagram</a>
                    <a href="http://almadeescrita.com.br/" target="_blank">Site Oficial</a>
                    <a href="/dashboard-escritora">Dashboard</a>
                </div>
            </div>
        </div>
    </footer>

    <script src="/static/js/main.js"></script>

    <style>
        .redes-header {
            margin-top: 1rem;
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }

        .rede-social {
            color: white;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 20px;
            transition: all 0.3s ease;
        }

        .rede-social:hover {
            background: rgba(255,255,255,0.1);
            transform: translateY(-2px);
        }

        .alma-footer {
            background: var(--alma-texto);
            color: white;
            padding: 3rem 0 1rem;
            margin-top: 4rem;
        }

        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 2rem;
        }

        .footer-links {
            display: flex;
            gap: 1.5rem;
        }

        .footer-links a {
            color: white;
            text-decoration: none;
        }

        @media (max-width: 768px) {
            .footer-content {
                flex-direction: column;
                text-align: center;
            }
        }
    </style>
</body>
</html>'''
    
    with open("frontend/templates/index.html", "w", encoding="utf-8") as f:
        f.write(index_content)

    # 2. Atualizar identity-setup com suas informações pré-configuradas
    print("📝 Configurando identidade padrão...")
    identity_content = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Identidade Visual - Alma de Escrita</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
</head>
<body class="alma-system">
    <header class="alma-header">
        <div class="container">
            <div class="logo">✍️ Alma de Escrita</div>
            <p class="tagline">Configure sua identidade visual personalizada</p>
        </div>
    </header>

    <main class="identity-main">
        <div class="container">
            <section class="identity-header">
                <h1>🎨 Sua Identidade Sinarasantos</h1>
                <p class="identity-subtitle">
                    Configure sua identidade visual para todos os conteúdos gerados
                </p>
            </section>

            <div class="setup-step active">
                <h2 class="section-title">👑 Sua Marca Pessoal</h2>
                
                <div class="form-group">
                    <label class="form-label" for="nomeMarca">Nome da Sua Marca</label>
                    <input type="text" id="nomeMarca" class="form-input" value="Sinarasantos" placeholder="Seu nome ou marca">
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="estiloPreferido">Estilo Visual Preferido</label>
                    <select id="estiloPreferido" class="form-select">
                        <option value="elegante">Elegante & Sofisticado</option>
                        <option value="minimalista">Minimalista & Clean</option>
                        <option value="criativo">Criativo & Expressivo</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label">🔗 Suas Redes Sociais</label>
                    <div class="redes-sociais-inputs">
                        <div class="rede-social-item">
                            <label>📷 Instagram</label>
                            <input type="text" id="instagram" class="form-input" value="@sinarasantos.l" placeholder="@seu_usuario">
                        </div>
                        <div class="rede-social-item">
                            <label>🌐 Site Oficial</label>
                            <input type="text" id="site" class="form-input" value="http://almadeescrita.com.br/" placeholder="https://seusite.com">
                        </div>
                        <div class="rede-social-item">
                            <label>📘 Facebook (opcional)</label>
                            <input type="text" id="facebook" class="form-input" placeholder="@seu_usuario">
                        </div>
                        <div class="rede-social-item">
                            <label>🐦 Twitter/X (opcional)</label>
                            <input type="text" id="twitter" class="form-input" placeholder="@seu_usuario">
                        </div>
                    </div>
                </div>
                
                <button class="btn btn-primary" onclick="salvarIdentidade()">
                    💫 Salvar Minha Identidade
                </button>

                <div class="identity-info">
                    <h4>✨ Identidade Pré-configurada</h4>
                    <p>Sua identidade já vem com suas redes sociais configuradas. Você pode personalizar as cores e estilo visual.</p>
                </div>
            </div>

            <div class="preview-container">
                <div id="identityPreview">
                    <p>Preview da sua identidade aparecerá aqui após salvar.</p>
                </div>
            </div>
        </div>
    </main>

    <script src="/static/js/identity.js"></script>

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

        .identity-info {
            background: var(--alma-secundaria);
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 2rem;
            border-left: 4px solid var(--alma-primaria);
        }

        .identity-info h4 {
            color: var(--alma-primaria);
            margin-bottom: 0.5rem;
        }

        @media (min-width: 768px) {
            .redes-sociais-inputs {
                grid-template-columns: 1fr 1fr;
            }
        }
    </style>
</body>
</html>'''
    
    with open("frontend/templates/identity_setup.html", "w", encoding="utf-8") as f:
        f.write(identity_content)

    # 3. Atualizar dashboard com suas informações
    print("📝 Personalizando dashboard...")
    with open("frontend/templates/dashboard_escritora.html", "r", encoding="utf-8") as f:
        dashboard_content = f.read()
    
    # Adicionar redes sociais no header do dashboard
    novo_dashboard = dashboard_content.replace(
        '''<nav class="header-nav">
                    <a href="/" class="nav-link">Início</a>
                    <a href="/identity-setup" class="nav-link">Identidade</a>
                    <a href="/dashboard-escritora" class="nav-link active">Dashboard</a>
                </nav>''',
        '''<nav class="header-nav">
                    <a href="/" class="nav-link">Início</a>
                    <a href="/identity-setup" class="nav-link">Identidade</a>
                    <a href="/dashboard-escritora" class="nav-link active">Dashboard</a>
                    <a href="/posts-gerados" class="nav-link">Posts</a>
                    <a href="https://www.instagram.com/sinarasantos.l/" target="_blank" class="nav-link">📷 Instagram</a>
                </nav>'''
    ).replace(
        '''<h1>Bem-vinda à sua Oficina Literária! ✨</h1>''',
        '''<h1>Bem-vinda à sua Oficina Literária, Sinarasantos! ✨</h1>'''
    )
    
    with open("frontend/templates/dashboard_escritora.html", "w", encoding="utf-8") as f:
        f.write(novo_dashboard)

def criar_identidade_padrao():
    """Cria uma identidade padrão com as informações da Sinarasantos"""
    print("📝 Criando identidade padrão...")
    
    identidade_padrao = {
        "user_id": "sinarasantos",
        "nome_marca": "Sinarasantos",
        "cores_primarias": ["#8B7355", "#F5F1E8", "#5D4037"],
        "fontes": {"titulo": "Cormorant Garamond", "texto": "Inter"},
        "estilo_preferido": "elegante",
        "redes_sociais": {
            "instagram": "@sinarasantos.l",
            "site": "http://almadeescrita.com.br/"
        },
        "created_at": "2024-01-01T00:00:00"
    }
    
    # Salvar em um arquivo para referência
    with open("backend/identidade_sinarasantos.json", "w", encoding="utf-8") as f:
        json.dump(identidade_padrao, f, indent=2, ensure_ascii=False)

def criar_arquivo_deploy():
    """Cria instruções para deploy no domínio"""
    print("📝 Criando instruções de deploy...")
    
    instrucoes = '''# 🌐 DEPLOY - Alma de Escrita
# Domínio: http://almadeescrita.com.br/
# Instagram: https://www.instagram.com/sinarasantos.l/

## 🚀 COMO COLOCAR NO AR:

### OPÇÃO 1: HOSPEDAGEM COMPARTILHADA
1. Contrate uma hospedagem (Hostinger, HostGator, etc.)
2. Acesse o painel de controle (cPanel)
3. Vá em "File Manager" e navegue até public_html
4. Faça upload de TODOS os arquivos do sistema
5. Configure o Python na hospedagem (geralmente em "Setup Python App")
6. Acesse: http://almadeescrita.com.br/

### OPÇÃO 2: VPS (RECOMENDADO)
1. Contrate um VPS (DigitalOcean, Vultr, etc.)
2. Acesse via SSH
3. Instale: git, python, pip
4. Clone/faça upload dos arquivos
5. Execute: 
   cd backend
   pip install -r requirements.txt
   python main.py
6. Configure um domínio no painel do VPS

### OPÇÃO 3: SERVIÇOS DE DEPLOY
- **Railway**: Conecte seu GitHub e faça deploy automático
- **Render**: Similar ao Heroku, gratuito para pequenos projetos
- **PythonAnywhere**: Especializado em Python

## ⚙️ CONFIGURAÇÕES IMPORTANTES:

### No arquivo backend/main.py:
```python
# Alterar para produção
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Ou IP do servidor
        port=80,         # Porta padrão HTTP
        reload=False     # Desativar em produção
    )'''
