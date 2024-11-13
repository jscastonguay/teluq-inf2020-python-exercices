import re

texte1 = "zoto Ceci est un texte Ceci"

#r = re.match(r"Ceci est",  texte1).group()
r = re.search(r"^[z]",  texte1)
print(r)

r = re.search(r"e",  texte1)
print(r)

texte1 = "Ceci est Python, voilà"

r = re.search(r"(Python)",  texte1)
print(r)

texte1 = "xrty"

r = re.search(r"^(x..y)",  texte1)
print(r)

texte1 = "123"
r = re.search(r"^(123)$",  texte1)
print(r)

texte1 = "Ceci est Python, voilà"
r = re.search(r"^[A-Z]",  texte1)
print(r)

texte1 = "123456Toto"
r = re.search(r"^[0-9]*",  texte1)
print(r)

texte1 = "toto"
r = re.search(r"^[0-9]+",  texte1)
print(r)

texte1 = "MAGuscule"
r = re.search(r"^[A-Z]+",  texte1)
print(r)

texte1 = "MAG123"
r = re.search(r"^[A-Z]{3}",  texte1)
print(r)