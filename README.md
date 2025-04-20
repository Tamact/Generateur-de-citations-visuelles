# Générateur de Citations Visuelles

Une application web élégante pour créer des images de citations inspirantes avec divers styles visuels.



## Description

Ce générateur vous permet de transformer des citations en images visuellement attrayantes, prêtes à être partagées sur les réseaux sociaux ou à être téléchargées. Vous pouvez personnaliser la citation, l'auteur, le style visuel et même ajouter des décorations.

## Fonctionnalités

- 🖼️ Génération d'images de citations au format PNG
- 🎨 Plusieurs styles de fond (dégradé, radial, uni)
- 🌓 Thèmes clair et sombre
- 🎭 Décorations variées (guillemets, cadre, coins, motif)
- 🔄 Accès à une API pour obtenir des citations aléatoires
- 📊 Historique des citations générées
- 💾 Téléchargement des images générées

## Installation

### Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. Clonez ce dépôt:
   ```bash
   git clone https://github.com/votre-compte/generateur-citations-visuelles.git
   cd generateur-citations-visuelles
   ```

2. Installez les dépendances:
   ```bash
   pip install -r requirements.txt
   ```

3. Pour les polices (optionnel mais recommandé):
   - Créez un dossier `Lato` dans le répertoire principal
   - Placez-y les fichiers de police:
     - `Lato-Regular.ttf`
     - `Lato-Bold.ttf`
     - `Lato-Light.ttf`

## Utilisation

1. Lancez l'application:
   ```bash
   streamlit run app.py
   ```

2. Ouvrez votre navigateur à l'adresse indiquée (généralement http://localhost:8501)

3. Utilisez l'interface pour:
   - Entrer votre propre citation ou en générer une aléatoire
   - Personnaliser l'apparence visuelle
   - Générer l'image
   - Télécharger le résultat

## Structure du projet

Le projet est organisé en modules pour faciliter la maintenance et l'extension:

```
generateur-citations-visuelles/
├── app.py                # Application principale
├── modules/              # Modules du projet
│   ├── __init__.py       # Initialisation du package
│   ├── api_client.py     # Client API pour récupérer des citations
│   ├── background.py     # Générateurs de fonds
│   ├── config.py         # Configuration globale
│   ├── decorations.py    # Éléments décoratifs
│   ├── font_manager.py   # Gestion des polices
│   ├── generator.py      # Générateur principal d'images
│   └── text_renderer.py  # Rendu du texte sur les images
├── Lato/                 # Dossier des polices (à créer)
│   ├── Lato-Regular.ttf  # Police régulière
│   ├── Lato-Bold.ttf     # Police grasse
│   └── Lato-Light.ttf    # Police légère
└── requirements.txt      # Dépendances du projet
```

## Personnalisation

### Ajout de nouveaux thèmes

Modifiez le fichier `modules/config.py` pour ajouter de nouveaux thèmes de couleurs:

```python
THEMES = {
    'mon_theme': {
        'bg_color1': (r, g, b),
        'bg_color2': (r, g, b),
        'text_color': (r, g, b),
        'author_color': (r, g, b),
        'signature_color': (r, g, b),
        'decoration_color': (r, g, b)
    },
    # ... autres thèmes existants
}
```

### Ajout de nouvelles décorations

1. Ajoutez un nouveau type de décoration dans `config.py`:
   ```python
   DECORATION_STYLES = ['aucune', 'guillemets', 'cadre', 'coins', 'motif', 'ma_nouvelle_deco']
   ```

2. Implémentez la logique de dessin dans `decorations.py`:
   ```python
   # Dans la fonction add_decorative_elements
   elif decoration_style == "ma_nouvelle_deco":
       # Votre code de dessin
   ```

## Exigences

Pour installer toutes les dépendances nécessaires:

```bash
pip install streamlit pillow requests
```

Ou via le fichier requirements.txt:

```bash
pip install -r requirements.txt
```

## Auteur

Ibrahima Sory Sané

