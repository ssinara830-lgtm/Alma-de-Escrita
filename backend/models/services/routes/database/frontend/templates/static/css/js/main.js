// ALMA DE ESCRITORA - Main JavaScript
// Funcionalidades gerais e inicialização do sistema

class AlmaDeEscritora {
    constructor() {
        this.init();
    }

    init() {
        console.log('🎨 Alma de Escritora - Sistema inicializado');
        this.setupEventListeners();
        this.checkHealth();
    }

    setupEventListeners() {
        // Smooth scrolling para links internos
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Animação de entrada para elementos
        this.setupScrollAnimations();
    }

    setupScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        // Observar elementos para animação
        document.querySelectorAll('.feature-card, .process-step, .action-card').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });
    }

    async checkHealth() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            
            if (data.status === 'healthy') {
                console.log('✅ Sistema conectado e saudável');
            } else {
                console.warn('⚠️ Sistema com problemas de saúde');
            }
        } catch (error) {
            console.error('❌ Erro ao verificar saúde do sistema:', error);
        }
    }

    // Utilitários de formatação
    formatarData(data) {
        return new Date(data).toLocaleDateString('pt-BR');
    }

    formatarNumero(numero) {
        return new Intl.NumberFormat('pt-BR').format(numero);
    }

    // Gerenciamento de notificações
    mostrarNotificacao(mensagem, tipo = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${tipo}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${mensagem}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;

        // Estilos da notificação
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${tipo === 'error' ? '#f56565' : tipo === 'success' ? '#48bb78' : '#4299e1'};
            color: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            max-width: 400px;
            animation: slideInRight 0.3s ease;
        `;

        document.body.appendChild(notification);

        // Fechar notificação
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.onclick = () => this.fecharNotificacao(notification);

        // Auto-remover após 5 segundos
        setTimeout(() => this.fecharNotificacao(notification), 5000);
    }

    fecharNotificacao(notification) {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }

    // Animação CSS para notificações
    injectNotificationStyles() {
        const styles = `
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOutRight {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
            
            .notification-close {
                background: none;
                border: none;
                color: white;
                font-size: 1.2rem;
                cursor: pointer;
                margin-left: 1rem;
            }
            
            .notification-content {
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
        `;
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
    }

    // Upload de arquivos
    setupFileUpload(uploadArea, fileInput, onFileSelect) {
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#8B7355';
            uploadArea.style.background = 'rgba(139, 115, 85, 0.1)';
        });

        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#8B7355';
            uploadArea.style.background = 'rgba(139, 115, 85, 0.05)';
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#8B7355';
            uploadArea.style.background = 'rgba(139, 115, 85, 0.05)';
            
            const files = e.dataTransfer.files;
            if (files.length > 0 && files[0].type === 'application/pdf') {
                fileInput.files = files;
                onFileSelect(files[0]);
            } else {
                this.mostrarNotificacao('Por favor, selecione apenas arquivos PDF.', 'error');
            }
        });

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                onFileSelect(e.target.files[0]);
            }
        });
    }

    // Validação de formulários
    validarEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }

    validarTexto(texto, minLength = 1) {
        return texto && texto.trim().length >= minLength;
    }

    // API Utilities
    async fazerRequisicao(url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Erro na requisição:', error);
            this.mostrarNotificacao('Erro de conexão. Tente novamente.', 'error');
            throw error;
        }
    }

    // Gerenciamento de estado
    salvarNoLocalStorage(chave, dados) {
        try {
            localStorage.setItem(`alma_${chave}`, JSON.stringify(dados));
        } catch (error) {
            console.error('Erro ao salvar no localStorage:', error);
        }
    }

    carregarDoLocalStorage(chave) {
        try {
            const dados = localStorage.getItem(`alma_${chave}`);
            return dados ? JSON.parse(dados) : null;
        } catch (error) {
            console.error('Erro ao carregar do localStorage:', error);
            return null;
        }
    }

    removerDoLocalStorage(chave) {
        try {
            localStorage.removeItem(`alma_${chave}`);
        } catch (error) {
            console.error('Erro ao remover do localStorage:', error);
        }
    }
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    window.almaApp = new AlmaDeEscritora();
    window.almaApp.injectNotificationStyles();
});

// Utilitários globais
function mostrarCarregamento(elemento) {
    elemento.style.display = 'block';
}

function esconderCarregamento(elemento) {
    elemento.style.display = 'none';
}

function formatarTexto(texto, maxLength = 200) {
    if (texto.length <= maxLength) return texto;
    return texto.substring(0, maxLength) + '...';
}

function copiarParaAreaTransferencia(texto) {
    navigator.clipboard.writeText(texto).then(() => {
        window.almaApp.mostrarNotificacao('Copiado para a área de transferência!', 'success');
    }).catch(err => {
        console.error('Erro ao copiar:', err);
        window.almaApp.mostrarNotificacao('Erro ao copiar texto.', 'error');
    });
}
Crie frontend/static/js/dashboard_escritora.js:
javascript
// Dashboard da Escritora - Funcionalidades específicas

class DashboardEscritora {
    constructor() {
        this.biblioteca = [];
        this.trechos = [];
        this.init();
    }

    init() {
        console.log('📚 Dashboard da Escritora inicializado');
        this.carregarBiblioteca();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Upload de arquivos
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        
        if (uploadArea && fileInput) {
            window.almaApp.setupFileUpload(uploadArea, fileInput, (file) => {
                this.mostrarInfoArquivo(file);
            });
        }

        // Busca de trechos
        const buscaInput = document.getElementById('buscaTrechos');
        if (buscaInput) {
            buscaInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.buscarTrechos();
                }
            });
        }
    }

    mostrarInfoArquivo(file) {
        const uploadArea = document.getElementById('uploadArea');
        uploadArea.innerHTML = `
            <div class="file-info">
                <div class="file-icon">📄</div>
                <h4>${file.name}</h4>
                <p>Tamanho: ${this.formatarTamanhoArquivo(file.size)}</p>
                <button class="btn btn-secondary" onclick="trocarArquivo()">Trocar Arquivo</button>
            </div>
        `;
    }

    formatarTamanhoArquivo(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    trocarArquivo() {
        const uploadArea = document.getElementById('uploadArea');
        uploadArea.innerHTML = `
            <div class="upload-icon">📄</div>
            <h3>Arraste seu livro aqui</h3>
            <p>Formatos suportados: PDF</p>
            <input type="file" id="fileInput" accept=".pdf" style="display: none;">
            <button class="btn btn-primary" onclick="document.getElementById('fileInput').click()">
                Selecionar Arquivo
            </button>
        `;
        this.setupEventListeners();
    }

    // Seções do Dashboard
    showSection(sectionId) {
        // Esconder todas as seções
        document.querySelectorAll('.content-section').forEach(section => {
            section.style.display = 'none';
        });
        
        // Mostrar seção específica
        const section = document.getElementById(sectionId);
        if (section) {
            section.style.display = 'block';
            
            // Carregar conteúdo específico da seção
            switch(sectionId) {
                case 'bibliotecaSection':
                    this.carregarBibliotecaCompleta();
                    break;
                case 'trechosSection':
                    this.carregarTrechosAleatorios();
                    break;
                case 'curadoriaSection':
                    this.carregarCuradoria();
                    break;
            }
        }
    }

    hideSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.style.display = 'none';
        }
    }

    // API: Carregar Livro
    async carregarLivro() {
        const fileInput = document.getElementById('fileInput');
        const tituloInput = document.getElementById('tituloLivro');
        const sinopseInput = document.getElementById('sinopseLivro');
        const loadingElement = document.getElementById('uploadLoading');

        if (!fileInput.files.length) {
            window.almaApp.mostrarNotificacao('Por favor, selecione um arquivo PDF.', 'error');
            return;
        }

        if (!tituloInput.value.trim()) {
            window.almaApp.mostrarNotificacao('Por favor, informe o título do livro.', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('titulo_livro', tituloInput.value.trim());
        formData.append('sinopse', sinopseInput.value.trim());

        try {
            mostrarCarregamento(loadingElement);

            const response = await fetch('/api/escritora/carregar-livro', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                window.almaApp.mostrarNotificacao(data.message, 'success');
                
                // Resetar formulário
                fileInput.value = '';
                tituloInput.value = '';
                sinopseInput.value = '';
                this.trocarArquivo();
                
                // Atualizar biblioteca
                this.carregarBiblioteca();
                
            } else {
                throw new Error(data.detail || 'Erro ao carregar livro');
            }

        } catch (error) {
            console.error('Erro:', error);
            window.almaApp.mostrarNotificacao(error.message, 'error');
        } finally {
            esconderCarregamento(loadingElement);
        }
    }

    // API: Carregar Biblioteca
    async carregarBiblioteca() {
        try {
            const response = await window.almaApp.fazerRequisicao('/api/escritora/biblioteca');
            
            if (response.biblioteca) {
                this.biblioteca = response.biblioteca;
                this.atualizarEstatisticas(response.estatisticas);
            }
        } catch (error) {
            console.error('Erro ao carregar biblioteca:', error);
        }
    }

    async carregarBibliotecaCompleta() {
        await this.carregarBiblioteca();
        this.renderizarBiblioteca();
    }

    atualizarEstatisticas(estatisticas) {
        document.getElementById('totalLivros').textContent = estatisticas.total_livros;
        document.getElementById('totalTrechos').textContent = estatisticas.total_trechos;
        document.getElementById('totalTemas').textContent = estatisticas.total_temas;
    }

    renderizarBiblioteca() {
        const container = document.getElementById('bibliotecaContent');
        
        if (Object.keys(this.biblioteca).length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">📚</div>
                    <h3>Sua biblioteca está vazia</h3>
                    <p>Comece carregando seu primeiro livro para ver a mágica acontecer!</p>
                    <button class="btn btn-primary" onclick="showSection('uploadSection')">
                        Carregar Primeiro Livro
                    </button>
                </div>
            `;
            return;
        }

        let html = '<div class="biblioteca-grid">';
        
        for (const [titulo, dados] of Object.entries(this.biblioteca)) {
            html += `
                <div class="livro-card">
                    <div class="livro-header">
                        <h3>${titulo}</h3>
                        <span class="livro-status ${dados.status}">${dados.status}</span>
                    </div>
                    
                    ${dados.sinopse ? `<p class="livro-sinopse">${dados.sinopse}</p>` : ''}
                    
                    <div class="livro-stats">
                        <span>📊 ${dados.metadados.total_palavras} palavras</span>
                        <span>🎯 ${dados.trechos_extraidos.length} trechos</span>
                        <span>🏷️ ${dados.analise.temas_principais.length} temas</span>
                    </div>
                    
                    <div class="livro-actions">
                        <button class="btn btn-small btn-primary" onclick="verTrechosLivro('${titulo}')">
                            Ver Trechos
                        </button>
                        <button class="btn btn-small btn-secondary" onclick="gerarSequenciaLancamento('${titulo}')">
                            Lançamento
                        </button>
                        <button class="btn btn-small btn-secondary" onclick="removerLivro('${titulo}')">
                            Remover
                        </button>
                    </div>
                    
                    <div class="livro-temas">
                        ${dados.analise.temas_principais.slice(0, 3).map(tema => 
                            `<span class="tema-tag">${tema}</span>`
                        ).join('')}
                    </div>
                </div>
            `;
        }
        
        html += '</div>';
        container.innerHTML = html;
    }

    // API: Trechos Aleatórios
    async carregarTrechosAleatorios() {
        try {
            const response = await window.almaApp.fazerRequisicao('/api/escritora/trechos-aleatorios?quantidade=6');
            this.trechos = response.trechos;
            this.renderizarTrechos();
        } catch (error) {
            console.error('Erro ao carregar trechos:', error);
            window.almaApp.mostrarNotificacao('Erro ao carregar trechos.', 'error');
        }
    }

    // API: Buscar Trechos
    async buscarTrechos() {
        const termo = document.getElementById('buscaTrechos').value.trim();
        
        if (!termo) {
            this.carregarTrechosAleatorios();
            return;
        }

        try {
            const response = await window.almaApp.fazerRequisicao(`/api/escritora/buscar-trechos?tema=${encodeURIComponent(termo)}`);
            this.trechos = response.trechos;
            this.renderizarTrechos();
            
            if (response.trechos.length === 0) {
                window.almaApp.mostrarNotificacao(`Nenhum trecho encontrado para "${termo}"`, 'info');
            }
        } catch (error) {
            console.error('Erro na busca:', error);
        }
    }

    renderizarTrechos() {
        const container = document.getElementById('trechosGrid');
        
        if (this.trechos.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">💫</div>
                    <h3>Nenhum trecho encontrado</h3>
                    <p>Tente buscar por outro tema ou carregar mais livros.</p>
                </div>
            `;
            return;
        }

        let html = '';
        
        this.trechos.forEach(trecho => {
            html += `
                <div class="trecho-card">
                    <div class="trecho-texto">
                        "${trecho.texto}"
                    </div>
                    
                    <div class="trecho-metadata">
                        <span class="trecho-tema">${trecho.tema}</span>
                        <span class="trecho-engajamento">⭐ ${trecho.potencial_engajamento}/10</span>
                    </div>
                    
                    <div class="trecho-livro">
                        <small>Fonte: ${trecho.fonte_livro || 'Livro'}</small>
                    </div>
                    
                    <div class="trecho-acoes">
                        <button class="btn btn-small btn-primary" onclick="previewConteudo(${JSON.stringify(trecho).replace(/"/g, '&quot;')})">
                            Visualizar
                        </button>
                        <button class="btn btn-small btn-secondary" onclick="copiarTrecho('${trecho.texto.replace(/'/g, "\\'")}')">
                            Copiar
                        </button>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    }

    // API: Gerar Plano Mensal
    async gerarPlanoMensal() {
        const loadingElement = document.getElementById('curadoriaLoading');
        const container = document.getElementById('curadoriaContent');

        try {
            mostrarCarregamento(loadingElement);

            const response = await window.almaApp.fazerRequisicao('/api/escritora/plano-mensal', {
                method: 'POST'
            });

            if (response.success) {
                this.renderizarPlanoMensal(response.plano_mensal, container);
                window.almaApp.mostrarNotificacao('Plano mensal gerado com sucesso!', 'success');
            }

        } catch (error) {
            console.error('Erro:', error);
            window.almaApp.mostrarNotificacao('Erro ao gerar plano mensal.', 'error');
        } finally {
            esconderCarregamento(loadingElement);
        }
    }

    renderizarPlanoMensal(plano, container) {
        let html = `
            <div class="plano-mensal">
                <div class="plano-header">
                    <h3>📅 Plano de Conteúdo - ${plano.mes}</h3>
                    <p>${plano.total_posts} posts programados • ${plano.livros_utilizados.length} livros utilizados</p>
                </div>
                
                <div class="estrategia-geral">
                    <h4>🎯 Estratégia do Mês</h4>
                    <p><strong>Objetivo:</strong> ${plano.estrategia_geral.objetivo_principal}</p>
                    <p><strong>Abordagem:</strong> ${plano.estrategia_geral.abordagem}</p>
                    <p><strong>Tom de Voz:</strong> ${plano.estrategia_geral.tom_de_voz}</p>
                </div>
        `;

        for (const [semanaNum, semana] of Object.entries(plano.calendario)) {
            html += `
                <div class="semana-plano">
                    <h4>📋 Semana ${semanaNum}: ${semana.tema_principal}</h4>
                    <p><em>${semana.objetivo}</em></p>
                    
                    <div class="dias-semana">
            `;

            for (const [data, conteudo] of Object.entries(semana.dias)) {
                html += `
                    <div class="dia-plano">
                        <div class="dia-header">
                            <strong>${new Date(data).toLocaleDateString('pt-BR')}</strong>
                            <span class="horario">${conteudo.horario_sugerido}</span>
                        </div>
                        <div class="trecho-dia">${formatarTexto(conteudo.trecho_original.texto, 100)}</div>
                        <div class="formato-dia">📱 ${conteudo.formato_recomendado}</div>
                        <button class="btn btn-small btn-primary" onclick="previewConteudoPronto(${JSON.stringify(conteudo).replace(/"/g, '&quot;')})">
                            Ver Post
                        </button>
                    </div>
                `;
            }

            html += `
                    </div>
                </div>
            `;
        }

        html += '</div>';
        container.innerHTML = html;
    }

    // API: Sequência de Lançamento
    async gerarSequenciaLancamento(livroTitulo = null) {
        if (!livroTitulo) {
            // Pedir para selecionar um livro
            if (Object.keys(this.biblioteca).length === 0) {
                window.almaApp.mostrarNotificacao('Carregue um livro primeiro.', 'error');
                return;
            }
            
            // Aqui poderia ter um seletor de livros
            livroTitulo = Object.keys(this.biblioteca)[0];
        }

        const loadingElement = document.getElementById('curadoriaLoading');
        const container = document.getElementById('curadoriaContent');

        try {
            mostrarCarregamento(loadingElement);

            const response = await window.almaApp.fazerRequisicao('/api/escritora/sequencia-lancamento', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ livro_titulo: livroTitulo })
            });

            if (response.success) {
                this.renderizarSequenciaLancamento(response.sequencia_lancamento, container);
                window.almaApp.mostrarNotificacao('Sequência de lançamento criada!', 'success');
            }

        } catch (error) {
            console.error('Erro:', error);
            window.almaApp.mostrarNotificacao('Erro ao gerar sequência.', 'error');
        } finally {
            esconderCarregamento(loadingElement);
        }
    }

    renderizarSequenciaLancamento(sequencia, container) {
        let html = `
            <div class="sequencia-lancamento">
                <h3>🚀 Sequência de Lançamento</h3>
                
                <div class="fase-lancamento">
                    <h4>📢 Pré-Lançamento (7 dias antes)</h4>
        `;

        sequencia.pre_lancamento.forEach(dia => {
            html += `
                <div class="dia-lancamento">
                    <strong>${dia.dia}</strong>: ${dia.conteudo}
                    <br><small>🎯 ${dia.objetivo}</small>
                </div>
            `;
        });

        html += `
                </div>
                
                <div class="fase-lancamento">
                    <h4>🎉 Dia do Lançamento</h4>
        `;

        sequencia.lancamento.conteudos.forEach(conteudo => {
            html += `
                <div class="dia-lancamento">
                    <strong>${conteudo.horario}</strong> - ${conteudo.tipo}: ${conteudo.texto}
                    <br><small>📢 ${conteudo.call_to_action}</small>
                </div>
            `;
        });

        html += `
                </div>
                
                <div class="fase-lancamento">
                    <h4>✨ Pós-Lançamento (7 dias depois)</h4>
        `;

        sequencia.pos_lancamento.forEach(dia => {
            html += `
                <div class="dia-lancamento">
                    <strong>${dia.dia}</strong>: ${formatarTexto(dia.conteudo, 80)}
                    <br><small>🎯 ${dia.objetivo}</small>
                </div>
            `;
        });

        html += '</div></div>';
        container.innerHTML = html;
    }

    // Funções auxiliares
    carregarCuradoria() {
        // Placeholder - poderia carregar curadoria salva
        document.getElementById('curadoriaContent').innerHTML = `
            <div class="curadoria-info">
                <p>Gere um plano mensal de conteúdo ou uma sequência especial para lançamento.</p>
            </div>
        `;
    }
}

// Funções globais para o dashboard
function showSection(sectionId) {
    window.dashboardApp.showSection(sectionId);
}

function hideSection(sectionId) {
    window.dashboardApp.hideSection(sectionId);
}

function carregarLivro() {
    window.dashboardApp.carregarLivro();
}

function carregarTrechosAleatorios() {
    window.dashboardApp.carregarTrechosAleatorios();
}

function buscarTrechos() {
    window.dashboardApp.buscarTrechos();
}

function gerarPlanoMensal() {
    window.dashboardApp.gerarPlanoMensal();
}

function gerarSequenciaLancamento(livroTitulo = null) {
    window.dashboardApp.gerarSequenciaLancamento(livroTitulo);
}

function previewConteudo(trecho) {
    const modal = document.getElementById('previewModal');
    const content = document.getElementById('previewContent');
    
    content.innerHTML = `
        <div class="preview-header">
            <h4>${trecho.tema}</h4>
            <p>Potencial de engajamento: ⭐ ${trecho.potencial_engajamento}/10</p>
        </div>
        
        <div class="preview-texto">
            <blockquote>${trecho.texto}</blockquote>
        </div>
        
        <div class="preview-metadata">
            <p><strong>Formato recomendado:</strong> ${trecho.formatos_recomendados.join(', ')}</p>
            <p><strong>Pergunta engajadora:</strong> ${trecho.pergunta_engajadora}</p>
            <p><strong>Hashtags:</strong> ${trecho.hashtags_sugeridas.join(' ')}</p>
            <p><strong>Dica visual:</strong> ${trecho.dica_visual}</p>
        </div>
        
        <div class="preview-actions">
            <button class="btn btn-primary" onclick="aplicarIdentidade(${JSON.stringify(trecho).replace(/"/g, '&quot;')})">
                🎨 Aplicar Minha Identidade
            </button>
            <button class="btn btn-secondary" onclick="copiarTrecho('${trecho.texto.replace(/'/g, "\\'")}')">
                📋 Copiar Trecho
            </button>
        </div>
    `;
    
    modal.style.display = 'flex';
}

function previewConteudoPronto(conteudoPronto) {
    const modal = document.getElementById('previewModal');
    const content = document.getElementById('previewContent');
    
    content.innerHTML = `
        <div class="preview-header">
            <h4>Post Pronto - ${conteudoPronto.formato_recomendado}</h4>
            <p>📅 ${conteudoPronto.horario_sugerido}</p>
        </div>
        
        <div class="preview-post-pronto">
            ${conteudoPronto.conteudo_pronto?.preview_html || 'Preview não disponível'}
        </div>
        
        <div class="preview-metadata">
            <p><strong>Hashtags sugeridas:</strong> ${conteudoPronto.hashtags_sugeridas.join(' ')}</p>
            <p><strong>Pergunta engajadora:</strong> ${conteudoPronto.pergunta_engajadora}</p>
        </div>
        
        <div class="preview-actions">
            <button class="btn btn-primary" onclick="copiarParaAreaTransferencia('${conteudoPronto.trecho_original.texto.replace(/'/g, "\\'")}')">
                📋 Copiar Conteúdo
            </button>
        </div>
    `;
    
    modal.style.display = 'flex';
}

function closeModal() {
    document.getElementById('previewModal').style.display = 'none';
}

function copiarTrecho(texto) {
    copiarParaAreaTransferencia(texto);
}

function aplicarIdentidade(trecho) {
    // Redirecionar para a página de identidade com o trecho
    const identidadeData = {
        conteudo: trecho,
        acao: 'aplicar_identidade'
    };
    window.almaApp.salvarNoLocalStorage('identidade_pendente', identidadeData);
    window.location.href = '/identity-setup';
}

function verTrechosLivro(tituloLivro) {
    // Implementar visualização de trechos específicos do livro
    window.almaApp.mostrarNotificacao(`Carregando trechos de "${tituloLivro}"...`, 'info');
    // Aqui poderia abrir uma modal com todos os trechos do livro
}

async function removerLivro(tituloLivro) {
    if (!confirm(`Tem certeza que deseja remover "${tituloLivro}" da biblioteca?`)) {
        return;
    }

    try {
        const response = await window.almaApp.fazerRequisicao(`/api/escritora/remover-livro/${encodeURIComponent(tituloLivro)}`, {
            method: 'DELETE'
        });

        if (response.success) {
            window.almaApp.mostrarNotificacao(response.message, 'success');
            window.dashboardApp.carregarBibliotecaCompleta();
        }
    } catch (error) {
        console.error('Erro ao remover livro:', error);
        window.almaApp.mostrarNotificacao('Erro ao remover livro.', 'error');
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    window.dashboardApp = new DashboardEscritora();
});

