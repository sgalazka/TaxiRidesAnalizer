import couchdb

import csv_to_database
import googlemaps
import json

import transform

if __name__ == '__main__':
    print("hello world")
    uri = "http://127.0.0.1:5984/"
    dbname = "taxi_rides"

    dbServer = couchdb.Server(uri)

    csv_to_database.importCsvToDatabase("rides.csv")
    transform.transformAddresses(dbServer)

