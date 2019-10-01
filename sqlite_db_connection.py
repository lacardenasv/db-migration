import sqlite3
import logging
from sqlite3 import Error

from querys import OPERATIONS_BY_MODEL

DB_FILE = '/home/laura-angelica/Documents/Liminal/Backups/db_prueba.sqlite3'


class SQLiteDBConnection(object):
    def __init__(self):
        self.connection = None
        self.errors = []

    def connect(self):
        try:
            self.connection = sqlite3.connect(DB_FILE)
        except Error as error:
            logging.error('SQLite database connection failed {0}'.format(error))
            self.errors.append(error)

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
        except (Exception, sqlite3.DatabaseError) as error:
            logging.error('SELECT ERROR: {}'.format(error))
