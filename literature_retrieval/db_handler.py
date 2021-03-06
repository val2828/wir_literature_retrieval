import json
from pprint import pprint
import psycopg2
from psycopg2 import sql

class DataHandler:
    COMMANDS = {'create_table' : """
        CREATE TABLE articles (
            article_id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            publish_date VARCHAR(255),
            summary TEXT,
            link VARCHAR(255),
            authors TEXT ARRAY,
            source VARCHAR(255),
            literature_type VARCHAR(255)
            );
        """,
                'delete_table' : """
        DROP TABLE articles;
        """,
                'check_existence' : """
        SELECT EXISTS (
            SELECT 1 
            FROM   pg_tables
            WHERE  schemaname = 'public'
            AND    tablename = 'articles'
            );
        """,
                'update_table' : """
        INSERT INTO articles(title, publish_date, summary, link, authors, source, literature_type) VALUES(%s, %s, %s, %s, %s, %s, %s);
        """,
                'select_all' : """
        SELECT * FROM articles;
        """,
                'check_if_such_already_exists': ("""
        select exists ( select title from articles where {} = %(value)s);   
        """),
                'select_column': """
        SELECT {} FROM articles;
        """,
    }




    def connect_to_db(self):
        try:
            connection = psycopg2.connect(user = "valentin",
                                          password = "mydb",
                                          host = "127.0.0.1",
                                          port = "5432",
                                          database = "valentin")
            print(connection.get_dsn_parameters(), "\n")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting " , error)

        return connection



    def db_set_up(self, connection):
        cursor = connection.cursor()
        cursor.execute(self.COMMANDS['check_existence'])
        if not cursor.fetchone()[0]:
            cursor.execute(self.COMMANDS['create_table'])
            print('table was created')
        else:
            cursor.execute(self.COMMANDS['delete_table'])
            print('table deleted')
            cursor.execute(self.COMMANDS['create_table'])
            print('table was created')
        connection.commit()
        cursor.close()

    def db_select_all(self, connection):
        cursor = connection.cursor()
        cursor.execute(self.COMMANDS['select_all'])
        pprint(cursor.fetchall())
        cursor.close()

    def db_select_column(self, connection, column):
        cursor = connection.cursor()
        cursor.execute(sql.SQL(self.COMMANDS['select_column']).format(sql.Identifier(column)))
        pprint(cursor.fetchall())
        cursor.close()

    def db_check_if_record_exists(self, connection, column, value):
        cursor = connection.cursor()
        cursor.execute(sql.SQL(self.COMMANDS['check_if_such_already_exists']).format(sql.Identifier(column)), {'value' : value})
        return cursor.fetchone()[0]

    def db_update(self, connection, api_output):

        cursor = connection.cursor()
        duplicate_counter = 0

        for _, data_dict in api_output.items():
            record_to_write = [data for data in data_dict.values()]
            record_title = record_to_write[0]

            if self.db_check_if_record_exists(connection,'title',record_title):
                duplicate_counter += 1
                continue
            cursor.execute(self.COMMANDS['update_table'], tuple(record_to_write))
        print('table updated')
        print(duplicate_counter, ' duplicates were found')

        connection.commit()
        cursor.close()



    def write_to_file(self, dict_data):
        with open('json_data/query_results.json', 'w') as output:
            json.dump(dict_data,output)
        print('written into file')
        for source, source_records in dict_data.items():
            count_of_results = 0
            for record in source_records.keys():
                count_of_results += 1
            print(source + ' has  ' + str(count_of_results) + ' results')