import networkx as nx
import pandas as pd
import numpy as np
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


def split_book(book, n_sections=10, cumulative=True):
    '''
    Split a book into n equal parts, with optional cumulative aggregation

    Parameters
    ----------
    book : string (required)
        the book to be split
    n_sections :  (optional)
        the number of sections which we want to split our book into
    cumulative : bool (optional)
        If true, the returned sections will be cumulative, ie all
        will start at the book's beginning and end at evenly distributed
        points throughout the book

    Returns
    -------
    split_book : list
        the given book split into the specified number of even (or, if
        cumulative is set to True, uneven) sections
    '''
    book_sequences = get_sentence_sequences(book)
    split_book = np.array_split(np.array(book_sequences), n_sections)

    if cumulative is True:
        split_book = [np.concatenate(split_book[:pos + 1])
                      for pos, section in enumerate(split_book)]

    return split_book


def chronological_network(book_path, n_sections=10, cumulative=True):
    '''
    Split a book into n equal parts, with optional cumulative aggregation, and
    return a dictionary of assembled character graphs

    Parameters
    ----------
    book_path : string (required)
        path to the .txt file containing the book to be split
    n_sections :  (optional)
        the number of sections which we want to split our book into
    cumulative : bool (optional)
        If true, the returned sections will be cumulative, ie all will start at
        the book's beginning and end at evenly distributed points throughout
        the book

    Returns
    -------
    graph_dict : dict
        a dictionary containing the graphs of each split book section
        keys = section index
        values = nx.Graph describing the character graph in the specified book
                 section
    '''
    book = load_book(book_path)
    sections = split_book(book, n_sections, cumulative)
    graph_dict = {}

    for i, section in enumerate(sections):
        characters = extract_character_names(' '.join(section))
        df = find_connections(sequences=section, characters=characters)
        cooccurence = calculate_cooccurence(df)
        interaction_df = get_interaction_df(cooccurence, threshold=2)

        graph_dict[i] = nx.from_pandas_dataframe(interaction_df,
                                                 source='source',
                                                 target='target')
    return graph_dict


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
