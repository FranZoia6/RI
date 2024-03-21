import re
import os
import numpy as np
import pandas as pd

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

def contador(terms, tokens):
    for token in tokens:
        if token in terms:
            terms[token]["cf"] += 1
        else:
            terms[token] = {"cf": 1}
    return terms

terms = {}
for name in os.listdir("RI-tknz-data"):
    name = "RI-tknz-data/" + name
    termsAux = {}
    with open(name) as archivo:
        for linea in archivo:
            tokens=tokenizador(linea)
            termsAux = contador(termsAux,tokens)
    for termAux in termsAux:
        if termAux in terms:
            terms[termAux]["cf"] += termsAux[termAux]["cf"]
            terms[termAux]["df"] += 1
        else:
            terms[termAux] = {"cf": termsAux[termAux]["cf"],"df": 1}

sorted_terms = sorted(terms.items(), key=lambda item: item[1].get("cf", 0), reverse=True)
datos={"words":[],"rank":[],"freq":[]}
rank = 1
with open("terminosQuijote.txt", "w") as f:
    for term, info in sorted_terms:
        datos["words"].append(term)
        datos["rank"].append(rank)
        datos["freq"].append(info['cf'])
        rank += 1
        f.write(f"{term} {info['cf']} {info['df']}\n")

fit = np.polyfit(np.log(datos["rank"]),np.log(datos["freq"]),1)
df = pd.DataFrame(datos)
print(fit)
