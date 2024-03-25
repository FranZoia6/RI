import re
import string
import numpy as np
import pandas as pd
import math
from matplotlib import pyplot as plt
from langdetect import detect
#Inicializar diccionarios
def tokenizador(text):
    text = text.lower()
    intab = "áéíóú"
    outtab = "aeiou"
    str = text
    trantab = str.maketrans(intab, outtab)
    normalizado = str.translate(trantab)
    normalizado = re.sub(r'[^a-z]','', normalizado)
    return normalizado


def entrenar(dic, path):
    name ="languageIdentificationData/" + path 
    with open(name, encoding='iso-8859-1') as archivo:
        text = archivo.read()
    text = tokenizador(text)
    for char in text:
        dic[char] +=1
    return dic

def entrenar2(dic, path):
    name ="languageIdentificationData/" + path 
    with open(name, encoding='iso-8859-1') as archivo:
        text = archivo.read()
    text = tokenizador(text)
    for i in range(0,len(text)-1):
        dic[text[i] + text[i+1]] +=1
    return dic
    

def cargarTest(dic,text):
    for char in list(string.ascii_lowercase):
        dic[char] = 0
    text = tokenizador(text)
    for char in text:
        dic[char] +=1
    return dic
    
def cargarTest2(dic,text):
    for element in dic:
        dic[element] = 0
    text = tokenizador(text)
    for i in range(0,len(text)-1):
        dic[text[i] + text[i+1]] +=1
    return dic

def cargar2():
    chars =set()
    with open("languageIdentificationData/training/English", encoding='iso-8859-1') as archivo:
        text_en = archivo.read()
    text = tokenizador(text_en)
    with open("languageIdentificationData/training/French", encoding='iso-8859-1') as archivo:
        text_fr = archivo.read()
    text += tokenizador(text_fr)
    with open("languageIdentificationData/training/Italian", encoding='iso-8859-1') as archivo:
        text_it = archivo.read()
    text += tokenizador(text_it)
    for i in range(0,len(text)-1):
        chars.add(text[i] + text[i+1])
    with open("languageIdentificationData/test", encoding='iso-8859-1') as archivo:
        text_test = archivo.read()
    text += tokenizador(text_test)
    for i in range(0,len(text)-1):
        chars.add(text[i] + text[i+1])
    return chars
    
en = {}
fr = {}
it = {}
test={}
resultado1=[]
resultado2= []
solution = []
resulado_langdetect = []


for letra in list(string.ascii_lowercase):
    en[letra] = 0
    fr[letra] = 0
    it[letra] = 0
    test[letra] =0

en = entrenar(en,"training/English")
fr = entrenar(fr,"training/French")
it = entrenar(it,"training/Italian")
array_en = np.array(list(en.values()))
array_fr = np.array(list(fr.values()))
array_it = np.array(list(it.values()))

chars = cargar2()
en2 = {}
fr2 = {}
it2 ={}
test2 ={}
for element in chars:
    en2[element] = 0
    fr2[element] = 0
    it2[element] = 0
    test2[element] =0

en2 = entrenar2(en2,"training/English")
fr2 = entrenar2(fr2,"training/French")
it2 = entrenar2(it2,"training/Italian")
array_en2 = np.array(list(en2.values()))
array_fr2 = np.array(list(fr2.values()))
array_it2 = np.array(list(it2.values()))



with open("languageIdentificationData/test", encoding='iso-8859-1') as archivo:
    for linea in archivo:
        test = cargarTest(test,linea)
        array_test = np.array(list(test.values()))
        en_cor = np.corrcoef(array_en,array_test)[0][1]
        fr_cor = np.corrcoef(array_fr,array_test)[0][1]
        it_cor = np.corrcoef(array_it,array_test)[0][1] 
        match np.argmax([en_cor, fr_cor, it_cor]):
            case 0:
                resultado1.append("English")
            case 1:
                resultado1.append("French")
            case 2:
                resultado1.append("Italian")

        test2 = cargarTest2(test2,linea)
        array_test2 = np.array(list(test2.values()))
#        matriz = {"en":array_en2,"fr":array_fr2,"it":array_it2,"test":array_test2 }
#        df = pd.DataFrame(matriz)
        en_cor2 = np.corrcoef(array_en2,array_test2)[0][1]
        fr_cor2 = np.corrcoef(array_fr2,array_test2)[0][1]
        it_cor2 = np.corrcoef(array_it2,array_test2)[0][1] 
        match np.argmax([en_cor2, fr_cor2, it_cor2]):
            case 0:
                resultado2.append("English")
            case 1:
                resultado2.append("French")
            case 2:
                resultado2.append("Italian")
        idioma = detect(linea)
        if idioma == "en":
            resulado_langdetect.append("English")
        elif idioma == "it":
            resulado_langdetect.append("Italian")
        elif idioma == "fr":
            resulado_langdetect.append("French")
        else:
            resulado_langdetect.append("Idioma no detectado")

solutions = []
with open("languageIdentificationData/solution", encoding='iso-8859-1') as archivo:
    for linea in archivo:
        linea = re.sub(r'[^a-zA-Z]','', linea)
        linea = linea.split(" ")
        solutions.append(linea[0])

correctos1 = 0
correctos2 = 0
correctos_langdetect = 0
for i in range(len(solutions)):
#    print(solutions[i])
    if solutions[i] == resultado1[i]:
        correctos1+=1
    if solutions[i] == resultado2[i]:
        correctos2+=1
    
    if solutions[i] == resulado_langdetect[i]:
        correctos_langdetect+=1
     
resultado1.append(correctos1)
resultado2.append(correctos2)
resulado_langdetect.append(correctos_langdetect)

matriz = {"resultado1":resultado1,"Resultado 2":resultado2,"Langdetect":resulado_langdetect}
df = pd.DataFrame(matriz)
print(df)

        
