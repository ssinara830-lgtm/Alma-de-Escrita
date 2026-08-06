// Dashboard da Escritora
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
});