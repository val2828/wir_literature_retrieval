import requests
import re
from pprint import pprint




class API_collector:

    def __init__(self):
        self.sources_dict = {'arxiv': self.generate_arxiv_url,
                        'springer': self.generate_springer_url}

    def generate_arxiv_url(self, terms_list, operator,max_results='10'):

        query_type = 'search_query'

        query = ''
        for id, term in enumerate(terms_list):
            if len(terms_list) - id > 1:
                query += term + '+' + operator + '+'
            else:
                query += term


        url = f'http://export.arxiv.org/api/query?{query_type}=all:{query}&max_results={max_results}'

        return url

    def generate_springer_url(self, terms_list, operator, search_method='keyword', max_results='10'):

        # max_results denoted with p in Spinger, max allowed is 100

        user_key = 'dbebbf24eeba1fbb3915edeef3acc32e'
        method = 'metadata'
        format = 'json'



        query = '('
        for id, term in enumerate(terms_list):
            if len(terms_list) - id > 1:
                query += search_method + ':' + term + " " + operator + " "
            else:
                query += search_method + ':' + term + ')'

        url = f'http://api.springernature.com/{method}/{format}?q={query}&p={max_results}&api_key={user_key}'
        return url



    def query_apis(self, terms_list, operator, max_results='10'):

        collected_requests = {}

        for source_name, source_method in self.sources_dict.items():
            query_url = source_method(terms_list=terms_list,operator=operator, max_results=max_results)
            current_request = requests.get(query_url)
            if current_request.raise_for_status() is None:
                collected_requests[source_name] = current_request

        return collected_requests

