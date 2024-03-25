import os
import re
import sys
import nltk
from nltk.corpus import stopwords

def tokenizador(text,dtokens):
    tokens=text.split(" ")
    for token in tokens:
        if token in dtokens:
            dtokens[token]["cf"] += 1
        else:
            dtokens[token] = {"cf": 1}
    
    tokens = []
    abbreviations, text = extract_abbreviations(text)
    tokens.extend(abbreviations)
    mails, text = extract_mails(text)
    tokens.extend(mails) 
    numbers, text = extract_numbers(text)
    tokens.extend(numbers)
    urls, text = extract_urls(text)
    for url in urls:
        formatted_url = f"{url[0]}://{url[1]}{url[2]}"
        tokens.append(formatted_url)
    names,text = extract_proper_names(text)
    tokens.extend(names)

    normalized_text = text.lower()
    intab = "áéíóú"
    outtab = "aeiou"
    trantab = normalized_text.maketrans(intab, outtab)
    normalized_text = normalized_text.translate(trantab)
    normalized_text = re.sub(r'[^a-z0-9 ]', '', normalized_text)
    normalized_tokens = normalized_text.split(" ")
    tokens.extend(normalized_tokens)

    if "" in tokens:
        while "" in tokens:
            tokens.remove("")
    return tokens, dtokens

def contador(terms, tokens):
    for token in tokens:
        if token in terms:
            terms[token]["cf"] += 1
        elif len(token)>2 and len(token)<30:
            terms[token] = {"cf": 1}
    return terms


def extract_abbreviations(text):
    token = re.findall(r'\b[A-Z][a-z]+\.', text)
    text = re.sub(r'\b[A-Z][a-z]+\.','', text)
    return token, text

def extract_mails(text):
    tokens = re.findall(r'\b[A-Za-z0-9._]+@[A-Za-z0-9._]+\.[A-Za-z]{2,}\b', text)
    text = re.sub(r'\b[A-Za-z0-9._-]+@[A-Za-z0-9._-]+\.[A-Za-z]{2,}\b', '', text)
    return tokens, text

def extract_numbers(text):
    tokens = re.findall(r'\b\d+\b', text)
    text = re.sub(r'\b\d+\b','', text)
    return tokens, text

def extract_urls(text):
    urls = re.findall(r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', text)
    text = re.sub(r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?','', text)
    return urls, text


def extract_proper_names(text):
    names = re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', text)
    text = re.sub(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b','', text)
    return names, text

def remove_sportsworld(terms):
    dic = {}
    stopsSp = set(stopwords.words('spanish'))
    stopsEn = set(stopwords.words('english'))
    for term in terms:
        if term not in stopsSp and term not in stopsEn:
            dic[term] = terms[term]
    return dic


file_location = sys.argv[1]
cant_files = len(os.listdir(file_location))
cant_terms = 0
cant_min_tokens = 0
cant_max_tokens = 0
cant_min_terms = 0
cant_max_terms = 0
terms_length = 0
unique_terms = 0
terms = {}
dtokens = {}

for path in os.listdir(file_location):
    path = file_location + path
    termsAux = {}
    cant_tokens_doc = 0
    with open(path) as file:
        for linea in file:
            tokens,dtokens=tokenizador(linea,dtokens)
            termsAux = contador(termsAux,tokens)
            cant_tokens_doc += len(tokens)
        if cant_tokens_doc> cant_max_tokens:
            cant_max_tokens = cant_tokens_doc
            cant_max_terms = len(termsAux)
        if cant_min_tokens>cant_tokens_doc or cant_min_tokens == 0:
            cant_min_tokens = cant_tokens_doc
            cant_min_terms = len(termsAux)
    for termAux in termsAux:
        if termAux in terms:
            terms[termAux]["cf"] += termsAux[termAux]["cf"]
            terms[termAux]["df"] += 1
        else:
            terms[termAux] = {"cf": termsAux[termAux]["cf"],"df": 1}

if len(sys.argv)>2:
    terms = remove_sportsworld(terms)

sorted_terms = sorted(terms.items(), key=lambda item: item[1].get("cf", 0), reverse=True)

cant_terms =  len(terms)

with open("terminos.txt", "w") as f:
    for term, info in sorted_terms:
        f.write(f"{term} {info['cf']} {info['df']}\n")
        if info['cf'] == 1:
            unique_terms += 1
        terms_length += len(term)

cant_tokens = sum([dtokens[term]["cf"] for term in dtokens])

with open("estadisticas.txt", "w") as f:
    f.write(f"{cant_files} \n")
    f.write(f"{cant_tokens} \n")
    f.write(f"{cant_terms} \n")
    f.write(f"{cant_tokens/cant_files} {cant_terms/cant_files}\n")
    f.write(f"{terms_length/cant_terms}\n")
    f.write(f"{cant_max_tokens} {cant_min_tokens}\n")
    f.write(f"{cant_max_terms} {cant_min_tokens}\n")
    f.write(f"{unique_terms}\n")

higher_frequency = sorted_terms[:10]
lower_frequency = sorted_terms[-10:] 
with open("frecuencias.txt", "w") as f:
    for term, info in higher_frequency:
        f.write(f"{term} {info['cf']} \n")
    for term, info in lower_frequency:
        f.write(f"{term} {info['cf']} \n")
 
