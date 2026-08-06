// ALMA DE ESCRITORA - JavaScript
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
});