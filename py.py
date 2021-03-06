import re
import os

class index_element:
    def __init__(self, word: str, docid_list: list):
        self.__word = word
        self.__docid_list = docid_list
    def print(self):
        print(self.__word)
        print(self.__docid_list)
    @property
    def get_word(self):
        return self.__word
    @property
    def get_docid_list(self):
        return self.__docid_list
    def set_word(self, word: str):
        self.__word = word
    def set_docid_list(self, docid_list: list):
        self.__docid_list = docid_list

def preprocess_text(doc):
    processed_doc = doc.lower()
    processed_doc = processed_doc.replace("’", "'")
    processed_doc = processed_doc.replace("“", '"')
    processed_doc = processed_doc.replace("”", '"')
    non_words = re.compile(r"[^A-Za-z0-9']+")
    processed_doc = re.sub(non_words, ' ', processed_doc)
    return processed_doc

def read_file(file_path):
    f = open(file_path, encoding = 'utf-8', mode = "r")
    text = f.read()
    return text

def build_inverted_index(library_path):
    inverted_index = []

    # Get distinct words from docs and make a temporary doc list
    word_collection = '' # Distinct words
    docs = [] # Doc list
    for filename in os.listdir(library_path):
        file_path = os.path.join(library_path, filename)
        text = read_file(file_path)
        text = preprocess_text(text)
        docs.append(text)
        word_collection = word_collection + ' ' + text
    word_collection = word_collection.split()
    word_collection = list(set(word_collection))

    # Build an inverted index
    for i in range(len(word_collection)):
        docid_list = []
        for j in range(len(docs)):
            if docs[j].find(word_collection[i]) != -1:
                docid_list.append(j)
        inverted_index.append(index_element(word_collection[i], docid_list))
    return inverted_index

def search_docs(search_term: str, inverted_index: list):
    search_term = preprocess_text(search_term)
    search_term = search_term.split()
    search_items = []
    for i in range(len(search_term)):
        for j in range(len(inverted_index)):
            if search_term[i] == inverted_index[j].get_word:
                search_items.append(inverted_index[j].get_docid_list)
                break
    
    if len(search_items) == 0:
        return []
    else:
        return list(set(search_items[0]).intersection(*search_items))

b = input()
a = input()

print(search_docs(a, build_inverted_index(b)))