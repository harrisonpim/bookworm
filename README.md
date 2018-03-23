# Bookworm :books:
Most novels are, in some way, a description of a social network. Bookworm ingests novels, builds a solid version of their implicit character network and spits out a intuitively understandable and deeply analysable graph.


### Navigation
- [bookworm](bookworm) for the code itself.
- Notebooks including example usage (with a load of interwoven description of how the thing actually works), in jupyter notebook form. [Start Here](01%20-%20Intro%20to%20Bookworm.ipynb)
- [data](data) for a description of how to get hold of data so that you can run bookworm yourself.


### Usage
#### Command Line Usage
The `bookworm('path/to/book.txt')` function wraps the following steps into one simple command, allowing the entire analysis process to be run easily from the command line
```bash
python run_bookworm.py --path 'path/to/book.txt'
```
- Add `--d3` to format the output for interpretation by the d3.js force directed graph
- Add `--threshold n` where n is an integer to specify the minimum character interaction strength to be included in the output (default 2)
- Add `--output_file 'path/to/file'` to specify where the .json or .csv should be left


#### Detailed API Usage
Start by loading in a book
```python
book = load_book('path/to/book.txt')
```
Split the book into individual sentences, sequences of `n` words, or sequences of `n` characters by respectively running
```python
sequences = get_sentence_sequences(book)
sequences = get_word_sequences(book, n=50)
sequences = get_character_sequences(book, n=200)
```
Manually input a list of character names or automatically extract a list of 'plausible' character names by respectively using
```python
characters = load_characters('path/to/character_list.csv')
characters = extract_character_names(book)
```
Find instances of each character in each sequence with `find_connections()`, enumerate their cooccurences with `calculate_cooccurence()`, and transform that into a more easily interpretable format using `get_interaction_df()`
```python
df = find_connections(sequences, characters)
cooccurence = calculate_cooccurence(df)
interaction_df = get_interaction_df(cooccurence, characters)
```
The resulting dataframe can be easily transform into a networkx graph using
```python
nx.from_pandas_dataframe(interaction_df,
                         source='source',
                         target='target')
```
From there, all sorts of interesting analysis can be done. See the project's [associated jupyter notebooks](01%20-%20Intro%20to%20Bookworm.ipynb) and the [networkx documentation](https://networkx.github.io/documentation/stable/index.html) for more details.

### Slides
I presented a bunch of this stuff at
- :statue_of_liberty: [PyData NYC 17](data/other-files/Bookworm,%20PyData%20NYC%2017.pdf)
- :beers: [Databeers London](data/other-files/Bookworm,%20Databeers%20London%202018.pdf)
