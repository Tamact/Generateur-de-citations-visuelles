import io
import streamlit as st
from PIL import Image, ImageDraw
from modules import config, font_manager, background, decorations, text_renderer

def generate_quote_image(quote, author, theme='light', background_style='gradient', 
                        watermark=True, signature=True, decoration=None):
    """
    Génère l'image stylisée et retourne ses données binaires (bytes).
    
    Args:
        quote (str): Texte de la citation
        author (str): Nom de l'auteur
        theme (str): Thème de couleurs ('light', 'dark')
        background_style (str): Style de fond ('gradient', 'radial', 'uni')
        watermark (bool): Si le watermark doit être ajouté
        signature (bool): Si la signature doit être ajoutée
        decoration (str): Style de décoration ('aucune', 'guillemets', 'cadre', 'coins', 'motif')
        
    Returns:
        bytes: Données binaires de l'image générée, ou None en cas d'erreur
    """
    # Réinitialiser la détection de police par défaut
    config.using_default_font = False
    
    try:
        # 1. Créer le fond
        img = background.create_background(background_style, theme)
        
        # 2. Ajouter les décorations
        if decoration:
            img = decorations.add_decorative_elements(img, decoration, theme)
        
        # 3. Charger les polices
        fonts = font_manager.load_fonts(theme)
        quote_font, author_font, signature_font, is_default = fonts
        
        # 4. Ajouter le texte
        img = text_renderer.render_quote_text(
            img, quote, author, (quote_font, author_font, signature_font), 
            theme, add_signature=signature, add_watermark=watermark
        )
        
        # 5. Convertir l'image en bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr
        
    except Exception as e:
        st.error(f"Erreur lors de la génération de l'image : {e}")
        return None 