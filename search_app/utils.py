import os
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, ISRIStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_document(document, language='english'):
    if document is None:
        return ''

    words = word_tokenize(document.lower())

    if language == 'arabic':
        stemmer = ISRIStemmer()
    else:
        stemmer = PorterStemmer()

    stop_words = set(stopwords.words(language))
    words = [word for word in words if word.isalnum() and word not in stop_words and len(word) > 2]
    words = [stemmer.stem(word) for word in words]
    return ' '.join(words)
def build_boolean_index(documents):
    inverted_index = {}
    for doc_id, document in enumerate(documents):
        processed_doc = preprocess_document(document)
        for term in processed_doc.split():
            if term not in inverted_index:
                inverted_index[term] = set()
            inverted_index[term].add(doc_id)
    return inverted_index

def boolean_search(query, inverted_index, documents):
    query_terms = set(preprocess_document(query).split())
    result_docs = set(range(len(documents)))

    for term in query_terms:
        if term in inverted_index:
            result_docs.intersection_update(inverted_index[term])
        else:
            result_docs.clear()

    return [documents[doc_id] for doc_id in result_docs]

def extended_boolean_search(query, inverted_index, documents):
    query_terms = [preprocess_document(term) for term in query.split()]
    result_docs = set(range(len(documents)))

    for term in query_terms:
        term_result = set()
        for subterm in term.split():
            if subterm in inverted_index:
                term_result.update(inverted_index[subterm])
        result_docs.intersection_update(term_result)

    return [documents[doc_id] for doc_id in result_docs]

def vector_space_model_search(query, documents):
    filtered_documents = [doc for doc in documents if doc is not None]

    if not filtered_documents:
        raise ValueError("All documents are too short. Adjust your preprocessing steps.")

    vectorizer = TfidfVectorizer(min_df=1)
    vectors = vectorizer.fit_transform(filtered_documents)

    if vectors.shape[1] == 0:
        raise ValueError("No features left after pre-processing. Adjust your preprocessing steps.")

    query_vector = vectorizer.transform([preprocess_document(query)])
    similarities = cosine_similarity(query_vector, vectors).flatten()

    ranked_docs = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)

    return [filtered_documents[doc_id] for doc_id, _ in ranked_docs]

def read_doc(file_path, language='english'):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            text = extract_text_from_doc(data, language)
        return text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def extract_text_from_doc(doc_data, language='english'):
    try:
        text = doc_data.decode('utf-8', errors='ignore')
        return preprocess_document(text, language)
    except Exception as e:
        print(f"Error extracting text from document: {e}")
        return None