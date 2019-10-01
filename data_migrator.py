import datetime
import json
import logging
from postgres_db_connection import PostgresDBConnection
from settings import CRAWLER_DATABASES_CONFIG
from sqlite_db_connection import SQLiteDBConnection

from querys import OPERATIONS_BY_MODEL, INSERT_BY_ORDER


class DataMigrator(object):

    def __init__(self):
        self.sqlite_conn = SQLiteDBConnection()
        self.postgres_conn = PostgresDBConnection()

    def data_bases_init(self):
        self.sqlite_conn.connect()
        self.postgres_conn.connect()

    def migrate_data(self):
        pass


class CrawlerDataMigrator(object):
    def __init__(self, **databases_connfig):
        self.postgres_conn_primary = PostgresDBConnection(**databases_connfig['primary'])
        self.postgres_conn_secondary = PostgresDBConnection(**databases_connfig['secondary'])

    def data_bases_init(self):
        self.postgres_conn_primary.connect()
        self.postgres_conn_secondary.connect()

    @staticmethod
    def dict_to_json(row):
        row = list(row)
        row[10] = json.dumps(row[10])
        row[13] = json.dumps(row[13])
        return row

    def migrate_data(self):
        self.data_bases_init()
        self.postgres_conn_secondary.delete_tables()
        self.postgres_conn_secondary.create_tables()
        records, count_records = self.postgres_conn_primary.fetch_model_data('CRAWLER_PRODUCT')
        casting_records = list(map(CrawlerDataMigrator.dict_to_json, records))
        self.postgres_conn_secondary.insert_model_data('CRAWLER_PRODUCT', casting_records)
        inserted_rows = self.postgres_conn_secondary.count_rows_in_table('CRAWLER_PRODUCT')
        logging.warning('Crawler data migration Success!') if inserted_rows == count_records else logging.error('Crawler data migration failed!')


if __name__ == '__main__':
    CrawlerDataMigrator(**CRAWLER_DATABASES_CONFIG).migrate_data()
''' start = datetime.datetime.now()
    migrator = DataMigrator()
    migrator.data_bases_init()
    migrator.postgres_conn.delete_tables()
    migrator.postgres_conn.create_tables()
    migrator.postgres_conn.execute_extra_operations_db()
    for model in INSERT_BY_ORDER:
        rows, count_rows = migrator.sqlite_conn.fetch_model_data(model)
        migrator.postgres_conn.insert_model_data(model, rows)
        inserted_rows = migrator.postgres_conn.count_rows_in_table(model)
        if count_rows != inserted_rows:
            success = False
            break
    if success:
        print('Sucess!!!')
    else:
        print('Something went wrong!!')
    end = datetime.datetime.now()
    print(abs(end - start).microseconds)
'''
