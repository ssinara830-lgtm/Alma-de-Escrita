// Identity Setup
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
});