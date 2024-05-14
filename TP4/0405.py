import pickle
import struct

def read_index(directory, df, pointer):
    seek = pointer * 8
    cant = df * 8
    with open(directory, 'rb') as binary_file:
        binary_file.seek(seek)
        byte_data = binary_file.read(cant)
    format_string = f">{len(byte_data) // 4}I"
    unpacked_data = struct.unpack(format_string, byte_data)
    grouped_data = [(unpacked_data[i], unpacked_data[i+1]) for i in range(0, len(unpacked_data), 2)]
    return grouped_data

def read_pickle(name):
    with open(name, 'rb') as f:
        structure = pickle.load(f)
    return structure

def search(term,dictionary,vocabulary,directory):
    if term in dictionary:
        termId = dictionary[term]
        df = vocabulary[termId]['df']
        pointer = vocabulary[termId]['pointer']
        result = read_index(directory, df, pointer)
        return result

def sort_docId(rank):
    sort = sorted(rank, key=lambda x: x[0])
    return sort

def crear_skip_lists(n):
    vocabulary = read_pickle('vocabulary.pickle')
    dictionary = read_pickle('dictionary.pickle')
    frequency = []
    docs = []
    max_freq = 0
    skip_lists = {}
    for term, termId in dictionary.items():
        bloque = 1
        skip_list = []
        docs_term = search(term,dictionary,vocabulary,'index.bin')
        docs_term = sort_docId(docs_term)
        for docId, freq in docs_term:
            frequency.append(freq)
            docs.append(docId)
            if max_freq < freq:
                max_freq = freq
            if bloque % n == 0:
                skip_list.append(((docId, max_freq),docs,frequency))
                frequency = []
                docs = []
                max_freq = 0
            bloque +=1
        if len(docs)>0:
            skip_list.append(((docId, max_freq),docs,frequency))
            frequency = []
            docs = []
            max_freq = 0   
        
        skip_lists[termId] = skip_list


        
    return skip_lists


def operator_and (docs,skip_list):
    result = []
    for doc in docs:
        for max,docsId,freq in skip_list:
            if doc>max[0]:
                continue 
            else: 
                for docId in docsId:
                    if docId == doc:
                        result.append(doc)
                    elif doc<docId:
                        continue


    return result





skip_lists = crear_skip_lists(6)
term1 = skip_lists[9]
docs = []
for _,docsId, _ in term1:
    docs.extend(docsId)
term2 = skip_lists[22]
print(term2)
print(operator_and(docs,term2))




