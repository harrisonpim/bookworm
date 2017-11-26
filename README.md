# Bookworm :books:
Most novels are, in some way, a description of a social network. Bookworm ingests novels, builds a solid version of their implicit character network and spits out a intuitively understandable and deeply analysable graph.

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
 using
```python
characters = load_characters('path/to/character_list.csv')
characters = extract_character_names(book)
```
Find instances of each character in each sequence with `find_connections()`, enumerate out their cooccurences with `calculate_cooccurence()`, and transform that into a more easily interpretable format using `get_interaction_df()`
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

### Navigation
- [src](src) for the code itself.
- Notebooks for example usage (with a load of interwoven description of how the thing actually works), in jupyter notebook form. [Start Here](01%20-%20Intro%20to%20Bookworm.ipynb)
- [data](data) for the example explicit character lists that I've used to test the project. Novel texts are variously available online - [Project Gutenberg](https://www.gutenberg.org/browse/scores/top#books-last30) is a great source of clean data, downloadable in .txt form, while [The British Library](https://data.bl.uk/digbks/) hosts huge amounts of (admittedly poor) OCR in XML form.
