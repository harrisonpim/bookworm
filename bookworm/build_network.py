import nltk
import spacy
import requests
import numpy as np
import pandas as pd
import networkx as nx
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer

nlp = spacy.load('en')

def remove_punctuation(input_string):
    return input_string.translate(str.maketrans('', '', punctuation))


def window_over_sentences(sentences, size=2):
    return [' '.join(sentences[i : i + size]) 
            for i in range(len(sentences) - size - 1)]


def sequences_to_count_matrix(sequences, count_vectorizer):
    '''count instances of each word in the vocabulary in each sentence'''
    return count_vectorizer.fit_transform(sequences).todense()


def is_plausible_entity(word):
    return ((word.pos_ == 'PROPN') & 
            (word.text.istitle()) & 
            (len(word) > 2))


def get_plausible_entities(count_vectorizer):
    vocabulary = remove_punctuation(' '.join(count_vectorizer.vocabulary_.keys()))
    plausible_entities = [word.text for word in nlp(vocabulary)
                          if is_plausible_entity(word)]
    return plausible_entities


def get_adjacency_matrix(count_matrix, count_vectorizer, plausible_entities):
    '''
    count instances of each plausible entity in each sequence. 
    return character/character counts
    '''
    relevant_indicies = [count_vectorizer.vocabulary_[e]
                         for e in plausible_entities]
    interaction_matrix = count_matrix[:, relevant_indicies]
    adjacency = interaction_matrix.T.dot(interaction_matrix)
    np.fill_diagonal(adjacency, 0)
    return pd.DataFrame(data=adjacency, 
                        columns=plausible_entities, 
                        index=plausible_entities)


def get_edgelist(adjacency, threshold):
    rows, columns = np.where(np.triu(adjacency.values, 1) > threshold)
    edges = np.column_stack([adjacency.index[rows],
                             adjacency.columns[columns],
                             adjacency.values[rows, columns]])
    return pd.DataFrame(data=edges,
                        columns=['source', 'target', 'value'])


def bookworm(book, threshold=15):
    sentences = nltk.sent_tokenize(book)
    sequences = window_over_sentences(sentences)
    count_vectorizer = CountVectorizer(lowercase=False)
    count_matrix = sequences_to_count_matrix(sequences, count_vectorizer)
    plausible_entities = get_plausible_entities(count_vectorizer)

    adjacency = get_adjacency_matrix(count_matrix, 
                                     count_vectorizer, 
                                     plausible_entities)

    edgelist = get_edgelist(adjacency, threshold)
    return nx.from_pandas_edgelist(edgelist, 
                                   source='source', 
                                   target='target', 
                                   edge_attr='value')
