import sqlite3
from sqlite3 import Error

# SQLite database configuration
DB_FILE = "transactions.db"

DB_SCHEMA = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        currency TEXT NOT NULL,
        amount REAL NOT NULL,
        remaining_ttl INTEGER NOT NULL
    )
"""


DEFAULT_TTL = 10

# PostgreSQL database configuration
# DB_HOST = "your_postgresql_host"
# DB_PORT = "your_postgresql_port"
# DB_NAME = "your_postgresql_database"
# DB_USER = "your_postgresql_user"
# DB_PASSWORD = "your_postgresql_password"

class Database:
    def __init__(self):
        self.conn = self.create_connection()

    def create_connection(self):
        try:
            return sqlite3.connect(DB_FILE)
        except Error as e:
            print(e)
            return None

        # PostgreSQL connection
        # conn = psycopg2.connect(
        #     host=DB_HOST,
        #     port=DB_PORT,
        #     database=DB_NAME,
        #     user=DB_USER,
        #     password=DB_PASSWORD
        # )
        # return conn

    def close_connection(self):
        if self.conn:
            self.conn.close()

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(DB_SCHEMA)
            self.conn.commit()
            cursor.close()
        except Error as e:
            print(e)
    
    def add_pending_transaction(self, currency, amount):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO transactions (currency, amount, remaining_ttl)
                VALUES (?, ?, ?)
                """,
                (currency, amount, DEFAULT_TTL)
            )
            self.conn.commit()
            cursor.close()
        except Error as e:
            print(e)

    def remove_expired_transactions(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                DELETE FROM transactions
                WHERE remaining_ttl = 0
                """
            )
            self.conn.commit()
            cursor.close()
        except Error as e:
            print(e)

    def get_transactions(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM transactions")
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except Error as e:
            print(e)
            return []

    def initialize_database(self):
        self.create_table()