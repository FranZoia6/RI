import itertools
import re
import math
import struct
import nltk
from nltk.corpus import stopwords
import os
import sys
import pyterrier as pt
import numpy as np
from scipy.stats import spearmanr
import timeit
import time
from bs4 import BeautifulSoup
import pickle

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

def counter_terms(tokens):
    terms = {}
    for token in tokens:
        if token in terms:
            terms[token] += 1
        elif len(token)>2:
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


def create_dictionary(directory):
    dictionary = {}
    termId = 1
    for root,_,files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as html_file:
                soup = BeautifulSoup(html_file, 'html.parser')
                content = soup.get_text(separator=' ')
                tokens =tokenizador(content)
                for token in tokens:
                    if not token in dictionary:
                        dictionary[token] = termId
                        termId += 1
    return dictionary

def sort_vocabulary(vocabulary):
    sort = sorted(vocabulary, key=lambda x: x[0])
    return sort

def dump_partial_index(sorted_partial_index, filename):
    byte_data = struct.pack(f">{len(sorted_partial_index)}I", *sorted_partial_index)
    with open(filename, 'wb') as index_file:
        index_file.write(byte_data)

def index(memory,directory,count,dictionary):
    vocabulary = []
    reference  = []
    terms = []
    docID = 1
    file_b = 'index/'
    index_id = 1
    for root,_,files in os.walk(directory):
        for file in files:
            if docID % memory !=0:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as html_file:
                    soup = BeautifulSoup(html_file, 'html.parser')
                    content = soup.get_text(separator=' ')
                    tokens =tokenizador(content)
                    terms = counter_terms(tokens)
                    for term, frecuency in terms.items():
                        term_id = dictionary[term]
                        item = (term_id,docID,frecuency)
                        vocabulary.append(item)
                reference.append(f"{docID}+{file}")

            else: 
                path_binario = file_b + str(index_id) + ".bin"
                sort = sort_vocabulary(vocabulary)
                sorted_partial_index = list(itertools.chain(*sort))
                dump_partial_index(sorted_partial_index, path_binario)
                index_id += 1
            docID+=1


def marge(directory_index,dictionary ):
    index = []
    vocabulary = {}
    formato = 'I'
    pointer = 0
    for term, termId in dictionary.items():
        vocabulary[termId] = {"term": term, "df": 0, "pointer": -1}
    for root,_,files in os.walk(directory_index):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as binary_file:
                byte_data = binary_file.read()
            format_string = f">{len(byte_data) // 4}I"
        unpacked_data = struct.unpack(format_string, byte_data)
        grouped_data = [(unpacked_data[i], unpacked_data[i+1], unpacked_data[i+2]) for i in range(0, len(unpacked_data), 3)]
        for term in grouped_data:                
            termId = term[0]
            docId = term[1]
            if vocabulary:
                vocabulary[termId]["df"] += 1
                vocabulary[termId]["pointer"] = pointer
            index.append(docId)
            pointer += 1
    print(index)
        





path = sys.argv[1]
directory = 'collection_test_ER2/'
n = 1
count = sys.argv[3].lower() == 'true'
dictionary = create_dictionary(directory)
marge("index/",dictionary)
#start_time = time.time()
#index(100,directory, count,dictionary)
#end_time = time.time()
# time_result = end_time -  start_time
# print(f"Tiempo resultado con n = 100, {time_result}s")
# os.remove('index.txt')
# os.remove('reference.txt') 
# start_time = time.time()
# index_frequently(200,directory, count)
# end_time = time.time()
# time_result = end_time -  start_time
# print(f"Tiempo resultado con memory de 200 {time_result}")
# os.remove('index.txt')
# os.remove('reference.txt')
# start_time = time.time()
# index_frequently(1000,directory, count)
# end_time = time.time()
# time_result = end_time -  start_time
# print(f"Tiempo resultado con memory de 1000 {time_result}")
# os.remove('index.txt')
# os.remove('reference.txt')
# start_time = time.time()
# index_frequently(1500,directory, count)
# end_time = time.time()
# time_result = end_time -  start_time
# print(f"Tiempo resultado con memory de 1500 {time_result}")
# os.remove('index.txt')
# os.remove('reference.txt')

