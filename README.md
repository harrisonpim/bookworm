# Bookworm :books:
Most novels are, in some way, a description of a social network. I've built something which builds a solid version of that implied network and spits out beautiful, queryable graph.

#### Why did I do this thing
_Infinite Jest_ is a very long and complicated novel. There are a lot of brilliant resources connected to the book, which aim to help the reader stay afloat amongst the chaos of David Foster Wallace's obscure language, interwoven timelines and narratives, and the sprawling networks of characters. The [Infinite Jest Wiki](http://infinitejest.wallacewiki.com/david-foster-wallace/index.php?title=Infinite_Jest_Page_by_Page), for example, is insanely well documented and I'd recommend it to anyone reading the book.  
One of the most interesting resources I found while reading was Sam Potts' [Infinite Jest Diagram](http://www.sampottsinc.com/ij/).  

![alt text](https://a.fastcompany.net/upload/IJ_Diagram-Huge-A.jpg "IJmap")

I genuinely went back to the image once or twice to work out who a character was and how they were connected to the scene. It's a fun thing to have access to while reading something so deliberately scattered.  
However, Infinite Jest isn't the only "big" book I've ever read, and as far as I know the network above was drawn up entirely by hand. I thought it would be nice to have something like this for anything I was reading. It might also function as an interesting learning resource - either at a young, early-reader stage with simple books and small character networks, or for people learning about network analysis who have never bothered reading [Les Miserables](https://bl.ocks.org/mbostock/4062045) (again, the standard Les Mis dataset was put together entirely by hand).  
I thought that with a bit of thought and testing, this process was probably automatable. I can now feed Bookworm any novel and have it churn out a pretty network like the one above in seconds, without me having to know anything about the book. Also, by virtue of the way links are measured, it can tell you the relative strength of all links between characters.

### Repo Navigation
- [data](data) for the example texts I've used to test the project. Technically these aren't in the public domain yet so i should probably switch these out for some of the books made available through [Project Gutenberg](https://www.gutenberg.org/browse/scores/top#books-last30) instead.
- [notebooks](notebooks) for example usage (with a load of interwoven description of how the thing actually works), in jupyter notebook form.
- [src](src) for the code itself.
