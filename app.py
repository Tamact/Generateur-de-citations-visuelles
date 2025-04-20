import streamlit as st
import random
import os
from modules import config, api_client, generator

# --- Configuration de la page Streamlit ---
st.set_page_config(layout="wide", page_title="Générateur de Citations")

st.title("🖼️ Générateur de Citations Visuelles ✍️")
st.markdown("Créez rapidement des images de citations inspirantes !")

# --- Initialisation de la session ---
def init_session_state():
    """Initialise les variables de session."""
    if 'quote' not in st.session_state:
        st.session_state.quote = "La seule limite à notre réalisation de demain sera nos doutes d'aujourd'hui."
    if 'author' not in st.session_state:
        st.session_state.author = "Franklin D. Roosevelt"
    if 'generated_image' not in st.session_state:
        st.session_state.generated_image = None
    if 'using_default_font_message_shown' not in st.session_state:
        st.session_state.using_default_font_message_shown = False
    if 'history' not in st.session_state:
        st.session_state.history = []

init_session_state()

# --- Interface utilisateur de la barre latérale ---
def render_sidebar():
    """Rend l'interface de la barre latérale."""
    st.sidebar.header("Configuration")
    
    # Source de la citation
    source = st.sidebar.radio("Source de la citation :", 
                              ('Manuelle', 'API (type.fit)'), 
                              key='source_choice')
    
    if source == 'API (type.fit)':
        if st.sidebar.button("💡 Charger une citation aléatoire"):
            load_random_quote()
    
    # Entrée manuelle
    st.sidebar.text_area("Citation :", key='quote', height=150)
    st.sidebar.text_input("Auteur :", key='author')
    
    # Options de style
    st.sidebar.subheader("Style de l'image")
    
    st.sidebar.selectbox("Thème :", 
                         config.THEMES.keys(), 
                         key='theme_choice')
    
    st.sidebar.selectbox("Style de fond :", 
                         config.BACKGROUND_STYLES, 
                         key='background_style')
    
    st.sidebar.selectbox("Décoration :", 
                         config.DECORATION_STYLES,
                         key='decoration_style')
    
    st.sidebar.checkbox("Ajouter un watermark", 
                        value=True, 
                        key='add_watermark')
    
    st.sidebar.checkbox("Ajouter signature", 
                        value=True, 
                        key='add_signature')
    
    st.sidebar.divider()
    
    return st.sidebar.button("🚀 Générer l'image", 
                             type="primary", 
                             use_container_width=True)

# --- Fonctions utilitaires ---
def load_random_quote():
    """Charge une citation aléatoire depuis l'API."""
    with st.spinner("Recherche d'inspiration..."):
        quote_text, quote_author, error_msg = api_client.get_quote_from_api()
        if error_msg:
            st.sidebar.error(error_msg)
        elif quote_text:
            st.session_state.quote = quote_text
            st.session_state.author = quote_author or "Inconnu"
            st.session_state.generated_image = None
            st.sidebar.success("Citation chargée !")
            st.session_state.using_default_font_message_shown = False
        else:
            st.sidebar.warning("Impossible de charger la citation depuis l'API.")

def add_to_history(quote, author, image, theme, background, decoration):
    """Ajoute une citation à l'historique."""
    # Identifiant unique pour l'historique
    timestamp = random.randint(1000, 9999)
    
    history_item = {
        "id": timestamp,
        "quote": quote,
        "author": author,
        "image": image,
        "theme": theme,
        "background": background,
        "decoration": decoration
    }
    
    # Ajouter au début de l'historique
    st.session_state.history.insert(0, history_item)
    
    # Limiter la taille de l'historique
    if len(st.session_state.history) > config.MAX_HISTORY_SIZE:
        st.session_state.history.pop()

def generate_image():
    """Génère l'image de citation avec les paramètres actuels."""
    if not st.session_state.quote:
        st.warning("Veuillez entrer une citation.")
        return False
    
    with st.spinner("Création de l'image..."):
        # Gestion de la valeur du paramètre decoration
        decoration_param = None if st.session_state.decoration_style == 'aucune' else st.session_state.decoration_style
        
        # Générer l'image
        image_bytes = generator.generate_quote_image(
            st.session_state.quote,
            st.session_state.author,
            theme=st.session_state.theme_choice,
            background_style=st.session_state.background_style,
            watermark=st.session_state.add_watermark,
            signature=st.session_state.add_signature,
            decoration=decoration_param
        )
        
        if image_bytes:
            st.session_state.generated_image = image_bytes
            
            # Ajouter à l'historique
            add_to_history(
                st.session_state.quote,
                st.session_state.author,
                image_bytes,
                st.session_state.theme_choice,
                st.session_state.background_style,
                st.session_state.decoration_style
            )
            
            return True
        else:
            st.error("La génération de l'image a échoué.")
            st.session_state.generated_image = None
            return False

# --- Interface principale ---
def render_main_column():
    """Rend la colonne principale avec l'aperçu de l'image."""
    st.subheader("Aperçu :")
    
    # Afficher un avertissement si la police par défaut est utilisée
    if config.using_default_font and not st.session_state.using_default_font_message_shown:
        st.warning("Rendu avec la police par défaut (basse qualité). Pour un meilleur résultat, placez les fichiers de police dans le dossier 'Lato'.", icon="ℹ️")
        st.session_state.using_default_font_message_shown = True
    
    # Afficher l'image générée
    if st.session_state.generated_image:
        st.image(
            st.session_state.generated_image,
            caption=f"Citation de {st.session_state.author or 'Inconnu'}",
            use_container_width=True
        )
        
        # Option de téléchargement
        default_filename = f"citation_{st.session_state.author.replace(' ','_').lower() if st.session_state.author else 'inconnu'}_{st.session_state.quote[:15].replace(' ','_').lower()}.png"
        safe_filename = "".join(c for c in default_filename if c.isalnum() or c in ('_', '.', '-')).rstrip()
        
        st.download_button(
            label="📥 Télécharger (.png)",
            data=st.session_state.generated_image,
            file_name=safe_filename,
            mime="image/png",
        )
    else:
        st.info("Configurez et cliquez sur 'Générer l'image'.")

def render_history_column():
    """Rend la colonne d'historique des citations générées."""
    st.subheader("Historique des citations")
    
    if not st.session_state.history:
        st.info("Votre historique de citations apparaîtra ici.")
        return
    
    # Afficher l'historique des citations générées
    for i, item in enumerate(st.session_state.history):
        title = f"{item['author']} - {item['quote'][:30]}..." if len(item['quote']) > 30 else item['quote']
        
        with st.expander(title):
            st.image(item['image'], use_container_width=True)
            st.caption(f"Theme: {item['theme']} | Fond: {item['background']} | Décoration: {item.get('decoration', 'aucune')}")
            
            # Ajouter un bouton pour réutiliser cette citation
            if st.button(f"Réutiliser cette citation", key=f"reuse_{item['id']}"):
                st.session_state.quote = item['quote']
                st.session_state.author = item['author']
                st.session_state.theme_choice = item['theme']
                st.session_state.background_style = item['background']
                st.session_state.decoration_style = item.get('decoration', 'aucune')
                st.session_state.generated_image = item['image']
                st.rerun()

# --- Pied de page ---
def render_footer():
    """Rend le pied de page de l'application."""
    st.sidebar.divider()
    st.sidebar.markdown("---")
    st.sidebar.caption("Mini Projet #1 - Générateur de Citations")

# --- Application principale ---
def main():
    """Fonction principale de l'application."""
    # Barre latérale
    generate_button = render_sidebar()
    
    # Disposition en colonnes
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Génération d'image si le bouton est cliqué
        if generate_button:
            # Réinitialiser le flag d'avertissement avant la génération
            st.session_state.using_default_font_message_shown = False
            config.using_default_font = False
            
            # Générer l'image
            generate_image()
        
        # Afficher la colonne principale
        render_main_column()
    
    with col2:
        # Afficher l'historique
        render_history_column()
    
    # Pied de page
    render_footer()

if __name__ == "__main__":
    main()