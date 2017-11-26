import community
import matplotlib.pyplot as plt
import networkx as nx


def draw_with_communities(book):
    '''
    draw a book's network with its nodes coloured by (detected) community

    Parameters
    ----------
    book : nx.Graph (required)
        graph to be analysed and visualised
    '''
    partitions = community.best_partition(book)
    values = [partitions.get(node) for node in book.nodes()]

    nx.draw(book,
            cmap=plt.get_cmap("RdYlBu"),
            node_color=values,
            with_labels=True)


def d3_dict(interaction_df):
    '''
    Reformats a DataFrame of interactions into a dictionary which is
    interpretable by the Mike Bostock's d3.js force directed graph script
    https://bl.ocks.org/mbostock/4062045

    Parameters
    ----------
    interaction_df : pandas.DataFrame (required)
        DataFrame enumerating the strength of interactions between charcters.
        source = character one
        target = character two
        value = strength of interaction between character one and character two

    Returns
    -------
    d3_dict : dict
        a dictionary of nodes and links in a format which is immediately
        interpretable by the d3.js script
    '''
    nodes = [{"id": str(id), "group": 1} for id in set(interaction_df['source'])]
    links = interaction_df.to_dict(orient='records')
    return {'nodes': nodes, 'links': links}
