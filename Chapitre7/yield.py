def fibonacci(max: int):
    n1 = 1
    n2 = 1
    n = n1 + n2
    while n < max:
        n = n1 + n2
        n2 = n1
        n1 = n
        yield n

    
for nb in fibonacci(100):
    print(nb)