#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Fonction pour vérifier si un caractère est une lettre alphabétique
int is_letter(char c) {
    return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z');
}

// Fonction pour normaliser un caractère en majuscule
char normalize_char(char c) {
    if (c >= 'a' && c <= 'z') {
        return c - 'a' + 'A';
    }
    return c;
}

// Fonction qui réalise le chiffrement/déchiffrement de Vigenère
void vigenere_cipher(FILE *input_file, FILE *output_file, char *key, int encrypt) {
    int key_len = strlen(key);
    int j = 0;  // Pour parcourir la clé

    // Normaliser la clé en majuscules
    for (int i = 0; i < key_len; i++) {
        key[i] = normalize_char(key[i]);
    }

    char c;
    while ((c = fgetc(input_file)) != EOF) {
        if (is_letter(c)) {
            char normalized_c = normalize_char(c);
            int offset = normalized_c - 'A';
            int key_offset = key[j % key_len] - 'A';

            char result;
            if (encrypt) {
                // Chiffrement : additionner l'offset de la clé
                result = (offset + key_offset) % 26 + 'A';
            } else {
                // Déchiffrement : soustraire l'offset de la clé
                result = (offset - key_offset + 26) % 26 + 'A';
            }

            fputc(result, output_file);
            j++;  // Avancer dans la clé seulement pour les lettres
        } else {
            fputc(c, output_file);  // Garder les autres caractères inchangés
        }
    }
}

int main() {
    char key[100];
    int choice;
    char input_file_name[100];
    char output_file_name[100];

    // Demander le nom des fichiers source et de sortie
    printf("Entrez le nom du fichier source : ");
    scanf("%s", input_file_name);

    printf("Entrez le nom du fichier de sortie : ");
    scanf("%s", output_file_name);

    // Demander la clé
    printf("Entrez la clé : ");
    scanf("%s", key);

    // Choisir entre chiffrement et déchiffrement
    printf("Entrez 1 pour chiffrer ou 0 pour déchiffrer : ");
    scanf("%d", &choice);

    // Ouvrir les fichiers
    FILE *input_file = fopen(input_file_name, "r");
    FILE *output_file = fopen(output_file_name, "w");

    if (input_file == NULL || output_file == NULL) {
        printf("Erreur lors de l'ouverture des fichiers.\n");
        return 1;
    }

    // Appliquer le chiffrement ou déchiffrement
    vigenere_cipher(input_file, output_file, key, choice);

    // Fermer les fichiers
    fclose(input_file);
    fclose(output_file);

    printf("Opération terminée avec succès.\n");

    return 0;
}
