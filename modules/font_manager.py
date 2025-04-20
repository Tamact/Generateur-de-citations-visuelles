import os
import streamlit as st
from PIL import ImageFont
from modules import config

def get_font(font_path, requested_size):
    """
    Charge la police spécifiée ou retourne la police par défaut de Pillow si non trouvée.
    
    Args:
        font_path (str): Chemin vers le fichier de police
        requested_size (int): Taille de police demandée
        
    Returns:
        PIL.ImageFont: La police chargée
    """
    if font_path and os.path.exists(font_path):
        try:
            font = ImageFont.truetype(font_path, requested_size)
            return font
        except Exception as e:
            st.sidebar.warning(f"Impossible de charger {os.path.basename(font_path)}: {e}. Utilisation de la police par défaut.")
            config.using_default_font = True
            return ImageFont.load_default()
    else:
        # N'affiche l'avertissement qu'une seule fois globalement
        if not config.using_default_font:
             st.sidebar.warning(f"Police '{os.path.basename(font_path)}' non trouvée. Utilisation de la police par défaut (qualité limitée).")
             config.using_default_font = True
        return ImageFont.load_default()

def load_fonts(theme='light'):
    """
    Charge toutes les polices nécessaires pour le rendu de l'image.
    
    Args:
        theme (str): Thème actuel (non utilisé actuellement mais pourrait servir pour charger des polices spécifiques par thème)
        
    Returns:
        tuple: (quote_font, author_font, signature_font, is_default)
    """
    # Charger les polices
    quote_font = get_font(config.FONT_REGULAR_PATH, config.FONT_SIZES['quote'])
    
    # Si la police bold n'existe pas ou est identique à la régulière, utiliser la même que quote_font
    author_font_path = config.FONT_BOLD_PATH if config.FONT_BOLD_PATH != config.FONT_REGULAR_PATH else config.FONT_REGULAR_PATH
    author_font = get_font(author_font_path, config.FONT_SIZES['author'])
    
    # Police pour la signature
    signature_font = get_font(config.FONT_SIGNATURE_PATH, config.FONT_SIZES['signature'])
    
    # Vérifier si on utilise la police par défaut
    is_default = isinstance(quote_font, ImageFont.ImageFont)
    
    # Si on utilise la police par défaut, l'utiliser pour tout
    if is_default:
        author_font = quote_font
        signature_font = quote_font
    elif isinstance(author_font, ImageFont.ImageFont):
        # Si la police bold n'a pas été chargée correctement
        author_font = quote_font
        
    return quote_font, author_font, signature_font, is_default 