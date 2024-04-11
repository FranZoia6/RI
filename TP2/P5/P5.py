import pyterrier as pt
import sys
import numpy as np
from scipy.stats import spearmanr

if not pt.started():
    pt.init()

root_dir = sys.argv[1] #"wiki-small/"

indexer = pt.FilesIndexer("./index", verbose=True, overwrite=True, meta={"docno":20, "filename":512})
indexref =indexer.index(root_dir)
index = pt.IndexFactory.of(indexref)

queri = "software"

br =  pt.BatchRetrieve(index, num_results=50, wmodel="TF_IDF", metadata=["filename"])
results = br.search(queri)

tfidf = np.array(results["filename"])

br =  pt.BatchRetrieve(index, num_results=50, wmodel="BM25", metadata=["filename"])
results = br.search(queri)

bm25 = np.array(results["filename"])

print("Queri:", queri)

spearmancoefficient, datos = spearmanr(tfidf[:10], bm25[:10])
print("Coeficiente de correlación de Spearman:", spearmancoefficient,)
spearmancoefficient, datos = spearmanr(tfidf[:25], bm25[:25])
print("Coeficiente de correlación de Spearman:", spearmancoefficient,)
spearmancoefficient, datos = spearmanr(tfidf[:50], bm25[:50])
print("Coeficiente de correlación de Spearman:", spearmancoefficient,)

queri = "convention"

br =  pt.BatchRetrieve(index, num_results=50, wmodel="TF_IDF", metadata=["filename"])
results = br.search(queri)

tfidf = np.array(results["filename"])

br =  pt.BatchRetrieve(index, num_results=50, wmodel="BM25", metadata=["filename"])
results = br.search(queri)

bm25 = np.array(results["filename"])

print("Queri:", queri)

spearmancoefficient, datos = spearmanr(tfidf[:10], bm25[:10])
print("Coeficiente de correlación de Spearman:", spearmancoefficient,)
spearmancoefficient, datos = spearmanr(tfidf[:25], bm25[:25])
print("Coeficiente de correlación de Spearman:", spearmancoefficient,)
spearmancoefficient, datos = spearmanr(tfidf[:50], bm25[:50])
print("Coeficiente de correlación de Spearman:", spearmancoefficient,)

queri = "municipality"

br =  pt.BatchRetrieve(index, num_results=50, wmodel="TF_IDF", metadata=["filename"])
results = br.search(queri)

tfidf = np.array(results["filename"])

br =  pt.BatchRetrieve(index, num_results=50, wmodel="BM25", metadata=["filename"])
results = br.search(queri)

bm25 = np.array(results["filename"])

print("Queri:", queri)

spearmancoefficient, datos = spearmanr(tfidf[:10], bm25[:10])
print("Coeficiente de correlación de Spearman:", spearmancoefficient,)
spearmancoefficient, datos = spearmanr(tfidf[:25], bm25[:25])
print("Coeficiente de correlación de Spearman:", spearmancoefficient,)
spearmancoefficient, datos = spearmanr(tfidf[:50], bm25[:50])
print("Coeficiente de correlación de Spearman:", spearmancoefficient,)