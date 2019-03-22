import requests
from xml.etree import ElementTree as et
import re
from pprint import pprint


class Parser:

    def __init__(self):
        self.sources_dict = {'arxiv': self.xml_parse,
                        'springer': self.json_parse}

    def xml_parse(self, request_data):
        root = et.fromstring(request_data.text)
        data = {}
        for element in root:
            # TODO: change into regex, come up with arxiv distinguishment
            if element.tag == '{http://www.w3.org/2005/Atom}entry':
                id = ''
                title = ''
                published = ''
                summary = ''
                link = ''
                author_list = []
                for field in element:
                    # id_search = re.search(r'id', field.tag)
                    # if (id_search): id = 'arxiv_' + re.search(r'[0-9]\w+\.?[0-9]\w+', field.text).group()
                    title_search = re.search(r'title', field.tag)
                    if (title_search): title = field.text
                    published_search = re.search(r'published', field.tag)
                    if (published_search): published = field.text
                    summary_search = re.search(r'summary', field.tag)
                    if (summary_search): summary = field.text
                    link_search = re.search(r'link', field.tag)
                    if (link_search): link = field.attrib['href']
                    author_search = re.search(r'author', field.tag)
                    if (author_search):
                        for name in field:
                            author_name_search = re.search(r'name', name.tag)
                            if author_name_search:
                                author_list.append(name.text)

                data[title] = {'title': title,
                        'publish date': published,
                        'summary': summary,
                        'link': link,
                        'authors': author_list,
                        'source' : 'arxiv',
                        'literature_type': 'paper'
                               }


        return data


    def json_parse(self, request_data):

        # TODO: add distinguishment for springer

        input_data = request_data.json()
        data = {}
        for record in input_data['records']:
            title = record['title']
            link = record['url'][0]['value']
            publish_date = record['publicationDate']
            summary = record['abstract']
            author_list = []
            for creator_dict in record['creators']:
                author_list.append(creator_dict['creator'])
            literature_type = record['contentType']
            data[title] = {'title': title,
                        'publish_date': publish_date,
                        'summary': summary,
                        'link': link,
                        'authors': author_list,
                        'source': 'springer',
                        'literature_type': literature_type
                           }

        return data

    def parse_requests(self,source, request_data):
        return self.sources_dict[source](request_data)

