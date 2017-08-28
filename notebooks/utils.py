import csv
import nltk
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from random import randint


def load_book(bookPath):
    with open(bookPath) as f:
        book = f.read()
        book = book.lower()
    return book


def load_characters(charatersPath):
    with open(charatersPath) as f:
        reader = csv.reader(f)
        characters = [tuple(name.lower()+' ' for name in row) for row in reader]
    return characters


def get_sentence_sequences(book):
    detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = detector.tokenize(book)
    return sentences


def get_word_sequences(book, n=50):
    book_words = word_tokenize(book)
    return [' '.join(book_words[i : i+n]) for i in range(0, len(book_words), n)]


def get_character_sequences(book, n=200):
    return [''.join(book[i : i+n]) for i in range(0, len(book), n)]


def get_sequence_hashes(sequences):
    hash_to_sequence = {hash(s): s for s in sequences}
    sequence_to_hash = {s: hash(s) for s in sequences}
    return hash_to_sequence, sequence_to_hash


def get_character_hashes(characters):
    hash_to_character = {hash(c): c for c in characters}
    character_to_hash = {c: hash(c) for c in characters}
    return hash_to_character, character_to_hash


def find_connections(sequences, characters):
    # get hashes for characters and sequences
    hash_to_sequence, sequence_to_hash = get_sequence_hashes(sequences)
    hash_to_character, character_to_hash = get_character_hashes(characters)
    
    # instantiate blank dataframe
    df = pd.DataFrame({hash(c): {hash(s): 0 for s in sequences} for c in characters})
    
    # populate that dataframe with character instances in each sequence
    for sequence in sequences:
        for character in characters:
            if any(name in sequence for name in character):
                df[hash(character)][hash(sequence)] += 1
    return df


def calculate_cooccurence(df):
    cooccurence = df.T.dot(df)
    for i in cooccurence.index.values:
        cooccurence[i][i] = 0
    return cooccurence