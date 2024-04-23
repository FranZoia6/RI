import pyterrier as pt
import matplotlib.pyplot as plt
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
    
    documentos = contenido.split(".I ")[1:]
    
    with open('archivo_salida.trec', 'w', encoding='utf-8') as file:
        for i, documento in enumerate(documentos, start=1):
            documentoTrec = "<DOC>\n<DOCNO>" + str(i) + "</DOCNO>\n" + documento.strip() + "\n</DOC>\n\n"
            file.write(documentoTrec)


def tokenize_line(line, query_id):
    tokens = []
    for token in line.split():
        word = re.sub(regex_alpha_words, '', token.lower())
        if word and word not in stopwords:
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


def get_tag(line):
    match = re.match(r'\.([ITAWXB])', line)
    return match.group(1) if match else None

def get_query_id(line):
    match = re.search(r'\.I\s+(\d+)', line)
    return match.group(1) if match else None

def query_trec(path):
    filein = path + "/CISI.QRY"
    with open(filein, 'r', encoding='utf-8') as fin, open("queries_CISI.trec", "w", encoding='utf-8') as fout:
        queryId = None
        in_query = False
        for line in fin:
            tag = get_tag(line)
            if tag == "I":
                if queryId:
                    fout.write("</TITLE>\n</TOP>\n")
                queryId = get_query_id(line)
                fout.write(f"<TOP>\n<NUM>{queryId}</NUM>\n<TITLE> ")
                in_query = True
                unique_terms[queryId] = set()  
            elif tag == "B":
                if in_query:
                    fout.write(" </TITLE>\n</TOP>\n")
                    in_query = False
            elif in_query and not line.startswith(('.W', '.T')):
                tokens = tokenize_line(line, queryId)
                if tokens:
                    fout.write(" ".join(tokens))

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
                if queryId:
                    fout.write("</TITLE>\n</TOP>\n")
                queryId = get_query_id(line)
                fout.write(f"<TOP>\n<NUM>{queryId}</NUM>\n<TITLE> ")
                in_query = True
                unique_terms[queryId] = set()  
            elif tag == "B":
                if in_query:
                    fout.write(" </TITLE>\n</TOP>\n")
                    in_query = False
            elif in_query and not line.startswith(('.W', '.T')):
                tokens = tokenize_line_frec(line,queryId)
                if tokens:
                    fout.write(" ".join(tokens))
        
        if queryId and in_query:
            fout.write(" </TITLE>\n</TOP>\n")





path = sys.argv[1]
procesar_archivo_all(path)
nltk.download('stopwords')
regex_alpha_words = re.compile(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚüÜñÑ]')
stopwords = set(nltk_stopwords.words('spanish'))
unique_terms = {}

qrles_trec(path)
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
hlm = pt.BatchRetrieve(index, num_results=10, wmodel="Hiemstra_LM")

queries_sin_frec = pt.io.read_topics("queries_CISI.trec")
queries_con_frec = pt.io.read_topics("queriesfrec_CISI.trec")

qrels = pt.io.read_qrels("qrels_CISI")

eval_metrics = [
    "num_q", "num_ret", "num_rel", "num_rel_ret", "map", 
    "Rprec", "bpref", "recip_rank", "iprec_at_recall_0.00", 
    "iprec_at_recall_0.10", "iprec_at_recall_0.20", "iprec_at_recall_0.30", 
    "iprec_at_recall_0.40", "iprec_at_recall_0.50", "iprec_at_recall_0.60", 
    "iprec_at_recall_0.70", "iprec_at_recall_0.80", "iprec_at_recall_0.90", 
    "iprec_at_recall_1.00", "P_5", "P_10", "P_15", "P_20", "P_30", 
    "P_100", "P_200", "P_500", "P_1000"
]

# Ejecutar el experimento solo para el sistema TF-IDF
resultados_tfidf = pt.Experiment(
    [tf_idf],
    queries_con_frec,
    qrels,
    eval_metrics=eval_metrics,
    names=["TF_IDF"]
)

resultados_bm25 = pt.Experiment(
    [bm25],
    queries_con_frec,
    qrels,
    eval_metrics=eval_metrics,
    names=["BM25"]
)

resultados_hlm = pt.Experiment(
    [hlm],
    queries_con_frec,
    qrels,
    eval_metrics=eval_metrics,
    names=["Hiemstra_LM"]
)

df_11puntos_tfidf = resultados_tfidf.melt(value_vars=["iprec_at_recall_0.10", "iprec_at_recall_0.20", "iprec_at_recall_0.30", 
                                    "iprec_at_recall_0.40", "iprec_at_recall_0.50", "iprec_at_recall_0.60", 
                                    "iprec_at_recall_0.70", "iprec_at_recall_0.80", "iprec_at_recall_0.90", 
                                    "iprec_at_recall_1.00"], var_name="Recall", value_name="Precision")

df_11puntos_tfidf['Recall'] = df_11puntos_tfidf['Recall'].apply(lambda x: float(x.split('_')[-1]))

df_11puntos_bm25 = resultados_bm25.melt(value_vars=["iprec_at_recall_0.10", "iprec_at_recall_0.20", "iprec_at_recall_0.30", 
                                    "iprec_at_recall_0.40", "iprec_at_recall_0.50", "iprec_at_recall_0.60", 
                                    "iprec_at_recall_0.70", "iprec_at_recall_0.80", "iprec_at_recall_0.90", 
                                    "iprec_at_recall_1.00"], var_name="Recall", value_name="Precision")

df_11puntos_bm25['Recall'] = df_11puntos_bm25['Recall'].apply(lambda x: float(x.split('_')[-1]))

df_11puntos_hlm = resultados_hlm.melt(value_vars=["iprec_at_recall_0.10", "iprec_at_recall_0.20", "iprec_at_recall_0.30", 
                                    "iprec_at_recall_0.40", "iprec_at_recall_0.50", "iprec_at_recall_0.60", 
                                    "iprec_at_recall_0.70", "iprec_at_recall_0.80", "iprec_at_recall_0.90", 
                                    "iprec_at_recall_1.00"], var_name="Recall", value_name="Precision")

df_11puntos_hlm['Recall'] = df_11puntos_hlm['Recall'].apply(lambda x: float(x.split('_')[-1]))


plt.figure(figsize=(10, 6))  
plt.plot(df_11puntos_tfidf['Recall'], df_11puntos_tfidf['Precision'], marker='o', linestyle='-', label='TFIDF')  
plt.plot(df_11puntos_tfidf['Recall'], df_11puntos_hlm['Precision'], marker='x', linestyle='-', label='HLM')  
plt.plot(df_11puntos_bm25['Recall'], df_11puntos_bm25['Precision'], marker='x', linestyle='-', label='BM25') 
plt.xlabel('Recall')  
plt.ylabel('Precision') 
plt.title('Con Frecuencias') 
plt.grid(True)  
plt.legend()  
plt.show()  

resultados_tfidf_sin_frecs = pt.Experiment(
    [tf_idf],
    queries_sin_frec,
    qrels,
    eval_metrics=eval_metrics,
    names=["TF_IDF"]
)

resultados_hlm_sin_frecs = pt.Experiment(
    [hlm],
    queries_sin_frec,
    qrels,
    eval_metrics=eval_metrics,
    names=["Hiemstra_LM"]
)

resultados_bm25_sin_frecs = pt.Experiment(
    [bm25],
    queries_sin_frec,
    qrels,
    eval_metrics=eval_metrics,
    names=["BM25"]
)

df_11puntos_sin_frec_tfidf = resultados_tfidf_sin_frecs.melt(value_vars=["iprec_at_recall_0.10", "iprec_at_recall_0.20", "iprec_at_recall_0.30", 
                                    "iprec_at_recall_0.40", "iprec_at_recall_0.50", "iprec_at_recall_0.60", 
                                    "iprec_at_recall_0.70", "iprec_at_recall_0.80", "iprec_at_recall_0.90", 
                                    "iprec_at_recall_1.00"], var_name="Recall", value_name="Precision")

df_11puntos_sin_frec_tfidf['Recall'] = df_11puntos_sin_frec_tfidf['Recall'].apply(lambda x: float(x.split('_')[-1]))

df_11puntos_sin_frec_bm25 = resultados_bm25_sin_frecs.melt(value_vars=["iprec_at_recall_0.10", "iprec_at_recall_0.20", "iprec_at_recall_0.30", 
                                    "iprec_at_recall_0.40", "iprec_at_recall_0.50", "iprec_at_recall_0.60", 
                                    "iprec_at_recall_0.70", "iprec_at_recall_0.80", "iprec_at_recall_0.90", 
                                    "iprec_at_recall_1.00"], var_name="Recall", value_name="Precision")

df_11puntos_sin_frec_bm25['Recall'] = df_11puntos_sin_frec_bm25['Recall'].apply(lambda x: float(x.split('_')[-1]))


df_11puntos_sin_frec_hlm = resultados_hlm_sin_frecs.melt(value_vars=["iprec_at_recall_0.10", "iprec_at_recall_0.20", "iprec_at_recall_0.30", 
                                    "iprec_at_recall_0.40", "iprec_at_recall_0.50", "iprec_at_recall_0.60", 
                                    "iprec_at_recall_0.70", "iprec_at_recall_0.80", "iprec_at_recall_0.90", 
                                    "iprec_at_recall_1.00"], var_name="Recall", value_name="Precision")

df_11puntos_sin_frec_hlm['Recall'] = df_11puntos_sin_frec_hlm['Recall'].apply(lambda x: float(x.split('_')[-1]))


plt.figure(figsize=(10, 6))  
plt.plot(df_11puntos_sin_frec_tfidf['Recall'], df_11puntos_sin_frec_tfidf['Precision'], marker='o', linestyle='-', label='TFIDF')  
plt.plot(df_11puntos_sin_frec_hlm['Recall'], df_11puntos_sin_frec_hlm['Precision'], marker='x', linestyle='-', label='HLM')  
plt.plot(df_11puntos_sin_frec_bm25['Recall'], df_11puntos_sin_frec_bm25['Precision'], marker='x', linestyle='-', label='BM25') 
plt.title('Sin Frecuencias')  
plt.xlabel('Recall') 
plt.ylabel('Precision') 
plt.grid(True) 
plt.legend() 
plt.show()  