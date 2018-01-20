import couchdb
import csv_to_database
import transform
import recostruct

if __name__ == '__main__':
    uri = "http://admin:admin@127.0.0.1:5984/"
    dbname = "taxi_rides"

    dbServer = couchdb.Server(uri)

    csv_to_database.importCsvToDatabase("rides.csv")
    transform.transformAddresses(dbServer)

    G = recostruct.create_graph(dbServer)
    recostruct.show(G)

