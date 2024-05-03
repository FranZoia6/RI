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

def get_idf(terms):
    idf = {}
    for term in terms:
        idf[term] = math.log(terms[term]["cf"]/ terms[term]["df"])
    return idf

def get_score(index,queriText, idf):
    score = {}
    queri = tokenizador(queriText)
    for q in queri:
        for path,terms in index.items():
            if q in terms:
                tf = terms[q] / len(terms)
                if path in score:
                    score[path] +=  tf*idf[q]
                else:
                    score[path] = tf*idf[q] 
    return score
        

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

def enumerate_html_files(directory):
    document_id = 1
    index = {}
    terms = {}
    for root, _, files in os.walk(directory):
        for file in files:
            dic = {}
            tokens = {}
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as html_file:
                termsAux = {}
                content = html_file.read()
                tokens =tokenizador(content)
                dic = contadorTerms(dic,tokens)
                termsAux = contadorTerms(termsAux,tokens)
                dic = remove_sportsworld(dic)
                index[file_path] = dic
                for term, aux in termsAux.items():
                    if term in terms:
                        terms[term]["cf"] += aux
                        terms[term]["df"] += 1
                    else:
                        terms[term] = {"cf": aux, "df": 1}
    return index, terms

root_dir = sys.argv[1] #"wiki-small/"
index,terms = enumerate_html_files(root_dir)
idf = get_idf(terms)
queri = 'software'
score=get_score(index,queri,idf)

sorted_terms = sorted(score.items(), key=lambda item: item[1], reverse=True)

rankTfIdf = [tupla[0] for tupla in sorted_terms]

# Eje7


if not pt.started():
    pt.init()

indexer = pt.FilesIndexer("./index", verbose=True, overwrite=True, meta={"docno":20, "filename":512})
indexref =indexer.index(root_dir)
index = pt.IndexFactory.of(indexref)

br =  pt.BatchRetrieve(index, num_results=50, wmodel="TF_IDF", metadata=["filename"])
results = br.search(queri)

tfidf = np.array(results["filename"])


spearmancoefficient, datos = spearmanr(tfidf[:5], rankTfIdf[:5])
print("Coeficiente de correlación de Spearman 5 elementos:", spearmancoefficient,)

spearmancoefficient, datos = spearmanr(tfidf[:10], rankTfIdf[:10])
print("Coeficiente de correlación de Spearman 10 elementos:", spearmancoefficient,)
