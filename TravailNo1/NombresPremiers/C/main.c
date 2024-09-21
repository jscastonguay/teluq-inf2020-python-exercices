#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

void sieve_of_eratosthenes(int limit) {
    int *is_prime = (int *)malloc((limit + 1) * sizeof(int));
    for (int i = 0; i <= limit; i++) {
        is_prime[i] = 1;  // On initialise tout à 1 (on considère tous les nombres comme premiers)
    }

    is_prime[0] = is_prime[1] = 0;  // 0 et 1 ne sont pas des nombres premiers

    for (int i = 2; i <= sqrt(limit); i++) {
        if (is_prime[i]) {
            for (int j = i * i; j <= limit; j += i) {
                is_prime[j] = 0;  // Eliminer les multiples de i
            }
        }
    }

    // Afficher tous les nombres premiers trouvés
    for (int i = 2; i <= limit; i++) {
        if (is_prime[i]) {
            printf("%d ", i);
        }
    }
    printf("\n");
    free(is_prime);
}

int main() {
    int limit = 100000000;  // Par exemple, trouver tous les nombres premiers jusqu'à 1 million

    clock_t start = clock();
    sieve_of_eratosthenes(limit);
    clock_t end = clock();

    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Temps d'exécution en C : %f secondes\n", time_spent);

    return 0;
}
