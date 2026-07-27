import os

import psycopg
from psycopg import pool
from psycopg.rows import dict_row


class DatabaseConfigurationError(RuntimeError):
    pass


class Database:
    _pool = None

    def __init__(self, connection_pool):
        self.connection_pool = connection_pool

    @classmethod
    def from_environment(cls):
        connection_url = os.getenv("DATABASE_URL")
        if not connection_url:
            raise DatabaseConfigurationError("DATABASE_URL não configurada.")
        
        if cls._pool is None:
            cls._pool = pool.SimpleConnectionPool(1, 20, connection_url)
        
        return cls(cls._pool)

    def execute(self, query, params=None):
        with self.connection_pool.getconn() as connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    connection.commit()
            except Exception:
                connection.rollback()
                raise
            finally:
                self.connection_pool.putconn(connection)

    def fetch_one(self, query, params=None):
        with self.connection_pool.getconn() as connection:
            try:
                with connection.cursor(row_factory=dict_row) as cursor:
                    cursor.execute(query, params)
                    return cursor.fetchone()
            finally:
                self.connection_pool.putconn(connection)

    def fetch_all(self, query, params=None):
        with self.connection_pool.getconn() as connection:
            try:
                with connection.cursor(row_factory=dict_row) as cursor:
                    cursor.execute(query, params)
                    return cursor.fetchall()
            finally:
                self.connection_pool.putconn(connection)
