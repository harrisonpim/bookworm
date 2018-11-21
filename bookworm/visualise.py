import community
import matplotlib.pyplot as plt
import networkx as nx


def draw_with_communities(book):
    partitions = community.best_partition(book)
    values = [partitions.get(node) for node in book.nodes()]

    nx.draw(book,
            cmap=plt.get_cmap("RdYlBu"),
            node_color=values,
            with_labels=True)