import networkx as nx
from networkx.utils import is_string_like, open_file


def analize_graph(G):
    print("Wczytano graf. {} wierzchołków, {} krawędzi".format(G.order(), len(G.edges)))
    numberOfConnectedComponents = getNumberOfConnectedComponents(G)
    print("liczba składowych spójnych: ", numberOfConnectedComponents)
    printConnectedComponents(G)
    printTheLargestComponent(G)
    largestComponent = getTheLargestComponent(G)
    closeness = getClosenessForAllNodes(largestComponent)
    print("5 węzłów o największej bliskości: ", sorted(closeness)[-5:])
    betweeness = getBetwennessForAllNodes(largestComponent)
    print("5 węzłów o największym pośrednictwie: ", sorted(betweeness)[-5:])
    rank = getRankForAllNodes(largestComponent)
    print("5 węzłów o największej randze: ", sorted(rank)[-5:])
    printCliques(largestComponent)


def generate_pajek(G):
    if G.name == '':
        name = 'NetworkX'
    else:
        name = G.name

    yield '*vertices %s' % (G.order())
    nodes = list(G)

    nodenumber = dict(zip(nodes, range(1, len(nodes) + 1)))
    for n in nodes:
        na = G.nodes.get(n, {"s": "S"})
        x = na.get('x', 0.0)
        y = na.get('y', 0.0)
        # print("node: ", n)
        id = int(na.get('id', nodenumber[n]))
        nodenumber[n] = id
        shape = na.get('shape', 'ellipse')
        s = ' '.join(map(make_qstr, (id, n, x, y, shape)))
        for k, v in na.items():
            if v.strip() != '':
                s += ' %s %s' % (make_qstr(k), make_qstr(v))
        yield s

    # write edges with attributes
    if G.is_directed():
        yield '*arcs'
    else:
        yield '*edges'
    for u, v, edgedata in G.edges(data=True):
        d = edgedata.copy()
        # print("edgeData: ",d)
        value = d.pop('value', 1.0)  # use 1 as default edge value
        s = ' '.join(map(make_qstr, (nodenumber[u], nodenumber[v], value)))
        # print ("vertex ",v)
        for k, v in d.items():
            if isinstance(v, str):
                if v.strip() != '':
                    s += ' %s %s' % (make_qstr(k), make_qstr(v))
        yield s


@open_file(1, mode='wb')
def write_pajek(G, path, encoding='UTF-8'):
    for line in generate_pajek(G):
        line += '\n'
        path.write(line.encode(encoding))


def make_qstr(t):
    if not is_string_like(t):
        t = str(t)
    if " " in t:
        t = r'"%s"' % t
    return t


def getNumberOfConnectedComponents(G):
    return nx.number_connected_components(G)


def printConnectedComponents(G):
    components = nx.connected_component_subgraphs(G)
    sizesOfComponents = dict()
    for c in components:
        if str(c.order()) in sizesOfComponents:
            count = sizesOfComponents.get(str(c.order()))
            t = {}
            t[str(c.order())] = count + 1
            sizesOfComponents.update(t)
        else:
            d = {}
            d[str(c.order())] = 1
            sizesOfComponents.update(d)
    print("Rzędy skłądowych:")
    print("rozmiar\tilość wystąpień")
    for s in sizesOfComponents.items():
        print(" ", s[0], "\t", s[1])


def printTheLargestComponent(G):
    components = nx.connected_component_subgraphs(G)
    largest = max(components, key=len)
    print("Największa spójna składowa ma ", largest.order(), " wierzchołków")


def getTheLargestComponent(G):
    components = nx.connected_component_subgraphs(G)
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
