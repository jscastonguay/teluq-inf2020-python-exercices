#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

// Fonction de rappel (callback) pour stocker la réponse de l'API
static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t totalSize = size * nmemb;
    strcat((char *)userp, (char *)contents);
    return totalSize;
}

int main() {
    CURL *curl;
    CURLcode res;
    char response[4096] = ""; // Tampon pour stocker la réponse de l'API

    // URL de l'API (exemple d'une API qui renvoie un mot aléatoire)
    const char *url = "https://random-word-api.herokuapp.com/word?length=10";  // Remplacez par l'URL de votre API

    // Initialiser curl
    curl = curl_easy_init();
    if(curl) {
        // Configurer l'URL à laquelle la requête doit être envoyée
        curl_easy_setopt(curl, CURLOPT_URL, url);

        // Configurer la fonction de rappel pour écrire les données de la réponse
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        
        // Passer le tampon pour stocker la réponse
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)response);

        // Exécuter la requête
        res = curl_easy_perform(curl);

        // Vérifier si la requête a réussi
        if(res != CURLE_OK) {
            fprintf(stderr, "Erreur lors de l'exécution de curl: %s\n", curl_easy_strerror(res));
        } else {
            // Afficher la réponse reçue (le mot renvoyé par l'API)
            printf("Réponse de l'API: %s\n", response);
        }

        // Nettoyer curl
        curl_easy_cleanup(curl);
    }

    return 0;
}
