import pickle
import re
import struct

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

def sort_rank(rank):
    sort = sorted(rank, key=lambda x: x[1],reverse=True)
    return sort

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
    

def search(term,dictionary,vocabulary,directory):
    if term in dictionary:
        termId = dictionary[term]
        df = vocabulary[termId]['df']
        pointer = vocabulary[termId]['pointer']
        result = read_index(directory, df, pointer)
        return result
    
def read_pickle(name):
    with open(name, 'rb') as f:
        structure = pickle.load(f)
    return structure

def search_daat(references,terms,rank, k):
    vocabulary = read_pickle('vocabulary.pickle')
    dictionary = read_pickle('dictionary.pickle')
    for doc in references:
        score_doc = 0
        for term in terms:
            docs_term = search(term,dictionary,vocabulary,'index.bin')
            for docID, freq in docs_term:
                if doc == docID:
                    score_doc += freq
        if len(rank)>=k:
            min_score =  rank[k-1][1]
            if score_doc > min_score:
                rank.pop()
                rank.append((doc,score_doc))
        else:   
            rank.append((doc,score_doc))
        rank = sort_rank(rank)
    return rank



def read_pickle(name):
    with open(name, 'rb') as f:
        structure = pickle.load(f)
    return structure

query = 'casa lluvia'
query = tokenizador(query)
references = read_pickle('reference.pickle')
print(query)
print(search_daat(references,query,[], 5))
