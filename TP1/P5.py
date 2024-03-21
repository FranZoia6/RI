import re
import string
import numpy as np
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


def entrenar(dic, len):
    name ="languageIdentificationData/" + len 
    with open(name, 'rb') as archivo:
        text = archivo.read()
    text = tokenizador(text.decode('utf-8', errors='ignore'))
    for char in text:
        dic[char] +=1
    return dic

def cargar(dic,text):
    text = tokenizador(text.decode('utf-8', errors='ignore'))
    for char in text:
        dic[char] +=1
    return dic

en = {}
fr = {}
it = {}
test={}
for letra in list(string.ascii_lowercase):
    en[letra] = 0
    fr[letra] = 0
    it[letra] = 0
    test[letra] = 0
#Entrenar diccionarios
en = entrenar(en,"training/English")
fr = entrenar(fr,"training/French")
it = entrenar(it,"training/Italian")
array_en = np.array(list(en.values()))
array_fr = np.array(list(fr.values()))
array_it = np.array(list(it.values()))
with open("languageIdentificationData/test", 'rb') as archivo:
    for linea in archivo:
        test = cargar(test,linea)
        array_test = np.array(list(test.values()))
#        matriz = np.array([array_en,array_fr,array_it,array_test])
#        correlacion =  np.corrcoef(matriz)
#        en_cor =correlacion[0][3]
#        fr_cor =correlacion[1][3]
#        it_cor =correlacion[2][3]
        en_cor = np.corrcoef(array_en,array_test)[0][1]
        fr_cor = np.corrcoef(array_fr,array_test)[0][1]
        it_cor = np.corrcoef(array_it,array_test)[0][1]       
        if en_cor>fr_cor and en_cor>it_cor:
            print("Ingles")
        if fr_cor>en_cor and fr_cor>it_cor:
            print("Frances")
        if it_cor>fr_cor and it_cor>en_cor:
            print("italiano")

