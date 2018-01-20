from couchdbkit import Server

import csv_to_database
import googlemaps
import json

import transform

if __name__ == '__main__':
    print("hello world")
    uri = "http://127.0.0.1:5984/"
    dbname = "taxi_rides"
    dbServer = Server(uri)
    db = dbServer.get_or_create_db(dbname)

    # csv_to_database.importCsvToDatabase("rides.csv", db)
    transform.transformAddresses(dbServer)
    # gmaps = googlemaps.Client(key='AIzaSyBabsATfHAXSihzTwbxTjV9Jqh3MrmZVHs')
    # res = gmaps.reverse_geocode((40.714224, -73.961452))
    #
    # x = next(iter(res), None)
    # print(x['formatted_address'])
    #
    #
    # rows = db.view("_all_docs", include_docs=True)
    # for row in rows:
    #     print(row)
    #     print(type(row))
    # docs = [row['doc'] for row in rows]
    # for doc in docs:
    #     print(type(doc))
    #     print(doc['dropoff_datetime'])
