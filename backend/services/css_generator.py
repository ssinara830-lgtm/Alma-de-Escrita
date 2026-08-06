from models.marca_profile import MarcaProfile
from typing import Dict

class CSSGenerator:
    def gerar_css_personalizado(self, marca_profile: MarcaProfile) -> str:
        """Gera CSS dinâmico baseado na identidade do cliente"""
        
        return f"""
/* ALMA DE ESCRITORA - CSS Personalizado */
:root {{
    --alma-primaria: {marca_profile.cores_primarias[0]};
    --alma-secundaria: {marca_profile.cores_primarias[1]};
    --alma-texto: {marca_profile.cores_primarias[2]};
    --alma-fonte-titulo: '{marca_profile.fontes["titulo"]}';
    --alma-fonte-texto: '{marca_profile.fontes["texto"]}';
}}

body {{
    font-family: var(--alma-fonte-texto), sans-serif;
    background-color: var(--alma-secundaria);
    color: var(--alma-texto);
}}

h1, h2, h3 {{
    font-family: var(--alma-fonte-titulo), serif;
    color: var(--alma-primaria);
}}

.btn-primary {{
    background: var(--alma-primaria);
    color: white;
}}
"""
