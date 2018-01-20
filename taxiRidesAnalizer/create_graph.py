def create_graph(dbServer):
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
        print("start: {}, end: {}, count: {}".format(start, end, count))
