import re
import os
import sys
import nltk
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords
#Devuelve el texto formateado 
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
        stemmer = LancasterStemmer()
        if stemmer.stem(token) in terms:
            terms[stemmer.stem(token)]["cf"] += 1
        else:
            terms[stemmer.stem(token)] = {"cf": 1}
    return terms
file_location = sys.argv[1]
terms = {}
for path in os.listdir(file_location):
    path = file_location + path 
    with open(path) as file:
        for linea in file:
            tokens = tokenizador(linea)
            terms= contador(terms,tokens)

if len(sys.argv)>2:
    terms = remove_sportsworld(terms)

sorted_terms = sorted(terms.items(), key=lambda item: item[1].get("cf", 0), reverse=True)

with open("terminosP3.txt", "w") as f:
    for term, info in sorted_terms:
        f.write(f"{term} {info['cf']}\n")



