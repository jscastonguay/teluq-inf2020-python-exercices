import requests
import random

# Fonction pour récupérer un mot aléatoire depuis une API web
def get_random_word():
    try:
        response = requests.get("https://random-word-api.herokuapp.com/word?length=8")
        if response.status_code == 200:
            word = response.json()[0]  # Récupérer le premier mot du tableau JSON
            return word.lower()
        else:
            print(f"Erreur lors de la requête : {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la connexion à l'API : {e}")
        return None

# Fonction pour afficher l'état actuel du mot (avec les lettres devinées)
def display_word_state(word, correct_guesses):
    displayed_word = ""
    for letter in word:
        if letter in correct_guesses:
            displayed_word += letter + " "
        else:
            displayed_word += "_ "
    print(displayed_word.strip())

# Fonction pour vérifier si le mot est entièrement deviné
def is_word_guessed(word, correct_guesses):
    return all(letter in correct_guesses for letter in word)

# Fonction principale du jeu du pendu
def play_hangman(word):
    attempts_left = 6
    correct_guesses = set()
    wrong_guesses = set()

    print("Bienvenue au jeu du Pendu !")
    print(f"Le mot à deviner contient {len(word)} lettres.\n")

    while attempts_left > 0:
        display_word_state(word, correct_guesses)
        print(f"Il vous reste {attempts_left} tentatives.")
        guess = input("Entrez une lettre : ").lower()

        # Vérifier si l'utilisateur a entré une seule lettre
        if len(guess) != 1 or not guess.isalpha():
            print("Veuillez entrer une seule lettre.")
            continue

        if guess in correct_guesses or guess in wrong_guesses:
            print("Vous avez déjà deviné cette lettre !")
            continue

        # Vérifier si la lettre est dans le mot
        if guess in word:
            print("Bonne lettre !")
            correct_guesses.add(guess)
        else:
            print("Mauvais choix !")
            wrong_guesses.add(guess)
            attempts_left -= 1

        # Vérifier si tout le mot est deviné
        if is_word_guessed(word, correct_guesses):
            print(f"Félicitations ! Vous avez deviné le mot : {word}")
            return

    # Si le joueur a épuisé toutes ses tentatives
    print(f"Vous avez perdu ! Le mot était : {word}")

if __name__ == "__main__":
    # Récupérer un mot aléatoire depuis l'API
    word = get_random_word()

    if word:
        # Jouer au pendu avec le mot récupéré
        play_hangman(word)
    else:
        print("Impossible de récupérer un mot depuis l'API.")
