import os
import urllib.parse

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

    def _connect(self):
        url = self.connection_url.strip()
        if not url:
            raise DatabaseConfigurationError("DATABASE_URL vazia.")
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in {"postgres", "postgresql"}:
            raise DatabaseConfigurationError("DATABASE_URL inválida.")
        return psycopg.connect(url)

    def execute(self, query, params=None):
        with self._connect() as connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    connection.commit()
            except Exception:
                connection.rollback()
                raise

    def fetch_one(self, query, params=None):
        with self._connect() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()

    def fetch_all(self, query, params=None):
        with self._connect() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
