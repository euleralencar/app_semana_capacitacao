import os

import psycopg
from psycopg.rows import dict_row


class DatabaseConfigurationError(RuntimeError):
    pass


class Database:
    def __init__(self, connection_url):
        self.connection_url = connection_url

    @classmethod
    def from_environment(cls):
        connection_url = os.getenv("DATABASE_URL")
        if not connection_url:
            raise DatabaseConfigurationError("DATABASE_URL não configurada.")
        return cls(connection_url)

    def execute(self, query, params=None):
        with psycopg.connect(self.connection_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)

    def fetch_one(self, query, params=None):
        with psycopg.connect(self.connection_url, row_factory=dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()

    def fetch_all(self, query, params=None):
        with psycopg.connect(self.connection_url, row_factory=dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()

