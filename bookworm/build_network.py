import csv
import nltk
import pandas as pd
import numpy as np
import spacy
from nltk.tokenize import word_tokenize
import string


def load_book(book_path, lower=False):
    '''
    Reads in a novel from a .txt file, and returns it in (optionally
    lowercased) string form

    Parameters
    ----------
    book_path : string (required)
        path to txt file containing full text of book to be analysed
    lower : bool (optional)
        If True, the returned string will be lowercased;
        If False, the returned string will retain its original case formatting.

    Returns
    -------
    book : string
        book in string form
    '''
    with open(book_path) as f:
        book = f.read()
    if lower:
        book = book.lower()
    return book


def load_characters(charaters_path):
    '''
    Reads in a .csv file of character names

    Parameters
    ----------
    charaters_path : string (required)
        path to csv file containing full list of characters to be examined.
        Each character should take up one line of the file. If the character is
        referred to by multiple names, nicknames or sub-names within their
        full name, these should be split by commas, eg:
        Harry, Potter
        Lord, Voldemort, You-Know-Who
        Giant Squid

    Returns
    -------
    characters : list
        list of tuples naming characters in text
    '''
    with open(charaters_path) as f:
        reader = csv.reader(f)
        characters = [tuple(name.lower()+' ' for name in row) for row in reader]
    return characters


def remove_punctuation(input_string):
    '''
    Removes all punctuation from an input string

    Parameters
    ----------
    input_string : string (required)
        input string

    Returns
    -------
    clean_string : string
        clean string
    '''
    return input_string.translate(str.maketrans('', '', string.punctuation+'’'))


def extract_character_names(book):
    '''
    Automatically extracts lists of plausible character names from a book

    Parameters
    ----------
    book : string (required)
        book in string form (with original upper/lowercasing intact)

    Returns
    -------
    characters : list
        list of plasible character names
    '''
    nlp = spacy.load('en')
    stopwords = nltk.corpus.stopwords.words('english')

    words = [remove_punctuation(w) for w in book.split()]
    unique_words = list(set(words))

    characters = [word.text for word in nlp(' '.join(unique_words)) if word.pos_ == 'PROPN']
    characters = [c for c in characters if len(c) > 2]
    characters = [c for c in characters if c.istitle()]
    characters = [c for c in characters if not (c[-1] == 's' and c[:-1] in characters)]
    characters = list(set([c.title() for c in [c.lower() for c in characters]]) - set(stopwords))

    return [tuple([c + ' ']) for c in set(characters)]


def get_sentence_sequences(book):
    '''
    Splits a book into its constituent sentences

    Parameters
    ----------
    book : string (required)
        book in string form

    Returns
    -------
    sentences : list
        list of strings, where each string is a sentence in the novel as
        interpreted by NLTK's tokenize() function.
    '''
    detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = detector.tokenize(book)
    return sentences


def get_word_sequences(book, n=50):
    '''
    Takes a book and splits it into its constituent words, returning a list of
    substrings which comprise the book, whose lengths are determined by a set
    number of words (default = 50).

    Parameters
    ----------
    book : string (required)
        book in string form
    n : int (optional)
        number of words to be contained in each returned sequence (default = 50)

    Returns
    -------
    sequences : list
        list of strings, where each string is a list of n words as interpreted
        by NLTK's word_tokenize() function.
    '''
    book_words = word_tokenize(book)
    return [' '.join(book_words[i: i+n]) for i in range(0, len(book_words), n)]


def get_character_sequences(book, n=200):
    '''
    Takes a book and splits it into a list of substrings of length n
    (default = 200).

    Parameters
    ----------
    book : string (required)
        book in string form
    n : int (optional)
        number of characters to be contained in each returned sequence
        (default = 200)

    Returns
    -------
    sequences : list
        list of strings comprising the book, where each string is of length n.
    '''
    return [''.join(book[i: i+n]) for i in range(0, len(book), n)]


def find_connections(sequences, characters):
    '''
    Takes a novel and its character list and counts instances of each character
    in each sequence.

    Parameters
    ----------
    sequences : list (required)
        list of substrings representing the novel to be analysed
    characters : list (required)
        list of charater names (as tuples)

    Returns
    -------
    df : pandas.DataFrame
        columns = character names
        indexes = sequences
        values  = counts of instances of character name in sequence
    '''
    if any(len(names) > 1 for names in characters):
        df = pd.DataFrame({str(character):
                           {sequence: sum([sequence.count(name) for name in character])
                            for sequence in sequences}
                           for character in characters})
    else:
        characters = [c[0] for c in characters]
        df = pd.DataFrame([[sequence.count(character)
                            for character in characters]
                           for sequence in sequences],
                          index=sequences,
                          columns=characters)
    return df

def calculate_cooccurence(df):
    '''
    Uses the dot product to calculate the number of times two characters appear
    in the same sequences. This is the core of the bookworm graph.

    Parameters
    ----------
    df : pandas.DataFrame (required)
        columns = character names
        indexes = sequences
        values  = counts of instances of character name in sequence

    Returns
    -------
    cooccurence : pandas.DataFrame
        columns = character names
        indexes = character names
        values  = counts of character name cooccurences in all sequences
    '''
    characters = df.columns.values
    cooccurence = df.values.T.dot(df.values)
    np.fill_diagonal(cooccurence, 0)
    cooccurence = pd.DataFrame(cooccurence, columns=characters, index=characters)
    return cooccurence


def get_interaction_df(cooccurence, threshold=0):
    '''
    Produces an dataframe of interactions between characters using the
    cooccurence matrix of those characters. The return format is directly
    analysable by networkx in the construction of a graph of characters.

    Parameters
    ----------
    cooccurence : pandas.DataFrame (required)
        columns = character names
        indexes = character names
        values  = counts of character name cooccurences in all sequences
    threshold : int (optional)
        The minimum character interaction strength needed to be included in the
        returned interaction_df

    Returns
    -------
    interaction_df : pandas.DataFrame
        DataFrame enumerating the strength of interactions between charcters.
        source = character one
        target = character two
        value = strength of interaction between character one and character two
    '''
    rows, columns = np.where(np.triu(cooccurence.values, 1) > threshold)

    return pd.DataFrame(np.column_stack([cooccurence.index[rows],
                                         cooccurence.columns[columns],
                                         cooccurence.values[rows, columns]]),
                        columns=['source', 'target', 'value'])


def bookworm(book_path, charaters_path=None, threshold=2):
    '''
    Wraps the full bookworm analysis from the raw .txt file's path, to
    production of the complete interaction dataframe. The returned dataframe is
    directly analysable by networkx using:

    nx.from_pandas_dataframe(interaction_df,
                             source='source',
                             target='target')

    Parameters
    ----------
    book_path : string (required)
        path to txt file containing full text of book to be analysed
    charaters_path : string (optional)
        path to csv file containing full list of characters to be examined

    Returns
    -------
    interaction_df : pandas.DataFrame
        DataFrame enumerating the strength of interactions between charcters.
        source = character one
        target = character two
        value = strength of interaction between character one and character two
    '''
    book = load_book(book_path)
    sequences = get_sentence_sequences(book)

    if charaters_path is None:
        characters = extract_character_names(book)
    else:
        characters = load_characters(charaters_path)

    df = find_connections(sequences, characters)
    cooccurence = calculate_cooccurence(df)
    return get_interaction_df(cooccurence, threshold)
