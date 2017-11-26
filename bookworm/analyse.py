import networkx as nx
import pandas as pd
import networkx as nx
from nltk.tokenize import word_tokenize
from .build_network import *


def character_density(book_path):
    '''
    number of central characters divided by the total number of words in a novel

    Parameters
    ----------
    book_path : string (required)
        path to txt file containing full text of book to be analysed

    Returns
    -------
    density : float
        number of characters in book / number of words in book
    '''
    book = load_book(book_path)
    book_length = len(word_tokenize(book))
    book_graph = nx.from_pandas_dataframe(bookworm(book_path),
                                          source='source',
                                          target='target')
    n_characters = len(book_graph.nodes())
    return n_characters / book_length


def select_k(spectrum):
    '''
    Returns k, where the top k eigenvalues of the graph's laplacian describe 90
    percent of the graph's complexiities.

    Parameters
    ----------
    spectrum : type (required optional)
        the laplacian spectrum of the graph in question

    Returns
    -------
    k : int
        denotes the top k eigenvalues of the graph's laplacian spectrum,
        explaining 90 percent of its complexity (or containing 90 percent of
        its energy)
    '''
    if sum(spectrum) == 0:
        return len(spectrum)

    running_total = 0
    for i in range(len(spectrum)):
        running_total += spectrum[i]
        if (running_total / sum(spectrum)) >= 0.9:
            return i + 1

    return len(spectrum)


def graph_similarity(graph_1, graph_2):
    '''
    Computes the similarity of two graphs based on their laplacian spectra,
    returning a value between 0 and inf where a score closer to 0 is indicative
    of a more similar network

    Parameters
    ----------
    graph_1 : networkx.Graph (required)
    graph_2 : networkx.Graph (required)

    Returns
    -------
    similarity : float
        the similarity score of the two graphs where a value closer to 0 is
        indicative of a more similar pair of networks
    '''
    laplacian_1 = nx.spectrum.laplacian_spectrum(graph_1)
    laplacian_2 = nx.spectrum.laplacian_spectrum(graph_2)

    k_1 = select_k(laplacian_1)
    k_2 = select_k(laplacian_2)
    k = min(k_1, k_2)

    return sum((laplacian_1[:k] - laplacian_2[:k])**2)


def comparison_df(graph_dict):
    '''
    takes an assortment of novels and computes their simlarity, based on their
    laplacian spectra

    Parameters
    ----------
    graph_dict : dict (required)
        keys   = book title
        values = character graph

    Returns
    -------
    comparison : pandas.DataFrame
        columns = book titles
        indexes = book titles
        values  = measure of the character graph similarity of books
    '''
    books = list(graph_dict.keys())
    comparison = {book_1: {book_2: graph_similarity(graph_dict[book_1],
                                                    graph_dict[book_2])
                           for book_2 in books} for book_1 in books}

    return pd.DataFrame(comparison)
