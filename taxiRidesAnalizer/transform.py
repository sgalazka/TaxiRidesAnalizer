import googlemaps


def transformAddresses(dbServer):
    try:
        taxiRidesDb = dbServer['taxi_rides']
    except:
        taxiRidesDb = dbServer.create('taxi_rides')
    try:
        ridesDb = dbServer['rides']
    except:
        ridesDb = dbServer.create('rides')

    gmaps = googlemaps.Client(key='AIzaSyBabsATfHAXSihzTwbxTjV9Jqh3MrmZVHs')

    taxiRidesRows = taxiRidesDb.view('_all_docs', include_docs=True)
    taxiRides = [row['doc'] for row in taxiRidesRows]
    index = 0
    for taxiRide in taxiRides:

        startPointResponce = gmaps.reverse_geocode((taxiRide['pickup_latitude'], taxiRide['pickup_longitude']))
        endPointResponce = gmaps.reverse_geocode((taxiRide['dropoff_latitude'], taxiRide['dropoff_longitude']))
        startPointData = next(iter(startPointResponce), None)
        endPointData = next(iter(endPointResponce), None)
        startAddress = startPointData['formatted_address']
        endAddress = endPointData['formatted_address']

        map_fun = '''function(doc) {
                    emit([doc.start_address, doc.end_address], doc._id);
                }'''
        ridesView = ridesDb.query(map_fun=map_fun,
                                  key=[startPointData['formatted_address'], endPointData['formatted_address']])
        if (len(ridesView) >= 1):
            searchedRide = next(iter(ridesView), None)
            print("incremented: ", searchedRide.value)
            existingRide = ridesDb[searchedRide.value]
            currentCount = existingRide['count']
            existingRide['count'] = currentCount + 1
            ridesDb[searchedRide.value] = existingRide
        else:
            newRide = {}
            newRide['start_address'] = startAddress
            newRide['end_address'] = endAddress
            newRide['count'] = 1
            print('added ride: ', newRide)
            ridesDb[str(index)] = newRide
            index = index + 1
