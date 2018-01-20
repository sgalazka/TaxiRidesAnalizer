import googlemaps


def transformAddresses(dbServer):
    taxiRidesDb = dbServer.get_or_create_db('taxi_rides')
    ridesDb = dbServer.get_or_create_db('rides')
    gmaps = googlemaps.Client(key='AIzaSyBabsATfHAXSihzTwbxTjV9Jqh3MrmZVHs')

    taxiRidesRows = taxiRidesDb.view('_all_docs', include_docs=True)
    taxiRides = [row['doc'] for row in taxiRidesRows]
    for taxiRide in taxiRides:
        newRide = {}
        startPointResponce = gmaps.reverse_geocode((taxiRide['pickup_latitude'], taxiRide['pickup_longitude']))
        endPointResponce = gmaps.reverse_geocode((taxiRide['dropoff_latitude'], taxiRide['dropoff_longitude']))
        startPointData = next(iter(startPointResponce), None)
        endPointData = next(iter(endPointResponce), None)
        newRide['start_address'] = startPointData['formatted_address']
        print(startPointData['formatted_address'])
        print(startPointData['types'])
        print(endPointData['formatted_address'])
        print(endPointData['types'])
        newRide['end_address'] = endPointData['formatted_address']
        queryParams = {
            'start_address': startPointData['formatted_address'],
            'end_address': startPointData['formatted_address']
        }

        map_fun = '''function(doc) {
            if (doc.start_address==startPointData['formatted_address'] && doc.end_address==endPointData['formatted_address'])
        }'''
        ridesView = ridesDb.query(map_fun)
        # todo Tu chciałem dostać listę obiektów spełniających podane warunki
        for row in ridesView:
            print("emitted row ", row)
        print(newRide)
        ridesDb.save_doc(newRide)
