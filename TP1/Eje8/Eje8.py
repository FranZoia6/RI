import re
import sys

def tokenizador(text):
    text = text.lower()
    intab = "áéíóú"
    outtab = "aeiou"
    str = text
    trantab = str.maketrans(intab, outtab)
    normalizado = str.translate(trantab)
    normalizado = re.sub(r'[^a-z0-9 ]','', normalizado)
    tokens = normalizado.split(" ")
    if "" in tokens:
        while "" in tokens:
            tokens.remove("")
    return tokens

def contador(terms, tokens,i):
    for token in tokens:
        if token in terms:
            terms[token]["cf"] += 1
        else:
            terms[token] = {"cf": 1}
            i +=1
    return terms, i

terms = {}
tokens_line = []
i = 0
cant_line = 0
file_location = sys.argv[1]
with open(file_location) as archivo:
    for linea in archivo:
        tokens=tokenizador(linea)
        terms, i = contador(terms,tokens,i)
        tokens_line.append(i)
        cant_line +=1
sorted_terms = sorted(terms.items(), key=lambda item: item[1].get("cf", 0), reverse=True)
terminos_totales = sum(terms[term]["cf"] for term in terms)

with open("terminos.txt", "w") as f:
    for term in tokens_line:
        f.write(f"{term}\n")
    f.write(f"terminos\n")
    f.write(f"{cant_line}")
