nbChiffre = 1
while nbChiffre < 10:
    nb = 1
    exp = nbChiffre - 1
    total = 0
    while nb <= nbChiffre:
        total += nb * (10 ** exp)
        nb += 1
        exp -= 1
    print(total)
    nbChiffre += 1