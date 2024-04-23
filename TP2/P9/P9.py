import pyterrier as pt
import matplotlib.pyplot as plt
from os import listdir
from os.path import join, isdir
import sys

import re
import nltk
from nltk.corpus import stopwords as nltk_stopwords

def qrles_trec(path):
    
    filein = path+"/CISI.REL"
    fileout= open("qrels_CISI", "x",encoding='utf-8')
    with open(filein,'r',encoding='utf-8') as f:  
        for line in f.readlines():
            query_id, document_id, _,_ = line.split()
            fileout.write("{} {} {} {}\n".format(query_id, 0, document_id, 1))
    fileout.close()

def procesar_archivo_all(path):
    path = path + '/CISI.ALL'
    with open(path, 'r', encoding='utf-8') as file:
        contenido = file.read()
    
    # Dividir el contenido en documentos
    documentos = contenido.split(".I ")[1:]
    
    # Escribir cada documento en el archivo de salida en formato TREC
    with open('archivo_salida.trec', 'w', encoding='utf-8') as file:
        for i, documento in enumerate(documentos, start=1):
            # Agregar etiquetas TREC
            documentoTrec = "<DOC>\n<DOCNO>" + str(i) + "</DOCNO>\n" + documento.strip() + "\n</DOC>\n\n"
            file.write(documentoTrec)


# Tokeniza una línea y opcionalmente cuenta las frecuencias de las palabras
def tokenize_line(line, query_id):
    tokens = []
    for token in line.split():
        word = re.sub(regex_alpha_words, '', token.lower())
        if word and word not in stopwords:
            # Si no estamos contando frecuencias, verificamos si el término ya se ha agregado a esta consulta
            if word not in unique_terms.get(query_id, set()):
                unique_terms.setdefault(query_id, set()).add(word)
                tokens.append(word)
    return tokens

def tokenize_line_frec(line, query_id):
    tokens = []
    for token in line.split():
        word = re.sub(regex_alpha_words, '', token.lower())
        if word and word not in stopwords:
            tokens.append(word)
    return tokens

# Obtiene el tipo de tag de una línea
def get_tag(line):
    match = re.match(r'\.([ITAWXB])', line)
    return match.group(1) if match else None

# Obtiene el ID de consulta de una línea
def get_query_id(line):
    match = re.search(r'\.I\s+(\d+)', line)
    return match.group(1) if match else None

# Función principal
def query_trec(path):
    filein = path + "/CISI.QRY"
    with open(filein, 'r', encoding='utf-8') as fin, open("queries_CISI.trec", "w", encoding='utf-8') as fout:
        queryId = None
        in_query = False
        for line in fin:
            tag = get_tag(line)
            if tag == "I":
                # Escribir el inicio de la consulta y marcar que estamos dentro de una consulta
                if queryId:
                    fout.write("</TITLE>\n</TOP>\n")
                queryId = get_query_id(line)
                fout.write(f"<TOP>\n<NUM>{queryId}</NUM>\n<TITLE> ")
                in_query = True
                unique_terms[queryId] = set()  # Limpiar los términos únicos para esta consulta
            elif tag == "B":
                # Escribir el fin de la consulta y marcar que no estamos dentro de una consulta
                if in_query:
                    fout.write(" </TITLE>\n</TOP>\n")
                    in_query = False
            elif in_query and not line.startswith(('.W', '.T')):
                # Escribir el contenido de la consulta, ignorando líneas que comienzan con .W o .T
                tokens = tokenize_line(line, queryId)
                if tokens:
                    fout.write(" ".join(tokens))
        
        # Verificar si quedó una consulta sin terminar
        if queryId and in_query:
            fout.write(" </TITLE>\n</TOP>\n")

def query_trec_frec(path):
    filein = path + "/CISI.QRY"
    with open(filein, 'r', encoding='utf-8') as fin, open("queriesfrec_CISI.trec", "w", encoding='utf-8') as fout:
        queryId = None
        in_query = False
        for line in fin:
            tag = get_tag(line)
            if tag == "I":
                # Escribir el inicio de la consulta y marcar que estamos dentro de una consulta
                if queryId:
                    fout.write("</TITLE>\n</TOP>\n")
                queryId = get_query_id(line)
                fout.write(f"<TOP>\n<NUM>{queryId}</NUM>\n<TITLE> ")
                in_query = True
                unique_terms[queryId] = set()  # Limpiar los términos únicos para esta consulta
            elif tag == "B":
                # Escribir el fin de la consulta y marcar que no estamos dentro de una consulta
                if in_query:
                    fout.write(" </TITLE>\n</TOP>\n")
                    in_query = False
            elif in_query and not line.startswith(('.W', '.T')):
                # Escribir el contenido de la consulta, ignorando líneas que comienzan con .W o .T
                tokens = tokenize_line_frec(line,queryId)
                if tokens:
                    fout.write(" ".join(tokens))
        
        # Verificar si quedó una consulta sin terminar
        if queryId and in_query:
            fout.write(" </TITLE>\n</TOP>\n")





path = 'cisi' #sys.argv[1]
qrles_trec(path)
procesar_archivo_all(path)

# Descargar las stopwords de NLTK si no están disponibles
nltk.download('stopwords')

# Expresión regular para eliminar caracteres no alfanuméricos
regex_alpha_words = re.compile(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚüÜñÑ]')

# Lista de stopwords de NLTK
stopwords = set(nltk_stopwords.words('spanish'))

# Diccionario para almacenar los términos únicos en cada consulta
unique_terms = {}

query_trec(path)
query_trec_frec(path)

if not pt.started():
    pt.init()



files = "archivo_salida.trec"

indexer = pt.TRECCollectionIndexer("./index", verbose=True, overwrite=True, meta={"docno":20, "filename":512})
indexref = indexer.index(files)

index = pt.IndexFactory.of(indexref)

tf_idf = pt.BatchRetrieve(index, num_results=10, wmodel="TF_IDF")
bm25 = pt.BatchRetrieve(index, num_results=10, wmodel="BM25")

queries_sin_frec = pt.io.read_topics("queries_CISI.trec")
queries_con_frec = pt.io.read_topics("queriesfrec_CISI.trec")
qrels = pt.io.read_qrels("qrels_CISI")

