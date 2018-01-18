import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import numpy as np


def get_graph():
    mdg = nx.MultiDiGraph()
    mdg.add_edge(1, 2)
    mdg.add_edge(1, 2)
    mdg.add_edge(1, 2)
    mdg.add_edge(3, 2)
    mdg.add_edge(3, 2)
    mdg.add_edge(3, 2)
    mdg.add_edge(3, 2)
    mdg.add_edge(2, 4)
    mdg.add_edge(2, 1)
    mdg.add_edge(2, 1)
    mdg.add_edge(2, 1)
    mdg.add_edge(2, 1)
    mdg.add_edge(2, 1)
    mdg.add_edge(2, 1)
    mdg.add_edge(2, 1)
    mdg.add_edge(2, 1)
    return mdg


def get_random_graph():
    return nx.gnm_random_graph(5, 12, seed=None, directed=True)


def merge_edges(M):
    G = nx.DiGraph()
    for u, v in M.edges():
        if G.has_edge(u, v):
            G[u][v]['weight'] += 1
        else:
            G.add_edge(u, v, weight=1)

    for u, v in G.edges():
        G[u][v]['weight'] = round(G[u][v]['weight'] / M.out_degree(u), 2)

    return G


def trim_edges(G):
    for node in G.nodes():
        weights = []
        for u, v in G.edges(node):
            weights.append(G[u][v]['weight'])
        std = np.std(weights)
        mean = np.mean(weights)
        min_weight = mean # - std
        edges_to_remove = [(u, v) for u, v in G.edges(node) if G[u][v]['weight'] < min_weight]
        G.remove_edges_from(edges_to_remove)

    not_connected_nodes = [node for node in G.nodes() if G.degree(node) == 0]
    G.remove_nodes_from(not_connected_nodes)

    return G


def directed_to_bipartie(D):
    B = nx.Graph()
    B.add_nodes_from(D.nodes(), bipartite=0)
    B.add_nodes_from(map(lambda x: -1*x, D.nodes()), bipartite=1)
    for u, v in D.edges():
        B.add_edge(u, -1*v)
    return B


def project(G):
    pickup_nodes = [node for node in G.nodes() if node > 0]
    G = bipartite.projected_graph(G, pickup_nodes)
    return G


# def reconstruct(directed_multigraph):
#     directed_weighted_graph = merge_edges(directed_multigraph)
#     # trim edges
#     trimmed_directed_weighted_graph = trim_edges(directed_weighted_graph)
#     # bipartie graph (not directed)
#     # projection
#     return trimmed_directed_weighted_graph


def show(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos)

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=0.8)

    nx.draw_networkx_labels(G, pos)

    plt.show()


if __name__ == '__main__':
    g = get_graph()
    show(g)
    g = merge_edges(g)
    show(g)
    g = trim_edges(g)
    show(g)
    g = directed_to_bipartie(g)
    show(g)
    g = project(g)
    show(g)


