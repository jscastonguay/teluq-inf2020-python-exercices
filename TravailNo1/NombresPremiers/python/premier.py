import math
import time

def sieve_of_eratosthenes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False  # 0 et 1 ne sont pas premiers

    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    primes = [i for i in range(2, limit + 1) if is_prime[i]]
    print(primes)

if __name__ == "__main__":
    limit = 100000000  # Par exemple, trouver tous les nombres premiers jusqu'à 1 million

    start_time = time.time()
    sieve_of_eratosthenes(limit)
    end_time = time.time()

    print(f"Temps d'exécution en Python : {end_time - start_time} secondes")
