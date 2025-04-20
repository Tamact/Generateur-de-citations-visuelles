from PIL import ImageDraw
from math import sin, cos, pi
from modules import config, font_manager

def draw_decoration(img, decoration_type, color, pos_x, pos_y, size):
    """
    Dessine une décoration/icône sur l'image.
    
    Args:
        img (PIL.Image): Image sur laquelle dessiner
        decoration_type (str): Type de décoration ('guillemets', 'étoile', 'cercle', 'ligne')
        color (tuple): Couleur RGB de la décoration
        pos_x (int): Position X
        pos_y (int): Position Y
        size (int): Taille de la décoration
        
    Returns:
        PIL.Image: Image avec la décoration ajoutée
    """
    draw = ImageDraw.Draw(img)
    
    if decoration_type == "guillemets":
        # Dessiner des guillemets stylisés
        quote_size = size
        draw.text((pos_x, pos_y), "\"\"", font=font_manager.get_font(config.FONT_BOLD_PATH, quote_size*2), fill=color)
    
    elif decoration_type == "étoile":
        # Dessiner une étoile
        points = []
        outer_radius = size
        inner_radius = size / 2
        for i in range(10):
            angle = i * pi / 5
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = pos_x + radius * sin(angle)
            y = pos_y + radius * cos(angle)
            points.append((x, y))
        draw.polygon(points, fill=color)
    
    elif decoration_type == "cercle":
        # Dessiner un cercle
        draw.ellipse((pos_x - size, pos_y - size, pos_x + size, pos_y + size), outline=color, width=3)
    
    elif decoration_type == "ligne":
        # Dessiner une ligne décorative
        draw.line([(pos_x - size, pos_y), (pos_x + size, pos_y)], fill=color, width=5)
        
    return img

def add_decorative_elements(img, decoration_style, theme):
    """
    Ajoute des éléments décoratifs à l'image selon le style choisi.
    
    Args:
        img (PIL.Image): Image de base
        decoration_style (str): Style de décoration ('aucune', 'guillemets', 'cadre', 'coins', 'motif')
        theme (str): Thème de couleurs ('light', 'dark')
        
    Returns:
        PIL.Image: Image avec les décorations ajoutées
    """
    if not decoration_style or decoration_style == 'aucune':
        return img
        
    # Obtenir la couleur de décoration du thème actuel
    decoration_color = config.THEMES[theme]['decoration_color']
    
    if decoration_style == "guillemets":
        # Guillemets dans le coin supérieur gauche
        img = draw_decoration(img, "guillemets", decoration_color, config.PADDING, config.PADDING, 80)
    
    elif decoration_style == "cadre":
        # Dessiner un cadre simple
        draw = ImageDraw.Draw(img)
        line_thickness = 5
        margin = 50
        draw.rectangle([(margin, margin), (config.IMAGE_WIDTH-margin, config.IMAGE_HEIGHT-margin)], 
                     outline=decoration_color, width=line_thickness)
    
    elif decoration_style == "coins":
        # Dessiner des décorations aux quatre coins
        draw = ImageDraw.Draw(img)
        corner_size = 80
        line_width = 5
        margin = 40
        
        # Coin supérieur gauche
        draw.line([(margin, margin), (margin + corner_size, margin)], fill=decoration_color, width=line_width)
        draw.line([(margin, margin), (margin, margin + corner_size)], fill=decoration_color, width=line_width)
        
        # Coin supérieur droit
        draw.line([(config.IMAGE_WIDTH - margin, margin), (config.IMAGE_WIDTH - margin - corner_size, margin)], 
                 fill=decoration_color, width=line_width)
        draw.line([(config.IMAGE_WIDTH - margin, margin), (config.IMAGE_WIDTH - margin, margin + corner_size)], 
                 fill=decoration_color, width=line_width)
        
        # Coin inférieur gauche
        draw.line([(margin, config.IMAGE_HEIGHT - margin), (margin + corner_size, config.IMAGE_HEIGHT - margin)], 
                 fill=decoration_color, width=line_width)
        draw.line([(margin, config.IMAGE_HEIGHT - margin), (margin, config.IMAGE_HEIGHT - margin - corner_size)], 
                 fill=decoration_color, width=line_width)
        
        # Coin inférieur droit
        draw.line([(config.IMAGE_WIDTH - margin, config.IMAGE_HEIGHT - margin), 
                  (config.IMAGE_WIDTH - margin - corner_size, config.IMAGE_HEIGHT - margin)], 
                 fill=decoration_color, width=line_width)
        draw.line([(config.IMAGE_WIDTH - margin, config.IMAGE_HEIGHT - margin), 
                  (config.IMAGE_WIDTH - margin, config.IMAGE_HEIGHT - margin - corner_size)], 
                 fill=decoration_color, width=line_width)
    
    elif decoration_style == "motif":
        # Dessiner un motif répété (points)
        draw = ImageDraw.Draw(img)
        dot_size = 4
        spacing = 80
        rows = int(config.IMAGE_HEIGHT / spacing)
        cols = int(config.IMAGE_WIDTH / spacing)
        
        for r in range(rows):
            for c in range(cols):
                x = c * spacing + spacing/2
                y = r * spacing + spacing/2
                draw.ellipse([(x-dot_size, y-dot_size), (x+dot_size, y+dot_size)], 
                           fill=decoration_color)
    
    return img 