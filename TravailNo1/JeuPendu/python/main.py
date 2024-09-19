import requests

def get_word_from_api(api_url):
    try:
        # Faire une requête GET à l'API
        response = requests.get(api_url)
        
        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Si la réponse est au format JSON et contient un mot
            word = response.json()
            print(f"Mot récupéré depuis l'API : {word}")
        else:
            print(f"Erreur lors de la requête : {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête HTTP : {e}")

if __name__ == "__main__":
    # Exemple d'API qui retourne un mot aléatoire (vous pouvez remplacer cette URL par une autre)
    api_url = "https://random-word-api.herokuapp.com/word?length=10"
    
    # Récupérer le mot à partir de l'API
    get_word_from_api(api_url)
