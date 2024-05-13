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

def crear_skip_list(docs_term, n):
    skip_list = []
    frequency = []
    docs = []
    max_freq = 0
    bloque = 0
    docs_term = sort_docId(docs_term)
    for docId, freq in docs_term:
        frequency.append(freq)
        docs.append(docId)
        if max_freq < freq:
            max_freq = freq
        bloque +=1
        if bloque % n == 0:
            skip_list.append(((docId, max_freq),docs,frequency))
            frequency = []
            docs = []
            max_freq = 0
    return skip_list


vocabulary = read_pickle('vocabulary.pickle')
dictionary = read_pickle('dictionary.pickle')
docs_term = search('lluvia',dictionary,vocabulary,'index.bin')
print(crear_skip_list(docs_term,5))


