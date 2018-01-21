#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
from networkx.utils import is_string_like, open_file
import matplotlib.pyplot as plt
import numpy as np


def read_graph(file_path):
    G = nx.read_weighted_edgelist(file_path)
    return G


def save_graph(G, file_path):
    nx.write_weighted_edgelist(G, file_path)


def analize_graph(G):
    print("Wczytano graf. {} wierzchołków, {} krawędzi".format(G.order(), len(G.edges)))
    numberOfConnectedComponents = getNumberOfConnectedComponents(G)
    print("liczba składowych spójnych: " + str(numberOfConnectedComponents))
    largestComponent = getTheLargestComponent(G)
    print("Największa spójna składowa ma {} wierzchołków, {} krawędzi".format(largestComponent.order(), len(largestComponent.edges)))
    closeness = getClosenessForAllNodes(largestComponent)
    print("5 węzłów o największej bliskości: " + str(sorted(closeness)[-5:]))
    betweeness = getBetwennessForAllNodes(largestComponent)
    print("5 węzłów o największym pośrednictwie: " + str(sorted(betweeness)[-5:]))
    rank = getRankForAllNodes(largestComponent)
    print("5 węzłów o największej randze: " + str(sorted(rank)[-5:]))
    printCliques(largestComponent)


def getNumberOfConnectedComponents(G):
    return nx.number_connected_components(G)


def getTheLargestComponent(G):
    components = nx.connected_component_subgraphs(G, copy=False)
    largest = max(components, key=len)
    return largest


def getClosenessForAllNodes(G):
    closenessList = nx.closeness_centrality(G)
    #    for cl in closenessList:
    #        print("closenessList: ",closenessList[cl])
    #        print("{\"", cl,"\" : \"",closenessList[cl],"\" }")
    return closenessList


def getRankForAllNodes(G):
    rankList = nx.pagerank(G)
    #    for cl in rankList:
    #        print("rankList: ",rankList[cl])
    #        print("{\"", cl,"\" : \"",rankList[cl],"\" }")
    return rankList


def getBetwennessForAllNodes(G):
    betweennessList = nx.betweenness_centrality(G, normalized=True)

    #    for cl in betweennessList:
    #        print("betweennessList: ",betweennessList[cl])
    #        print("{\"", cl,"\" : \"",betweennessList[cl],"\" }")
    return betweennessList


def printCliques(G):
    cliques = nx.find_cliques(G)
    sizesOfCliques = dict()
    for c in cliques:
        if str(len(c)) in sizesOfCliques:
            count = sizesOfCliques.get(str(len(c)))
            t = {}
            t[str(len(c))] = count + 1
            sizesOfCliques.update(t)
        else:
            d = {}
            d[str(len(c))] = 1
            sizesOfCliques.update(d)
    print("Rzędy klik:")
    print("rozmiar\tilość wystąpień")
    for s in sizesOfCliques.items():
        print(" ", s[0], "\t", s[1])


def plot(data, filename, degreetype):
    """ Plot Frequency """
    plt.figure()
    freq = np.bincount(data)
    plt.plot(range(len(freq)), freq, 'bo')
    plt.title("Czestosc wystapien stopni wierzcholkow")
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Czestosc wystapienia')
    plt.xlabel('stopien wierzcholka')
    plt.draw()
    plt.show()
    plt.clf()

    """ Plot CCDF """
    s = float(data.sum())
    cdf = data.cumsum(0) / s
    ccdf = 1 - cdf
    plt.figure()
    plt.plot(range(len(ccdf)), ccdf, 'b-')
    plt.title("CCDF")
    plt.xscale('log')
    plt.yscale('log')
    plt.ylim([0, 1])
    plt.xlim([0, 90000])
    plt.ylabel('P(X>d)')
    plt.xlabel('stopień wierzchołka')
    plt.draw()
    plt.show()
    plt.clf()
    #
    # log_x = list(map(math.log, list(range(len(ccdf)))[1:-1]))
    # log_y = list(map(math.log, ccdf[1:-1]))
    # slope, intercept, _, _, _ = stats.linregress(log_x, log_y)
    # # plt.plot(x1, y1, x2, y2, marker='o')
    # print(slope)
    # print(intercept)
    #
    # """ Plot Distribution """
    #
    # def myExpFunc(x):
    #     return math.e ** (-2.32943479262 * x)
    #
    # new_x = range(8)
    # new_y = map(myExpFunc, new_x)
    # plt.figure()
    # plt.yscale('log')
    # plt.xscale('log')
    # plt.plot(list(new_x), list(new_y), 'r-')
    # plt.ylim([0, 1])
    # # plt.xlim([0, 90000])
    # plt.draw()
    # # plt.clf()
    #
    # # popt, pcov = curve_fit(myExpFunc, range(1, 1+len(ccdf)), ccdf)


def trim_edges(G, min_weight):
    edges_to_remove = [(u, v) for u, v in G.edges() if G[u][v]['weight'] < min_weight]
    G.remove_edges_from(edges_to_remove)
    return G


if __name__ == '__main__':
    print('read merged-12.graph')
    g12 = read_graph('merged-12-trimmed.graph')
    # g12 = trim_edges(g12, 15)
    # save_graph(g12, 'merged-12-trimmed.graph')
    # g12 = nx.gnm_random_graph(1000, 12000, seed=None, directed=False)
    analize_graph(g12)

    # print(nx.degree(g12))
    degrees_dict = dict(nx.degree(g12))
    degrees = sorted(degrees_dict.values())
    print(str(degrees[-1]) + " " + str(degrees_dict.keys()[degrees_dict.values().index(degrees[-1])]))
    print(str(degrees[-2]) + " " + str(degrees_dict.keys()[degrees_dict.values().index(degrees[-2])]))
    print(str(degrees[-3]) + " " + str(degrees_dict.keys()[degrees_dict.values().index(degrees[-3])]))
    print(str(degrees[-4]) + " " + str(degrees_dict.keys()[degrees_dict.values().index(degrees[-4])]))
    print(str(degrees[-5]) + " " + str(degrees_dict.keys()[degrees_dict.values().index(degrees[-5])]))
    plot(degrees, 'file', 'indegree')
