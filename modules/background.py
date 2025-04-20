from PIL import Image, ImageDraw
from modules import config

def create_gradient_background(width, height, color1, color2, direction='vertical'):
    """
    Crée un fond dégradé entre deux couleurs.
    
    Args:
        width (int): Largeur de l'image
        height (int): Hauteur de l'image
        color1 (tuple): Couleur RGB de départ
        color2 (tuple): Couleur RGB de fin
        direction (str): Direction du dégradé ('vertical' ou 'horizontal')
        
    Returns:
        PIL.Image: Image avec le fond dégradé
    """
    image = Image.new('RGB', (width, height), color=color1)
    draw = ImageDraw.Draw(image)
    
    if direction == 'vertical':
        for y in range(height):
            # Calcul du ratio de progression
            ratio = y / height
            # Interpolation linéaire entre les couleurs
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    else:  # horizontal
        for x in range(width):
            ratio = x / width
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.line([(x, 0), (x, height)], fill=(r, g, b))
            
    return image

def create_radial_background(width, height, color1, color2):
    """
    Crée un fond avec un dégradé radial.
    
    Args:
        width (int): Largeur de l'image
        height (int): Hauteur de l'image
        color1 (tuple): Couleur RGB du centre
        color2 (tuple): Couleur RGB des bords
        
    Returns:
        PIL.Image: Image avec le fond dégradé radial
    """
    img = Image.new('RGB', (width, height), color=color2)
    draw = ImageDraw.Draw(img)
    
    for r in range(max(width, height), 0, -1):
        ratio = r / max(width, height)
        r_color = int(color1[0] * ratio + color2[0] * (1 - ratio))
        g_color = int(color1[1] * ratio + color2[1] * (1 - ratio))
        b_color = int(color1[2] * ratio + color2[2] * (1 - ratio))
        
        draw.ellipse([(width//2 - r, height//2 - r), 
                     (width//2 + r, height//2 + r)], 
                     fill=(r_color, g_color, b_color))
                     
    return img

def create_solid_background(width, height, color):
    """
    Crée un fond uni d'une couleur spécifique.
    
    Args:
        width (int): Largeur de l'image
        height (int): Hauteur de l'image
        color (tuple): Couleur RGB du fond
        
    Returns:
        PIL.Image: Image avec le fond uni
    """
    return Image.new('RGB', (width, height), color=color)

def create_background(style, theme):
    """
    Crée le fond de l'image selon le style et le thème choisis.
    
    Args:
        style (str): Style de fond ('gradient', 'radial', 'uni')
        theme (str): Thème de couleurs ('light', 'dark')
        
    Returns:
        PIL.Image: Image avec le fond généré
    """
    # Obtenir les couleurs du thème
    bg_color1 = config.THEMES[theme]['bg_color1']
    bg_color2 = config.THEMES[theme]['bg_color2']
    
    # Créer le fond selon le style choisi
    if style == 'gradient':
        return create_gradient_background(config.IMAGE_WIDTH, config.IMAGE_HEIGHT, bg_color1, bg_color2)
    elif style == 'radial':
        return create_radial_background(config.IMAGE_WIDTH, config.IMAGE_HEIGHT, bg_color1, bg_color2)
    else:  # 'uni'
        return create_solid_background(config.IMAGE_WIDTH, config.IMAGE_HEIGHT, bg_color1) 