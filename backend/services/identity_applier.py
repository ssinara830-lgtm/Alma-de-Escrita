from models.marca_profile import MarcaProfile
from typing import Dict, Any

class IdentityApplier:
    def aplicar_identidade_post(self, conteudo: dict, marca_profile: MarcaProfile, formato: str) -> Dict[str, Any]:
        """Aplica identidade visual a um post específico"""
        
        return {
            "platform": "instagram",
            "tipo": formato,
            "conteudo": {
                "copy": self._formatar_copy(conteudo, marca_profile),
                "hashtags": conteudo.get("hashtags_sugeridas", []),
                "estilo_aplicado": {
                    "cor_fundo": marca_profile.cores_primarias[1],
                    "cor_texto": marca_profile.cores_primarias[2],
                    "cor_destaque": marca_profile.cores_primarias[0],
                    "fonte_titulo": marca_profile.fontes["titulo"],
                    "fonte_texto": marca_profile.fontes["texto"]
                }
            },
            "preview_html": self._gerar_html_preview(conteudo, marca_profile)
        }
    
    def _formatar_copy(self, conteudo: dict, marca_profile: MarcaProfile) -> str:
        texto = conteudo['texto']
        pergunta = conteudo.get('pergunta_engajadora', '')
        
        copy = f"{texto}"
        if pergunta:
            copy += f"\n\n{pergunta}"
        
        copy += f"\n\n— {marca_profile.nome_marca}"
        
        return copy
    
    def _gerar_html_preview(self, conteudo: dict, marca_profile: MarcaProfile) -> str:
        return f"""
        <div style="background: {marca_profile.cores_primarias[1]}; padding: 20px; border-radius: 10px; border-left: 5px solid {marca_profile.cores_primarias[0]};">
            <h3 style="color: {marca_profile.cores_primarias[0]}; font-family: {marca_profile.fontes['titulo']}, serif;">
                {conteudo.get('tema', 'Reflexão')}
            </h3>
            <p style="color: {marca_profile.cores_primarias[2]}; font-family: {marca_profile.fontes['texto']}, sans-serif;">
                "{conteudo['texto']}"
            </p>
        </div>
        """
