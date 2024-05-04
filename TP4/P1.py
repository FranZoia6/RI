import re
import math
import nltk
from nltk.corpus import stopwords
import os
import sys
import pyterrier as pt
import numpy as np
from scipy.stats import spearmanr



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

def contadorTerms(terms, tokens):
    for token in tokens:
        if token in terms:
            terms[token] += 1
        elif len(token)>2 and len(token)<20:
            terms[token] = 1
    return terms

def remove_sportsworld(terms):
    dic = {}
    stopsSp = set(stopwords.words('spanish'))
    stopsEn = set(stopwords.words('english'))
    for term in terms:
        if term not in stopsSp and term not in stopsEn:
            dic[term] = terms[term]
    return dic


directory = 'wiki-small/'
n = 1
archivos = []
for root, _, files in os.walk(directory):
    for file in files:
        if n % 100 != 0:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as html_file:
                termsAux = {}
                content = html_file.read()
                tokens =tokenizador(content)
                termsAux = contadorTerms(termsAux,tokens)
            archivos.append(f"{n} {file} {termsAux}")
        else: 
            with open('archivo_salida.txt', 'w', encoding='utf-8') as index:
                for archivo in archivos:
                    index.write(f"{archivo} \n")
                archivos = []
        n += 1

            