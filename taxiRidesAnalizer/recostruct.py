import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import numpy as np
import googlemaps


def get_manual_graph():
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


def get_graph_from_csv(file_path):

    mdg = nx.DiGraph()
    gmaps = googlemaps.Client(key='AIzaSyBabsATfHAXSihzTwbxTjV9Jqh3MrmZVHs')

    with open(file_path, 'r') as f:
        header_line = f.readline()
        header = {}
        for head in header_line.split(','):
            header[head] = len(header)
        f.readline()  # empty line

        for data_line in f:
            try:
                data = data_line.split(',')
                pickup_longitude = float(data[header['pickup_longitude']])
                pickup_latitude = float(data[header['pickup_latitude']])
                dropoff_longitude = float(data[header['dropoff_longitude']])
                dropoff_latitude = float(data[header['dropoff_latitude']])

                if not (-80.0 < pickup_longitude < -70.0) or \
                        not (35.0 < pickup_latitude < 45.0) or \
                        not (-80.0 < dropoff_longitude < -70.0) or \
                        not (35.0 < dropoff_latitude < 45.0):
                    # print('Skipping line due to strange geo: ' + str(pickup_longitude) + ' '
                    #       + str(pickup_latitude) + ' '
                    #       + str(dropoff_longitude) + ' '
                    #       + str(dropoff_latitude) + ' ')
                    continue

                if False:  # True - use Google; False - hash lat and lng
                    startPointResponce = gmaps.reverse_geocode((pickup_latitude, pickup_longitude))
                    endPointResponce = gmaps.reverse_geocode((dropoff_latitude, dropoff_longitude))
                    startPointData = next(iter(startPointResponce), None)
                    endPointData = next(iter(endPointResponce), None)

                    startPointPlaceId = startPointData['place_id']
                    endPointPlaceId = endPointData['place_id']
                else:
                    def my_hash(lat, lng):
                        precision = 3
                        lat_int = int(round(abs(lat), precision) * 10**precision)
                        lng_int = int(round(abs(lng), precision) * 10**precision)
                        hashed = int(str(lng_int) + str(lat_int))
                        return hashed
                    startPointPlaceId = my_hash(pickup_latitude, pickup_longitude)
                    endPointPlaceId = my_hash(dropoff_latitude, dropoff_longitude)

                if mdg.has_edge(startPointPlaceId, endPointPlaceId):
                    mdg[startPointPlaceId][endPointPlaceId]['weight'] += 1
                else:
                    mdg.add_edge(startPointPlaceId, endPointPlaceId)
                    mdg[startPointPlaceId][endPointPlaceId]['weight'] = 1
            except ValueError:
                print("Bad line: " + data_line)

    return mdg


def get_random_graph():
    return nx.gnm_random_graph(10000, 1200000, seed=None, directed=True)


def get_graph_from_db(dbServer):
    G = nx.DiGraph()

    try:
        ridesDb = dbServer['rides']
    except:
        ridesDb = dbServer.create('rides')

    ridesRows = ridesDb.view('_all_docs', include_docs=True)
    rides = [row['doc'] for row in ridesRows]

    for ride in rides:
        start = ride['start_address']
        end = ride['end_address']
        count = ride['count']
        G.add_edge(start, end, weight=count)
        print("start: {}, end: {}, count: {}".format(start, end, count))

    return G


def save_graph(G, file_path):
    nx.write_weighted_edgelist(G, file_path)


def read_graph(file_path):
    G = nx.read_weighted_edgelist(file_path, create_using=nx.MultiDiGraph)
    return G


def merge_edges(M):
    G = nx.DiGraph()
    for u, v in M.edges():
        if G.has_edge(u, v):
            G[u][v]['weight'] += 1
        else:
            G.add_edge(u, v, weight=1)

    return G


def calculate_weights(G):
    for node in G.nodes():
        weights_sum = 0
        for u, v in G.edges(node):
            weights_sum += G[u][v]['weight']
        for u, v in G.edges(node):
            G[u][v]['weight'] = round(G[u][v]['weight'] / weights_sum, 2)

    return G


def trim_edges(G):
    for node in G.nodes():
        weights = []
        for u, v in G.edges(node):
            weights.append(G[u][v]['weight'])
        if weights:
            std = np.std(weights)
            mean = np.mean(weights)
            min_weight = mean - std
            edges_to_remove = [(u, v) for u, v in G.edges(node) if G[u][v]['weight'] < min_weight]
            G.remove_edges_from(edges_to_remove)

    return G


def remove_unconnected_nodes(G):
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


def project(B):
    pickup_nodes = [node for node in B.nodes() if node > 0]
    P = bipartite.projected_graph(B, pickup_nodes)
    return P


def show(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos)

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=0.8)

    nx.draw_networkx_labels(G, pos)

    plt.show()


def merge_graphs(G1, G2):
    for u, v in G2.edges():
        if G1.has_edge(u, v):
            G1[u][v]['weight'] += 1
        else:
            G1.add_edge(u, v, weight=1)

    return G1


if __name__ == '__main__':
    def process_one_week(week):
        print("get_graph")
        g = get_graph_from_csv(week)
        print("calculate_weights")
        g = calculate_weights(g)
        print("trim_edges")
        g = trim_edges(g)
        g = remove_unconnected_nodes(g)
        print("directed_to_bipartie")
        g = directed_to_bipartie(g)
        g = remove_unconnected_nodes(g)
        print("project")
        g = project(g)
        g = remove_unconnected_nodes(g)
        print("finish")
        # save_graph(g, week + '.graph')
        return g

    G = nx.Graph()
    for g_name in ['aaa/' + str(num) for num in range(335, 366)]:
        try:
            print(g_name)
            G_add = process_one_week(g_name)
            G = merge_graphs(G, G_add)
            del G_add
        except IOError:
            print('Could not process file')

    file_name = 'merged.graph'
    print('saving graph to ' + file_name)
    save_graph(G, file_name)


