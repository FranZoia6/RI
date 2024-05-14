import pickle
import struct



def read_index(directory, df, pointer, count):
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
    grouped_data = [(unpacked_data[i], unpacked_data[i+1]) for i in range(0, len(unpacked_data), 2)]
    return grouped_data
    

def search(term,dictionary,vocabulary,directory, count):
    if term in dictionary:
        termId = dictionary[term]
        df = vocabulary[termId]['df']
        pointer = vocabulary[termId]['pointer']
        result = read_index(directory, df, pointer,count)
        return result

def read_pickle(name):
    with open(name, 'rb') as f:
        structure = pickle.load(f)
    return structure

def operator_and(doc_term1,doc_term2):
    result = []
    for docId_term1,freq_term1 in doc_term1:
        for docId_term2,freq_term2 in doc_term2:
            if docId_term1 == docId_term2:
                frequency = freq_term1 + freq_term2
                result.append((docId_term1,frequency))

    return result

def operator_not(doc_term1,doc_term2):
    result = []
    for docId_term1,freq_term1 in doc_term1:
        for docId_term2,freq_term2 in doc_term2:
            if docId_term1 == docId_term2:
                doc_term1.remove((docId_term1,freq_term1))

    return doc_term1

def operator_or (doc_term1,doc_term2):
    dic_result = {}
    result = []
    for docId, frequency in doc_term1:
        dic_result[docId] = dic_result.get(docId, 0) + frequency
    for docId, frequency in doc_term2:
        dic_result[docId] = dic_result.get(docId, 0) + frequency
    for docId, frequency in dic_result.items():
        result.append((docId,frequency))
    return result


def operadores(operador, doc_term1,doc_term2):
    if operador == "OR":
        result = operator_or(doc_term1,doc_term2)
    elif operador == "AND":
        result = operator_and(doc_term1,doc_term2)
    else:
        result = operator_not(doc_term1,doc_term2)
    return result


pila = []
vocabulary = read_pickle('vocabulary.pickle')
dictionary = read_pickle('dictionary.pickle')
query = 'casa AND lluvia'
query = query.split()
pila = query
pila2 = []
i = 0
array_docs = []

while len(pila) != 0:
    term = pila.pop()
    queryAux = []
    if term not in {'OR', 'AND', 'NOT'}:
        if ')' in term:
            subquery = []
            while term != '(':
                subquery.append(term)
                if len(pila) == 0:
                    break 
                term = pila.pop()
            queryAux.extend(subquery[::-1]) 
        else:
            queryAux.append(term)
        if len(queryAux)>1:
            term1 = queryAux[0].replace('(', '').replace(')', '')  
            operador = queryAux[1]
            term2 = queryAux[2].replace('(', '').replace(')', '')
            doc_term1 =  search(term1,dictionary,vocabulary,'index.bin', True)
            doc_term2 =  search(term2,dictionary,vocabulary,'index.bin', True)
            result = operadores(operador,doc_term1,doc_term2)
            array_docs.append(result)
        else:
            array_docs.append(search(term,dictionary,vocabulary,'index.bin', True))
    else:
        array_docs.append(term)
if len(array_docs) ==3:
    result = operadores(array_docs[1],array_docs[0],array_docs[2])
elif len(array_docs) ==5: 
    result_partial = operadores(array_docs[1],array_docs[0],array_docs[2])
    result = operadores(array_docs[3],result_partial,array_docs[4])

print(result)
