import couchdb
import csv_to_database
import transform
import recostruct
from analize_graph import analize_graph

if __name__ == '__main__':
    uri = "http://admin:admin@127.0.0.1:5984/"
    dbname = "taxi_rides"

    dbServer = couchdb.Server(uri)

    csv_to_database.importCsvToDatabase("rides.csv")
    transform.transformAddresses(dbServer)

    G = recostruct.get_graph_from_db(dbServer)
    recostruct.show(G)
    # Wystarczy jedno wywołanie:
    # analize_graph(G)

