# Bookworm :books:
Most novels are, in some way, a description of a social network. Bookworm ingests novels, builds a solid version of their implicit character network and spits out a intuitively understandable and deeply analysable graph.

### Motivation
_Infinite Jest_ is a very long and complicated novel. There are a lot of brilliant resources connected to the book, which aim to help the reader stay afloat amongst the chaos of David Foster Wallace's obscure language, interwoven timelines and narratives, and the sprawling networks of characters. The [Infinite Jest Wiki](http://infinitejest.wallacewiki.com/david-foster-wallace/index.php?title=Infinite_Jest_Page_by_Page), for example, is insanely well documented and I'd recommend it to anyone reading the book.  
One of the most interesting resources I found while reading was Sam Potts' [Infinite Jest Diagram](http://www.sampottsinc.com/ij/).  

![alt text](https://a.fastcompany.net/upload/IJ_Diagram-Huge-A.jpg "IJmap")

I genuinely went back to the image once or twice to work out who a character was and how they were connected to the scene. It's a fun thing to have access to while reading something so deliberately scattered.  
However, Infinite Jest isn't the only "big" book I've ever read, and as far as I know the network above was drawn up entirely by hand. I thought it would be nice to have something like this for anything I was reading. It might also function as an interesting learning resource - either for kids at a young, early-reader stage with simple books and small character networks, or for people learning about network analysis who have never bothered reading [Les Miserables](https://bl.ocks.org/mbostock/4062045) (again, as far as I know the standard Les Mis dataset was put together entirely by hand).  
I thought that with a bit of thought and testing, this process was probably automatable. It is. I can now feed Bookworm any novel and have it churn out a pretty network like the one above in seconds, without me having to know anything about the book. Also, by virtue of the way character connections are measured, it can tell you the relative strength of all links between characters.

### Usage
#### Command Line Usage
The `bookworm('path/to/book.txt')` function wraps the following steps into one simple command, allowing the entire analysis process to be run easily from the command line
```bash
python src/run_bookworm.py 'path/to/book.txt'
```

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
From there, all sorts of interesting analysis can be done. See the project's [associated jupyter notebooks](notebooks) and the [networkx documentation](https://networkx.github.io/documentation/stable/index.html) for more details.

### Navigation
- [src](src) for the code itself.
- Notebooks for example usage (with a load of interwoven description of how the thing actually works), in jupyter notebook form. [Start Here!](./01%20-%20Intro to Bookworm.ipynb)
- [data](data) for the example explicit character lists that I've used to test the project. Novel texts are variously available online - [Project Gutenberg](https://www.gutenberg.org/browse/scores/top#books-last30) is a great source of clean data, downloadable in .txt form, while [The British Library](https://data.bl.uk/digbks/) hosts huge amounts of (admittedly poor) OCR in XML form.
