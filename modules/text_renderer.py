import textwrap
from PIL import ImageDraw, ImageFont
from modules import config

def calculate_text_layout(draw, quote, author, fonts, is_default, max_width_px):
    """
    Calcule la disposition du texte sur l'image.
    
    Args:
        draw (PIL.ImageDraw.Draw): Objet de dessin PIL
        quote (str): Texte de la citation
        author (str): Nom de l'auteur
        fonts (tuple): Polices à utiliser (quote_font, author_font, signature_font)
        is_default (bool): Si on utilise la police par défaut
        max_width_px (int): Largeur maximale disponible pour le texte
        
    Returns:
        tuple: (wrapped_quote, line_heights, total_text_height, author_text, author_width, author_line_height)
    """
    quote_font, author_font, signature_font = fonts
    
    # Calcul de la césure (wrap)
    if is_default:
        chars_per_line_default = 60  # Plus de caractères par ligne pour la police par défaut
        wrapped_quote = textwrap.fill(quote, width=chars_per_line_default)
    else:
        # Estimation pour TrueType
        avg_char_width = draw.textlength("a", font=quote_font)
        chars_per_line = int(max_width_px / avg_char_width) if avg_char_width > 0 else 30
        wrapped_quote = textwrap.fill(quote, width=chars_per_line)
    
    quote_lines = wrapped_quote.split('\n')
    line_spacing = 10 if is_default else 15  # Moins d'espace pour la police par défaut
    
    # Calcul de la hauteur totale
    total_text_height = 0
    line_heights = []
    
    for line in quote_lines:
        if is_default:
            # Estimation pour police par défaut (hauteur fixe, largeur variable)
            line_width = draw.textlength(line, font=quote_font)
            line_height = 10  # Hauteur approximative de la police par défaut
        else:
            # Utilisation de textbbox pour TrueType
            line_bbox = draw.textbbox((0, 0), line, font=quote_font)
            line_width = line_bbox[2] - line_bbox[0]
            line_height = line_bbox[3] - line_bbox[1]
        
        line_heights.append(line_height)
        total_text_height += line_height
    
    total_text_height += line_spacing * (len(quote_lines) - 1)
    
    # Informations pour l'auteur
    author_text = ""
    author_width = 0
    author_line_height = 0
    
    if author:
        author_text = f"— {author}"
        if is_default:
            author_line_height = 10
            author_width = draw.textlength(author_text, font=author_font)
        else:
            author_bbox = draw.textbbox((0, 0), author_text, font=author_font)
            author_width = author_bbox[2] - author_bbox[0]
            author_line_height = author_bbox[3] - author_bbox[1]
        
        # Ajouter l'espace pour l'auteur
        total_text_height += author_line_height + line_spacing * 2  # Espace avant auteur
    
    return (wrapped_quote, quote_lines, line_heights, line_spacing, 
            total_text_height, author_text, author_width, author_line_height)

def render_quote_text(img, quote, author, fonts, theme, add_signature=True, add_watermark=True):
    """
    Dessine la citation, l'auteur, et optionnellement la signature et le watermark sur l'image.
    
    Args:
        img (PIL.Image): Image sur laquelle dessiner
        quote (str): Texte de la citation
        author (str): Nom de l'auteur
        fonts (tuple): Polices à utiliser (quote_font, author_font, signature_font)
        theme (str): Thème de couleurs
        add_signature (bool): Si la signature doit être ajoutée
        add_watermark (bool): Si le watermark doit être ajouté
        
    Returns:
        PIL.Image: Image avec le texte ajouté
    """
    quote_font, author_font, signature_font = fonts
    is_default = isinstance(quote_font, ImageFont.ImageFont)  # Vérifie si c'est la police par défaut
    
    # Récupérer les couleurs du thème
    text_color = config.THEMES[theme]['text_color']
    author_color = config.THEMES[theme]['author_color']
    signature_color = config.THEMES[theme]['signature_color']
    
    # Préparer le dessin
    draw = ImageDraw.Draw(img)
    max_width_px = config.IMAGE_WIDTH - (2 * config.PADDING)
    
    try:
        # Calculer la disposition du texte
        layout = calculate_text_layout(draw, quote, author, fonts, is_default, max_width_px)
        (wrapped_quote, quote_lines, line_heights, line_spacing, 
         total_text_height, author_text, author_width, author_line_height) = layout
        
        # Calculer l'espace pour la signature
        signature_height = 0
        if add_signature:
            signature_text = config.DEFAULT_SIGNATURE
            if is_default:
                signature_height = 10
            else:
                signature_bbox = draw.textbbox((0, 0), signature_text, font=signature_font)
                signature_height = signature_bbox[3] - signature_bbox[1]
        
        # Calculer la position Y de départ pour centrer verticalement le texte principal
        current_y = (config.IMAGE_HEIGHT - total_text_height - signature_height - 20) / 2
        
        # Dessiner la citation
        for i, line in enumerate(quote_lines):
            if is_default:
                line_width = draw.textlength(line, font=quote_font)
            else:
                line_bbox = draw.textbbox((0, 0), line, font=quote_font)
                line_width = line_bbox[2] - line_bbox[0]
            
            line_x = (config.IMAGE_WIDTH - line_width) / 2  # Centrer horizontalement
            draw.text((line_x, current_y), line, font=quote_font, fill=text_color)
            current_y += line_heights[i] + line_spacing
        
        # Dessiner l'auteur
        if author:
            current_y += line_spacing  # Espace supplémentaire
            author_x = (config.IMAGE_WIDTH - author_width) / 2
            draw.text((author_x, current_y), author_text, font=author_font, fill=author_color)
        
        # Ajouter la signature en bas
        if add_signature:
            signature_text = config.DEFAULT_SIGNATURE
            if is_default:
                signature_width = draw.textlength(signature_text, font=signature_font)
            else:
                signature_bbox = draw.textbbox((0, 0), signature_text, font=signature_font)
                signature_width = signature_bbox[2] - signature_bbox[0]
            
            signature_x = config.IMAGE_WIDTH - signature_width - 20
            signature_y = config.IMAGE_HEIGHT - signature_height - 20
            draw.text((signature_x, signature_y), signature_text, font=signature_font, fill=signature_color)
        
        # Ajouter le watermark
        if add_watermark:
            watermark_text = config.DEFAULT_WATERMARK
            if is_default:
                watermark_width = draw.textlength(watermark_text, font=signature_font)
                watermark_height = 10
            else:
                watermark_bbox = draw.textbbox((0, 0), watermark_text, font=signature_font)
                watermark_width = watermark_bbox[2] - watermark_bbox[0]
                watermark_height = watermark_bbox[3] - watermark_bbox[1]
            
            watermark_x = 20
            watermark_y = config.IMAGE_HEIGHT - watermark_height - 20
            draw.text((watermark_x, watermark_y), watermark_text, font=signature_font, fill=signature_color)
    
    except Exception as e:
        # En cas d'erreur, essayer d'afficher un message d'erreur sur l'image
        try:
            draw.text((config.PADDING, config.PADDING), f"Erreur lors du rendu du texte: {e}", 
                      fill=(255, 0, 0), font=quote_font or ImageFont.load_default())
        except:
            pass  # Si même ça échoue, ne rien faire de plus
    
    return img 