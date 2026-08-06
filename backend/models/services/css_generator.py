from models.marca_profile import MarcaProfile
from typing import Dict

class CSSGenerator:
    def gerar_css_personalizado(self, marca_profile: MarcaProfile) -> str:
        """Gera CSS dinâmico baseado na identidade do cliente"""
        
        return f"""
        /* CSS Personalizado - {marca_profile.nome_marca} */
        :root {{
            --alma-primaria: {marca_profile.cores_primarias[0]};
            --alma-secundaria: {marca_profile.cores_primarias[1]};
            --alma-texto: {marca_profile.cores_primarias[2]};
            --alma-destaque: {self._gerar_cor_destaque(marca_profile.cores_primarias[0])};
            --alma-borda: {self._escurecer_cor(marca_profile.cores_primarias[1], 0.1)};
            
            --alma-fonte-titulo: '{marca_profile.fontes["titulo"]}';
            --alma-fonte-texto: '{marca_profile.fontes["texto"]}';
            
            --alma-sombra: {self._gerar_sombra(marca_profile.cores_primarias[2])};
            --alma-gradiente: linear-gradient(135deg, {marca_profile.cores_primarias[0]}, {marca_profile.cores_primarias[2]});
        }}
        
        /* Sistema Alma de Escritora */
        .alma-system {{
            font-family: var(--alma-fonte-texto), sans-serif;
            background-color: var(--alma-secundaria);
            color: var(--alma-texto);
            line-height: 1.6;
        }}
        
        .alma-header {{
            background: var(--alma-gradiente);
            color: white;
            padding: 2rem 0;
            text-align: center;
            box-shadow: var(--alma-sombra);
        }}
        
        .logo {{
            font-family: var(--alma-fonte-titulo), serif;
            font-size: 3rem;
            font-weight: 300;
            margin-bottom: 0.5rem;
        }}
        
        .tagline {{
            font-style: italic;
            opacity: 0.9;
            font-size: 1.2rem;
        }}
        
        .card {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 4px solid var(--alma-primaria);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
        }}
        
        .section-title {{
            font-family: var(--alma-fonte-titulo), serif;
            color: var(--alma-primaria);
            margin-bottom: 1.5rem;
            font-size: 1.8rem;
            border-bottom: 2px solid var(--alma-borda);
            padding-bottom: 0.5rem;
        }}
        
        .btn {{
            display: inline-block;
            padding: 12px 30px;
            border: none;
            border-radius: 6px;
            font-family: var(--alma-fonte-texto), sans-serif;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            text-align: center;
            font-weight: 500;
        }}
        
        .btn-primary {{
            background: var(--alma-primaria);
            color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .btn-primary:hover {{
            background: var(--alma-destaque);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        
        .btn-secondary {{
            background: transparent;
            color: var(--alma-primaria);
            border: 2px solid var(--alma-primaria);
        }}
        
        .btn-secondary:hover {{
            background: var(--alma-primaria);
            color: white;
            transform: translateY(-2px);
        }}
        
        .upload-area {{
            border: 2px dashed var(--alma-primaria);
            border-radius: 10px;
            padding: 3rem;
            text-align: center;
            transition: all 0.3s ease;
            background: rgba(139, 115, 85, 0.05);
        }}
        
        .upload-area:hover {{
            border-color: var(--alma-destaque);
            transform: translateY(-2px);
            background: rgba(139, 115, 85, 0.1);
        }}
        
        .upload-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
            color: var(--alma-primaria);
        }}
        
        .form-group {{
            margin-bottom: 1.5rem;
        }}
        
        .form-label {{
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: var(--alma-texto);
        }}
        
        .form-input, .form-select, .form-textarea {{
            width: 100%;
            padding: 12px;
            border: 2px solid var(--alma-borda);
            border-radius: 6px;
            font-family: var(--alma-fonte-texto), sans-serif;
            font-size: 1rem;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
            background: white;
        }}
        
        .form-input:focus, .form-select:focus, .form-textarea:focus {{
            outline: none;
            border-color: var(--alma-primaria);
            box-shadow: 0 0 0 3px rgba(139, 115, 85, 0.1);
        }}
        
        .color-picker {{
            display: flex;
            gap: 1rem;
            align-items: center;
            margin-bottom: 1rem;
        }}
        
        .color-input {{
            width: 60px;
            height: 40px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .loading {{
            text-align: center;
            padding: 3rem;
            display: none;
        }}
        
        .loading-spinner {{
            border: 4px solid var(--alma-borda);
            border-top: 4px solid var(--alma-primaria);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        /* Dashboard Específico */
        .biblioteca-status {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
            text-align: center;
        }}
        
        .biblioteca-status p {{
            background: var(--alma-secundaria);
            padding: 1rem;
            border-radius: 8px;
            margin: 0;
            border-left: 3px solid var(--alma-primaria);
        }}
        
        .trechos-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.5rem;
            margin-bottom: 1rem;
        }}
        
        .trecho-card {{
            background: white;
            border: 1px solid var(--alma-borda);
            border-radius: 10px;
            padding: 1.5rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .trecho-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        }}
        
        .trecho-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--alma-primaria);
        }}
        
        .trecho-texto {{
            font-style: italic;
            color: var(--alma-texto);
            margin-bottom: 1rem;
            line-height: 1.6;
            font-size: 1.1em;
        }}
        
        .trecho-metadata {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
            font-size: 0.9rem;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        
        .trecho-tema {{
            background: var(--alma-secundaria);
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            color: var(--alma-primaria);
            font-weight: 500;
        }}
        
        .trecho-engajamento {{
            color: var(--alma-destaque);
            font-weight: 600;
        }}
        
        .trecho-acoes {{
            display: flex;
            gap: 0.5rem;
            margin-top: 1rem;
        }}
        
        .btn-small {{
            padding: 0.5rem 1rem;
            font-size: 0.8rem;
        }}
        
        /* Responsivo */
        @media (max-width: 768px) {{
            .biblioteca-status {{
                grid-template-columns: 1fr;
            }}
            
            .trechos-grid {{
                grid-template-columns: 1fr;
            }}
            
            .logo {{
                font-size: 2rem;
            }}
            
            .card {{
                padding: 1.5rem;
            }}
            
            .color-picker {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
        
        /* Utilitários */
        .text-center {{ text-align: center; }}
        .text-primary {{ color: var(--alma-primaria); }}
        .bg-primary {{ background: var(--alma-primaria); }}
        .bg-secondary {{ background: var(--alma-secundaria); }}
        .border-primary {{ border-color: var(--alma-primaria); }}
        """
    
    def _gerar_cor_destaque(self, cor_base: str) -> str:
        """Gera uma cor de destaque baseada na cor principal"""
        # Simples escurecimento para cor de destaque
        if cor_base.startswith('#'):
            r, g, b = int(cor_base[1:3], 16), int(cor_base[3:5], 16), int(cor_base[5:7], 16)
            r = max(0, r - 20)
            g = max(0, g - 20)
            b = max(0, b - 20)
            return f"#{r:02x}{g:02x}{b:02x}"
        return cor_base
    
    def _escurecer_cor(self, cor: str, fator: float) -> str:
        """Escurece uma cor por um fator"""
        if cor.startswith('#'):
            r, g, b = int(cor[1:3], 16), int(cor[3:5], 16), int(cor[5:7], 16)
            r = int(r * (1 - fator))
            g = int(g * (1 - fator))
            b = int(b * (1 - fator))
            return f"#{r:02x}{g:02x}{b:02x}"
        return cor
    
    def _gerar_sombra(self, cor_base: str) -> str:
        """Gera sombra sutil baseada na cor do texto"""
        return f"0 2px 10px {self._escurecer_cor(cor_base, 0.8)}22"
    
    def gerar_css_para_preview(self, marca_profile: MarcaProfile) -> str:
        """Gera CSS específico para preview em tempo real"""
        return f"""
        .preview-container {{
            font-family: {marca_profile.fontes['texto']}, sans-serif;
            background: {marca_profile.cores_primarias[1]};
            color: {marca_profile.cores_primarias[2]};
            padding: 20px;
            border-radius: 10px;
            border: 2px solid {marca_profile.cores_primarias[0]};
        }}
        
        .preview-titulo {{
            font-family: {marca_profile.fontes['titulo']}, serif;
            color: {marca_profile.cores_primarias[0]};
            text-align: center;
            margin-bottom: 15px;
        }}
        """

