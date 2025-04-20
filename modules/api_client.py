import random
import requests

def get_quote_from_api():
    """
    Récupère une citation aléatoire de l'API type.fit.
    
    Returns:
        tuple: (texte_citation, auteur, message_erreur)
            - texte_citation (str): Le texte de la citation
            - auteur (str): Le nom de l'auteur de la citation
            - message_erreur (str): Message d'erreur en cas de problème, None sinon
    """
    try:
        response = requests.get("https://type.fit/api/quotes", timeout=5)
        if response.status_code == 200:
            quotes = response.json()
            if quotes:
                random_quote = random.choice(quotes)
                return random_quote.get("text", ""), random_quote.get("author", "Inconnu"), None
        return "", "", "Impossible de récupérer les citations depuis l'API."
    except Exception as e:
        return "", "", f"Erreur lors de la récupération des citations: {e}" 