#include <stdio.h>

int main(int argc, char *argv[]) {
    // argc: nombre d'arguments passés au programme
    // argv: tableau de chaînes de caractères contenant les arguments

    if (argc > 1) {
        // Si un argument est passé, l'afficher
        printf("Hello, %s!\n", argv[1]);
    } else {
        // Si aucun argument n'est passé, afficher "Hello, World!"
        printf("Hello, World!\n");
    }

    return 0;
}