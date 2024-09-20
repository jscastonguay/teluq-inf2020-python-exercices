#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <ctype.h>

// Fonction de rappel pour stocker la réponse de l'API dans un tampon
static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t totalSize = size * nmemb;
    strncat((char *)userp, (char *)contents, totalSize);
    return totalSize;
}

// Fonction pour récupérer un mot aléatoire depuis une API web
int get_random_word(char *word, size_t size) {
    CURL *curl;
    CURLcode res;
    char response[4096] = "";  // Tampon pour stocker la réponse de l'API
    const char *url = "https://random-word-api.herokuapp.com/word?length=8";  // URL de l'API

    curl = curl_easy_init();  // Initialiser libcurl
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url);  // Configurer l'URL de la requête
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);  // Configurer la fonction de rappel
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, response);  // Stocker la réponse dans le tampon

        res = curl_easy_perform(curl);  // Exécuter la requête

        if(res != CURLE_OK) {
            fprintf(stderr, "Erreur lors de la requête curl: %s\n", curl_easy_strerror(res));
            curl_easy_cleanup(curl);
            return 0;  // Retourner une erreur
        }

        curl_easy_cleanup(curl);  // Nettoyer curl

        // Extraire le mot de la réponse JSON (ex. ["mot"])
        sscanf(response, "[\"%[^\"]\"]", word);
        return 1;  // Succès
    }
    return 0;  // Échec
}

// Fonction pour afficher l'état actuel du mot (avec les lettres devinées)
void display_word_state(char *word, int *correct_guesses) {
    for (int i = 0; i < strlen(word); i++) {
        if (correct_guesses[i]) {
            printf("%c ", word[i]);
        } else {
            printf("_ ");
        }
    }
    printf("\n");
}

// Fonction pour vérifier si le mot est entièrement deviné
int is_word_guessed(char *word, int *correct_guesses) {
    for (int i = 0; i < strlen(word); i++) {
        if (!correct_guesses[i]) {
            return 0;
        }
    }
    return 1;
}

// Fonction principale du jeu du pendu
void play_hangman(char *word) {
    int len = strlen(word);
    int correct_guesses[len];  // Tableau pour stocker les bonnes lettres trouvées
    memset(correct_guesses, 0, len * sizeof(int));  // Initialiser toutes les valeurs à 0

    int attempts_left = 6;  // Nombre d'essais avant de perdre
    char guess;
    int already_guessed;
    int found;

    printf("Bienvenue au jeu du Pendu !\n");
    printf("Le mot à deviner contient %d lettres.\n\n", len);

    while (attempts_left > 0) {
        display_word_state(word, correct_guesses);  // Afficher l'état actuel du mot
        printf("Il vous reste %d tentatives. Entrez une lettre : ", attempts_left);
        scanf(" %c", &guess);  // Lire la lettre proposée par le joueur
        guess = tolower(guess);  // Normaliser en minuscule

        // Vérifier si la lettre a déjà été devinée
        already_guessed = 0;
        for (int i = 0; i < len; i++) {
            if (correct_guesses[i] && word[i] == guess) {
                already_guessed = 1;
                break;
            }
        }
        if (already_guessed) {
            printf("Vous avez déjà deviné cette lettre !\n");
            continue;
        }

        // Vérifier si la lettre est dans le mot
        found = 0;
        for (int i = 0; i < len; i++) {
            if (word[i] == guess) {
                correct_guesses[i] = 1;
                found = 1;
            }
        }

        if (!found) {
            attempts_left--;  // Réduire le nombre d'essais si la lettre n'est pas dans le mot
            printf("Mauvais choix !\n");
        } else {
            printf("Bonne lettre !\n");
        }

        // Vérifier si tout le mot est deviné
        if (is_word_guessed(word, correct_guesses)) {
            printf("Félicitations ! Vous avez deviné le mot : %s\n", word);
            return;
        }
    }

    printf("Vous avez perdu ! Le mot était : %s\n", word);
}

int main() {
    char word[100];  // Tampon pour stocker le mot récupéré

    // Récupérer un mot aléatoire depuis l'API
    if (get_random_word(word, sizeof(word))) {
        play_hangman(word);  // Jouer au pendu avec le mot récupéré
    } else {
        printf("Impossible de récupérer un mot depuis l'API.\n");
    }

    return 0;
}
