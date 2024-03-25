import re
import os
import sys
import nltk 
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords
import time

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
def contadorPorter(terms, tokens):
    for token in tokens:
        stemmer = PorterStemmer()
        if stemmer.stem(token) in terms:
            terms[stemmer.stem(token)]["cf"] += 1
        else:
            terms[stemmer.stem(token)] = {"cf": 1}
    return terms

def contadorLancaster(terms, tokens):
    for token in tokens:
        stemmer = LancasterStemmer()
        if stemmer.stem(token) in terms:
            terms[stemmer.stem(token)]["cf"] += 1
        else:
            terms[stemmer.stem(token)] = {"cf": 1}
    return terms

def contadorPorter(terms, tokens):
    for token in tokens:
        stemmer = PorterStemmer()
        if stemmer.stem(token) in terms:
            terms[stemmer.stem(token)]["cf"] += 1
        else:
            terms[stemmer.stem(token)] = {"cf": 1}
    return terms

terms_lancaster = {}
file_location = sys.argv[1]
inicio = time.time()
for path in os.listdir(file_location):
    path = file_location + path 
    with open(path) as file:
        for linea in file:
            tokens=tokenizador(linea)
            terms_lancaster = contadorLancaster(terms_lancaster,tokens)
fin = time.time()
print("Lancaster", fin-inicio)

if len(sys.argv)>2:
    terms_lancaster = remove_sportsworld(terms_lancaster)

sorted_terms = sorted(terms_lancaster.items(), key=lambda item: item[1].get("cf", 0), reverse=True)

cant_terms = len(terms_lancaster)
print(cant_terms)
with open("terminosLancaster.txt", "w") as f:
    for term, info in sorted_terms:
        f.write(f"{term} {info['cf']}\n")

terms_porter = {}
file_location = sys.argv[1]
inicio = time.time()
for path in os.listdir(file_location):
    path = file_location + path 
    with open(path) as file:
        for linea in file:   
            tokens=tokenizador(linea)
            terms_porter = contadorPorter(terms_porter,tokens)
fin = time.time()
print("Porter", fin-inicio)

if len(sys.argv)>2:
    terms_porter = remove_sportsworld(terms_porter)

sorted_terms = sorted(terms_porter.items(), key=lambda item: item[1].get("cf", 0), reverse=True)


cant_terms = len(terms_porter)
print(cant_terms)
with open("terminosPorter.txt", "w") as f:
    for term, info in sorted_terms:
        f.write(f"{term} {info['cf']}\n")

