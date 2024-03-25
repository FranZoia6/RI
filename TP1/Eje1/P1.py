import re
import os
import sys
import nltk
from nltk.corpus import stopwords
#Devuelve el texto formateado 
def tokenizador(text,dtokens):
    tokens=text.split(" ")
    for token in tokens:
        if token in dtokens:
            dtokens[token]["cf"] += 1
        else:
            dtokens[token] = {"cf": 1}
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
    return tokens, dtokens

def remove_sportsworld(terms):
    dic = {}
    stopsSp = set(stopwords.words('spanish'))
    stopsEn = set(stopwords.words('english'))
    for term in terms:
        if term not in stopsSp and term not in stopsEn:
            dic[term] = terms[term]
    return dic



#Cuanta las ocurrencia de cada termino en el texto    
def contador(terms, tokens):
    for token in tokens:
        if token in terms:
            terms[token]["cf"] += 1
        elif len(token)>2 and len(token)<15:
            terms[token] = {"cf": 1}
    return terms
file_location = sys.argv[1]
cant_files = len(os.listdir(file_location))
cant_terms = 0
cant_min_tokens = 0
cant_max_tokens = 0
cant_min_terms = 0
cant_max_terms = 0
terms_length = 0
unique_terms = 0
terms = {}
dtokens = {}
for path in os.listdir(file_location):
    path = file_location + path
    termsAux = {}
    cant_tokens_doc = 0
    with open(path) as file:
        for linea in file:
            tokens, dtokens=tokenizador(linea,dtokens)
            termsAux = contador(termsAux,tokens)
            cant_tokens_doc += len(tokens)
        if cant_tokens_doc> cant_max_tokens:
            cant_max_tokens = cant_tokens_doc
            cant_max_terms = len(termsAux)
        if cant_min_tokens>cant_tokens_doc or cant_min_tokens == 0:
            cant_min_tokens = cant_tokens_doc
            cant_min_terms = len(termsAux)
    for termAux in termsAux:
        if termAux in terms:
            terms[termAux]["cf"] += termsAux[termAux]["cf"]
            terms[termAux]["df"] += 1
        else:
            terms[termAux] = {"cf": termsAux[termAux]["cf"],"df": 1}

if len(sys.argv)>2:
    terms = remove_sportsworld(terms)

sorted_terms = sorted(terms.items(), key=lambda item: item[1].get("cf", 0), reverse=True)

cant_terms =  len(terms)
with open("terminos.txt", "w") as f:
    for term, info in sorted_terms:
        f.write(f"{term} {info['cf']} {info['df']}\n")
        if info['cf'] == 1:
            unique_terms += 1
        terms_length += len(term)
cant_tokens = sum([dtokens[term]["cf"] for term in dtokens])
with open("estadisticas.txt", "w") as f:
    f.write(f"Cantidad de archivos {cant_files} \n")
    f.write(f"Cantidad de tokens:, {cant_tokens} \n")
    f.write(f"Cantidad de terminos: {cant_terms} \n")
    f.write(f"promedio de tokens y terminos en los documentos {cant_tokens/cant_files,cant_terms/cant_files}\n")
    f.write(f"Largo promedio de un término {terms_length/cant_terms}\n")
    f.write(f"Cantidad de tokens del documento más corto y del más largo {cant_max_tokens} {cant_min_tokens}\n")
    f.write(f"Cantidad de tokens del documento más corto y del más largo {cant_max_terms} {cant_min_tokens}\n")
    f.write(f"Cantidad de términos que aparecen sólo 1 vez en la colección {unique_terms}\n")

higher_frequency = sorted_terms[:10]
lower_frequency = sorted_terms[-10:] 
with open("frecuencias.txt", "w") as f:
    f.write(f"La lista de los 10 términos más frecuentes\n")
    for term, info in higher_frequency:
        f.write(f"{term} {info['cf']} \n")
    f.write(f"La lista de los 10 términos menos frecuentes\n")
    for term, info in lower_frequency:
        f.write(f"{term} {info['cf']} \n")



