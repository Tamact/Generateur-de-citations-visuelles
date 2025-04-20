# Dimensions de l'image
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1080
PADDING = 100

# Chemins vers les polices
FONT_REGULAR_PATH = "Lato/Lato-Regular.ttf"
FONT_BOLD_PATH = "Lato/Lato-Bold.ttf"
FONT_SIGNATURE_PATH = "Lato/Lato-Light.ttf"

# Thèmes de couleurs
THEMES = {
    'light': {
        'bg_color1': (255, 255, 250),
        'bg_color2': (230, 230, 240),
        'text_color': (30, 30, 30),
        'author_color': (80, 80, 80),
        'signature_color': (100, 100, 100),
        'decoration_color': (150, 150, 180)
    },
    'dark': {
        'bg_color1': (20, 20, 30),
        'bg_color2': (40, 40, 80),
        'text_color': (240, 240, 240),
        'author_color': (180, 180, 180),
        'signature_color': (150, 150, 150),
        'decoration_color': (120, 120, 180)
    }
}

# Liste des styles de fond disponibles
BACKGROUND_STYLES = ['gradient', 'radial', 'uni']

# Liste des décorations disponibles
DECORATION_STYLES = ['aucune', 'guillemets', 'cadre', 'coins', 'motif']

# Tailles de police par défaut
FONT_SIZES = {
    'quote': 120,
    'author': 60,
    'signature': 30
}

# Textes par défaut
DEFAULT_SIGNATURE = "by Ibrahima Sory Sané"
DEFAULT_WATERMARK = "☆ Citation Visuelle ☆"

# Taille maximale de l'historique
MAX_HISTORY_SIZE = 10

# Variable globale pour savoir si on utilise la police par défaut
using_default_font = False 