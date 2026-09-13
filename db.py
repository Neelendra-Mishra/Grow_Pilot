import os
import psycopg
from tkinter import messagebox
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "16prem1601")
DB_NAME = os.getenv("DB_NAME", "inventory")

class PgCursorWrapper:
    """Wrapper around psycopg cursor providing backwards compatibility with MySQL queries."""
    def __init__(self, real_cursor):
        self._cursor = real_cursor

    def execute(self, query, params=None):
        q_strip = query.strip()
        # In PostgreSQL, database switching is handled during connection.
        # Silently skip MySQL-specific "USE database" statements.
        if q_strip.lower().startswith("use "):
            return self
        
        # In PyMySQL, passing a single scalar (e.g. integer or string) for %s was accepted.
        # Psycopg requires parameters to be a sequence (tuple, list) or mapping (dict).
        if params is not None and not isinstance(params, (tuple, list, dict)):
            params = (params,)
            
        return self._cursor.execute(query, params)

    def executemany(self, query, params_seq):
        return self._cursor.executemany(query, params_seq)

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def fetchmany(self, size=None):
        if size is not None:
            return self._cursor.fetchmany(size)
        return self._cursor.fetchmany()

    @property
    def rowcount(self):
        return self._cursor.rowcount

    def close(self):
        return self._cursor.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __getattr__(self, name):
        return getattr(self._cursor, name)


class PgConnectionWrapper:
    """Wrapper around psycopg connection to return wrapped cursors."""
    def __init__(self, real_conn):
        self._conn = real_conn

    def cursor(self):
        return PgCursorWrapper(self._conn.cursor())

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def close(self):
        return self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __getattr__(self, name):
        return getattr(self._conn, name)


def connect_database():
    try:
        connection = psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME,
            autocommit=False
        )
        cursor = connection.cursor()
        return PgCursorWrapper(cursor), PgConnectionWrapper(connection)
    except Exception as e:
        messagebox.showerror("Error!", f"Database connectivity issue: {e}")
        return None, None
