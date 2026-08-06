# 🎨 ALMA DE ESCRITORA

**Sistema Completo de Curadoria Literária e Identidade Visual para Escritoras**

> Transforme sua essência literária em conteúdo autêntico que conecta, inspira e constrói comunidade.

## 🚀 Visão Geral

O **Alma de Escritora** é uma plataforma inteligente que ajuda escritoras a:
- **Descobrir** os trechos mais impactantes de suas obras
- **Criar** uma identidade visual única e autoral  
- **Planejar** conteúdo estratégico para redes sociais
- **Conectar** com sua comunidade leitora de forma autêntica

## 📁 Estrutura do Projeto


almadeescrita/
├── 📄 START.py (← Execute este primeiro!)
├── 📁 backend/
│ ├── main.py (Aplicação FastAPI principal)
│ ├── config.py (Configurações e variáveis de ambiente)
│ ├── requirements.txt (Dependências Python)
│ ├── .env (Variáveis de ambiente)
│ ├── 📁 models/
│ │ ├── marca_profile.py (Modelo de identidade visual)
│ │ └── user.py (Modelo de usuário)
│ ├── 📁 services/
│ │ ├── biblioteca_pessoal.py (Gerenciamento de livros)
│ │ ├── curadoria_escritora.py (Criação de planos de conteúdo)
│ │ ├── identity_applier.py (Aplicação de identidade visual)
│ │ ├── css_generator.py (Geração de CSS personalizado)
│ │ ├── pdf_processor.py (Processamento de PDFs)
│ │ ├── ai_analyzer.py (Análise de IA com OpenAI)
│ │ └── template_manager.py (Gerenciamento de templates)
│ ├── 📁 routes/
│ │ ├── escritora_routes.py (Endpoints para escritora)
│ │ ├── identity_routes.py (Endpoints para identidade)
│ │ └── content_routes.py (Endpoints para conteúdo)
│ └── 📁 database/
│ └── database.py (Configuração do banco SQLite)
├── 📁 frontend/
│ ├── 📁 templates/
│ │ ├── index.html (Página inicial)
│ │ ├── dashboard_escritora.html (Dashboard principal)
│ │ └── identity_setup.html (Configuração de identidade)
│ └── 📁 static/
│ ├── 📁 css/
│ │ └── style.css (Estilos principais)
│ └── 📁 js/
│ ├── main.js (JavaScript geral)
│ ├── dashboard_escritora.js (Dashboard functions)
│ └── identity.js (Identity setup functions)
└── 📄 README.md (Esta documentação)
text
## 🛠️ Instalação e Configuração

### 1. Executar o Inicializador Automático

```bash
python START.py

