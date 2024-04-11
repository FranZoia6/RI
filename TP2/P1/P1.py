import re
import numpy as np
import math
from matplotlib import pyplot as plt
import sys

def count_terms(terms, doc):
    for d in doc:
        if d in terms:
            terms[d] += 1
        else:
            terms[d] =  1
    return terms

def get_arr(file):
    arr = []
    for line in file:
        line = line.lower()
        line = line.replace('id','')
        line = line.replace('keywords','')
        line = line.replace('\n','')
        line = re.sub(r'[^a-z0-9(),:]','', line)
        ar =  line.split(":")
        if len(ar) > 1:
            doc_array = ar[1].strip('()').split(',')
            arr.append(doc_array) 
    return arr

def m_booleano(doc,queri):
    mb = []
    for q in queri:
        if q in doc:
            mb.append(1)
        else:
            mb.append(0)
    return mb

def m_vectorial(doc,queri):
    df = [0] * 203
    idf = []
    tfifd = {}
    docN = 1
    cantDoc = len(doc)

    for terms in doc:
        for term in terms:
            df[int(term)] += 1 
    
    for i in df[1:]:  # Iniciar desde el índice 1 para omitir el término 0
        idf.append(math.log(cantDoc / (i + 1)))  # Se agrega 1 para evitar división por cero

    for terms in doc:
        for term in terms:
            for q in queri:
                if q in term:
                    if docN in tfifd:
                        tfifd[docN] +=idf[int(q)]
                    else:
                        tfifd[docN]= idf[int(q)]
        docN += 1
    return tfifd

path = sys.argv[1]#"ejemploProfRibeiroNeto/ejemploRibeiro/documentVector.txt"
with open(path) as file:
      doc = get_arr(file)  

path =  sys.argv[2]#"ejemploProfRibeiroNeto/ejemploRibeiro/queries.txt"
with open(path) as file:
      queri = get_arr(file)  
    
mb = []
nq = 1 #Numero de queri
print("Modelo booleano")
for q in queri:
    nd = 1 #Numero de documento
    print ('Queri N',nq)
    for d in doc:
        mb = (m_booleano(d,q))
        if np.all(np.array(mb) == 1):#np,any para traer todos los documentos que tengan por lo menos un 1
            print('Docu N', nd)
        nd+=1
    nq+=1

cantDoc = len(doc)
terms = {}
for d in doc:
    terms = count_terms(terms,d)

nq = 1
docR = {}
print("Modelo vectorial")
for q in queri:
    nd = 1 #Numero de documento
    docScore = m_vectorial(doc,q)
    sorted_docs = sorted(docScore.items(), key=lambda item: item[1], reverse=True)
    print('Queri n', nq)
    docR[nq] = [] 
    for docN, score in sorted_docs:
        print('Doc N', docN, 'score', score)
        docR[nq].append(docN)
    nq +=1

nq = 1
docR2 = {}
print("Consultas modificadas")
for q in queri:
    nd = 1 #Numero de documento
    docScore = m_vectorial(doc,q)
    sorted_docs = sorted(docScore.items(), key=lambda item: item[1], reverse=True)
    print('Queri n', nq)
    docR2[nq] = [] 
    for docN, score in sorted_docs:
        print('Doc N', docN, 'score', score)
        docR2[nq].append(docN)
    nq +=1