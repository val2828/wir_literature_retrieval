from literature_retrieval import api_collector, api_parser, db_handler as dh


def select_query(column):
    data_handler = dh.DataHandler()
    db_connection = data_handler.connect_to_db()
    data_handler.db_select_column(db_connection, column)

def run_db_updates(queries):
    # queries is the list of list of terms - in case we want to include multiple terms per query
    # initialize helpers
    collector = api_collector.API_collector()
    parser = api_parser.Parser()
    data_handler = dh.DataHandler()

    db_connection = data_handler.connect_to_db()

    for query in queries:
        # query
        requests_data = collector.query_apis(terms_list=query, operator='AND', max_results='100')

        # parse query
        processed_data = {}
        # removing duplictes, if add source - update parser and controller source dicts
        for source,request in requests_data.items():
            processed_data.update(parser.parse_requests(source, request))

        # save data to the db

        data_handler.db_update(db_connection, processed_data)
        # data_handler.db_select_all(db_connection)

    db_connection.close()

# run_db_updates([['graph'], ['theory']])
select_query('title')