# !/usr/bin/env python

import math
from csv import DictReader
from couchdbkit import Server

keys = ["pickup_datetime", "pickup_latitude", "pickup_longitude", "dropoff_datetime", "dropoff_latitude",
        "dropoff_longitude"]


def parseDoc(doc):
    items = doc.items()
    for k, v in items:
        if (isinstance(v, str)):
            if v.isdigit() == True:  # int
                doc[k] = int(v)
            else:  # try a float
                try:
                    if math.isnan(float(v)) == False:
                        doc[k] = float(v)
                except:
                    pass
    return doc


def trimUnusedColumns(doc):
    items = doc.items()
    for k, v in items:
        if (k not in keys):
            del doc[k]
    return doc

def upload(db, docs):
    db.bulk_save(docs)
    del docs
    return list()


def uploadFile(fname, database):

    reader = DictReader(open(fname, 'rU'), dialect='excel')
    docs = list()
    checkpoint = 100

    for doc in reader:
        parsedDoc = parseDoc(doc)
        newdoc = trimUnusedColumns(parsedDoc)
        docs.append(newdoc)
        if len(docs) % checkpoint == 0:
            docs = upload(database, docs)
    docs = upload(database, docs)


def importCsvToDatabase(filename):
    uri = "http://127.0.0.1:5984/"
    dbname = "taxi_rides"
    dbServer = Server(uri)
    database = dbServer.get_or_create_db(dbname)
    uploadFile(filename, database)
