# Alma de Escrita

Assistente pessoal de curadoria literária para escritoras. A aplicação ajuda no processo criativo de escrita, oferecendo análise de textos, organização de biblioteca pessoal e apoio à identidade autoral.

## Funcionalidades

- Upload e leitura de arquivos PDF
- Análise de conteúdo com Inteligência Artificial (OpenAI) — identifica temas, sugere frases "instagramáveis", tom e hashtags a partir do texto
- Funciona também **sem chave de API**: nesse caso faz uma análise heurística real do texto enviado (temas por frequência, frases extraídas da própria obra), em vez de resultados fixos
- Biblioteca pessoal para organizar obras e referências
- Curadoria e sugestões voltadas para escritoras
- Interface web com dashboard

## Tecnologias

- **Python 3**
- **FastAPI** — framework web
- **Uvicorn** — servidor ASGI
- **PyPDF2** — leitura de PDFs
- **Jinja2** — templates HTML
- **OpenAI API** — análise inteligente de texto

## Como rodar o projeto

1. Clone o repositório e entre na pasta:

   ```bash
   git clone https://github.com/SEU-USUARIO/alma-de-escrita.git
   cd alma-de-escrita/backend
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # Linux/Mac
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:

   ```bash
   # copie o exemplo e preencha com suas chaves
   copy .env.example .env       # Windows
   cp .env.example .env         # Linux/Mac
   ```

5. Rode a aplicação:

   ```bash
   python main.py
   ```

6. Abra no navegador: `http://localhost:8000`

## Estrutura

```
backend/    -> API, modelos, serviços e rotas
frontend/   -> templates e arquivos estáticos
```

## Observação

O arquivo `.env` com chaves reais não é versionado por segurança. Use o `.env.example` como referência.

---

Projeto desenvolvido por Sinara Santos.
