import itertools
import re
import struct
import os
import sys
import time
from bs4 import BeautifulSoup
import pickle
import shutil

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
        else:
            terms[token] = 1
    return terms


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



def partial_index(memory,directory,dictionary):
    vocabulary = []
    reference  = {}
    terms = []
    docID = 0
    file_b = 'index/'
    index_id = 1
    for root,_,files in os.walk(directory):
        for file in files:
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
            reference[docID] = file
            if docID % memory ==0:
                path_binario = file_b + str(index_id) + ".bin"
                sort = sort_vocabulary(vocabulary)
                sorted_partial_index = list(itertools.chain(*sort))
                dump_partial_index(sorted_partial_index, path_binario)
                vocabulary.clear()
                with open('reference.pickle','ab') as reference_file:
                    pickle.dump(reference, reference_file)
                index_id += 1
                

            docID+=1
    if len(vocabulary)>0: 
        path_binario = file_b + str(index_id) + ".bin"
        sort = sort_vocabulary(vocabulary)
        sorted_partial_index = list(itertools.chain(*sort))
        dump_partial_index(sorted_partial_index, path_binario)
    with open('reference.pickle','wb') as reference_file:
        pickle.dump(reference, reference_file)


def marge(directory_index,dictionary,count ):
    index = []
    vocabulary = {}
    pointer = 1
    unsorted_index = []
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
            unsorted_index.extend(grouped_data)
    sort = sort_vocabulary(unsorted_index)
    for term in sort:                
        termId, docId, frequency = term
        vocabulary[termId]["df"] += 1
        vocabulary[termId]["pointer"] = pointer - vocabulary[termId]["df"]
        pointer += 1
        if count:
            index.append((docId,frequency))
        else:
            index.append(docId)
    path_binario = "index.bin"
    if count:
        sorted_index = list(itertools.chain(*index))
        dump_partial_index(sorted_index, path_binario)
    else:
        dump_partial_index(index, path_binario)
    return vocabulary


def read_index(directory, df, pointer,count):
    if count:
        seek = pointer * 8
        cant = df * 8
    else:
        seek = pointer * 4
        cant = df * 4
    with open(directory, 'rb') as binary_file:
        binary_file.seek(seek)
        byte_data = binary_file.read(cant)
    format_string = f">{len(byte_data) // 4}I"
    unpacked_data = struct.unpack(format_string, byte_data)
    if count:
        grouped_data = [(unpacked_data[i], unpacked_data[i+1]) for i in range(0, len(unpacked_data), 2)]
        print(grouped_data)
    else:
        print(sorted(unpacked_data))    
    print(len(unpacked_data))

def search(term,dictionary,vocabulary,directory,count):
    if term in dictionary:
        termId = dictionary[term]
        df = vocabulary[termId]['df']
        pointer = vocabulary[termId]['pointer']
        read_index(directory, df, pointer,count)

def save_pickle(structure, name):
    with open(name,'wb') as file:
        pickle.dump(structure, file)

n = int(sys.argv[1])
path = sys.argv[2]
count = sys.argv[3].lower() == 'true'
term = sys.argv[4]
directory =  "collection_test_ER2" #'wiki-small/'
start_time = time.time()
dictionary = create_dictionary(directory)
end_time = time.time()
time_result = end_time -  start_time
print(f"Tiempo en crear el diccionario, {time_result}s")
start_time = time.time()
partial_index(n,directory,dictionary)
end_time = time.time()
time_result = end_time -  start_time
print(f"Tiempo indexacion con n = 1000, {time_result}s")
start_time = time.time()
vocabulary = marge("index/",dictionary,count)
end_time = time.time()
time_result = end_time -  start_time
print(f"Tiempo marge, {time_result}s")
search(term,dictionary,vocabulary,'index.bin',count)
save_pickle(dictionary, "dictionary.pickle")
save_pickle(vocabulary, "vocabulary.pickle")
shutil.rmtree('index')
os.mkdir('index')

