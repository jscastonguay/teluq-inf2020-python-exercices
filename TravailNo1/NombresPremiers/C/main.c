#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>

void sieve_of_eratosthenes(int limit) {
    int *is_prime = (int *)malloc((limit + 1) * sizeof(int));
    for (int i = 0; i <= limit; i++) {
        is_prime[i] = 1;  // On initialise tout à 1 (on considère tous les nombres comme premiers)
    }

    is_prime[0] = is_prime[1] = 0;  // 0 et 1 ne sont pas des nombres premiers

    for (int i = 2; i <= sqrt(limit); i++) {
        if (is_prime[i]) {
            for (int j = i * i; j <= limit; j += i) {
                is_prime[j] = 0;  // Éliminer les multiples de i
            }
        }
    }

    // Afficher tous les nombres premiers trouvés (peut être commenté si besoin)
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

    struct timeval start, end;
    gettimeofday(&start, NULL);  // Obtenir le temps de départ

    sieve_of_eratosthenes(limit);

    gettimeofday(&end, NULL);  // Obtenir le temps de fin

    // Calculer le temps écoulé en secondes et microsecondes
    long seconds = (end.tv_sec - start.tv_sec);
    long microseconds = ((seconds * 1000000) + end.tv_usec) - (start.tv_usec);
    double elapsed = microseconds / 1000000.0;

    printf("Temps d'exécution en C : %.6f secondes\n", elapsed);

    return 0;
}
