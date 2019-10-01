import psycopg2
import logging

from psycopg2 import extras

from querys import OPERATIONS_BY_MODEL, ALTER_AND_CREATE_INDEX_BY_APP

HOST = ''
DATABASE = ''
PASSWORD = ''
DATABASE_USER = ''
PORT = ''


class PostgresDBConnection(object):
    def __init__(self, host=HOST, port=PORT, database=DATABASE, user=DATABASE_USER, password=PASSWORD):
        self.connection = None
        self.errors = []
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database, 
                user=self.user,
                password=self.password,
                port=self.port
            )

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error('Postgres database connection failed: {0}'.format(error))
            self.errors.append(error)

    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            for table in OPERATIONS_BY_MODEL.keys():
                create_query = OPERATIONS_BY_MODEL[table]['CREATE']
                cursor.execute(create_query)
            self.connection.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error('CREATE TABLES MODEL {0} ERROR: {1}'.format(error, table))
            self.errors.append(error)

    def insert_model_data(self, model, model_list_values):
        try:
            cursor = self.connection.cursor()
            extras.execute_values(cursor, OPERATIONS_BY_MODEL[model]['INSERT'], model_list_values)
            self.connection.commit()
            cursor.close()
        except(Exception, psycopg2.DatabaseError) as error:
            logging.error('INSERT ERROR {0}: {1}'.format(model, error))

    def delete_tables(self):
        try:
            for table in OPERATIONS_BY_MODEL.keys():
                cursor = self.connection.cursor()
                cursor.execute(OPERATIONS_BY_MODEL[table]['DELETE'])
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error('DELETE TABLES: {0}'.format(error))

    def fetch_all_data(self):
        for model in OPERATIONS_BY_MODEL.keys():
            model_items = self.fetch_model_data(model)

    def fetch_model_data(self, model):
        try:
            cursor = self.connection.cursor()
            select_query = OPERATIONS_BY_MODEL[model]['SELECT']
            cursor.execute(select_query)
            rows = cursor.fetchall()
            return rows, len(rows) if rows else 0
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error('SELECT ERROR: {}'.format(error))

    def count_rows_in_table(self, model):
        try:
            cursor = self.connection.cursor()
            cursor.execute(OPERATIONS_BY_MODEL[model]['COUNT'])
            result = cursor.fetchone()
            return result[0]
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error('COUNT ROWS IN TABLE: {0}'.format(error))

    def execute_extra_operations_db(self):
        try:
            cursor = self.connection.cursor()
            for app in ALTER_AND_CREATE_INDEX_BY_APP.keys():
                for operation in ALTER_AND_CREATE_INDEX_BY_APP[app]['NEXT_OPERATIONS']:
                    cursor.execute(operation)
                self.connection.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error('EXTRA OPERATIONS: {0}'.format(error))
