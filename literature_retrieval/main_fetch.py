from literature_retrieval import api_collector, api_parser, data_handler as dh

# initialize helpers
collector = api_collector.API_collector()
parser = api_parser.Parser()
data_handler = dh.DataHandler()

# query
requests_data = collector.query_apis(terms_list=['data','graph'], operator='OR', max_results='100')

# parse query
processed_data = {}

# add all the data to dict for filtering out duplicates by title (do not forget to update dicts for sources in both parser and controller!)
for source,request in requests_data.items():

    processed_data.update(parser.parse_requests(source, request))

# # save data to file
# data_handler.write_to_file(processed_data)

# save data to the db
db_connection = data_handler.connect_to_db()
data_handler.db_set_up(db_connection)
data_handler.db_update(db_connection, processed_data)
data_handler.db_select_all(db_connection)
db_connection.close()
