import re
import os
#Devuelve el texto formateado 
def tokenizador(text):
    return re.findall(r'\b\w+\b', text.lower())
#    intab = "áéíóú"
#    outtab = "aeiou"
#    str = text
#    trantab = str.maketrans(intab, outtab)
#    normalizado = str.translate(trantab).lower()
#    normalizado = re.sub(r'[^\w\s]','', normalizado)
#    return normalizado.split(" ")

#Cuanta las ocurrencia de cada termino en el texto    
def contador(terms, tokens):
    for token in tokens:
        if token in terms:
            terms[token]["cf"] += 1
        else:
            terms[token] = {"cf": 1}
    return terms

cant_files = len(os.listdir("RI-tknz-data"))
cant_tokens = 0
cant_terms = 0
terms = {}
for name in os.listdir("RI-tknz-data"):
    name = "RI-tknz-data/" + name
    termsAux = {}
    with open(name) as archivo:
        for linea in archivo:
            tokens=tokenizador(linea)
            termsAux = contador(termsAux,tokens)
            cant_tokens += len(tokens)
    for termAux in termsAux:
        if termAux in terms:
            terms[termAux]["cf"] += termsAux[termAux]["cf"]
            terms[termAux]["df"] += 1
        else:
            terms[termAux] = {"cf": termsAux[termAux]["cf"],"df": 1}

sorted_terms = sorted(terms.items(), key=lambda item: item[1].get("cf", 0), reverse=True)

cant_terms = len(terms)
with open("terminos.txt", "w") as f:
    for term, info in sorted_terms:
        f.write(f"{term} {info['cf']} {info['df']}\n")

print("Cantidad de archivos", cant_files  )
print("Cantidad de tokens:", cant_tokens )
print("Cantidad de terminos:", cant_terms )