import sqlite3
import logging
from sqlite3 import Error

# SQLite database configuration
DB_FILE = "transactions.db"

DB_PENDING_SCHEMA = """
    CREATE TABLE IF NOT EXISTS crypto_pending_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        currency TEXT NOT NULL,
        amount REAL NOT NULL,
        remaining_ttl INTEGER NOT NULL
    )
"""

DB_PROCESSED_SCHEMA = """
CREATE TABLE IF NOT EXISTS crypto_processed_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        currency TEXT NOT NULL,
        amount REAL NOT NULL,
        transaction_hash TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        from_address TEXT NOT NULL,
        to_address TEXT NOT NULL
    )
"""


DEFAULT_TTL = 10



class Database:
    def __init__(self):
        self.conn = self.create_connection()

    def create_connection(self):
        try:
            return sqlite3.connect(DB_FILE)
        except Error as e:
            print(e)
            return None


    def close_connection(self):
        if self.conn:
            self.conn.close()
    
    def fetch_transaction_hashes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT transaction_hash FROM crypto_processed_transactions")
        hashlist = [str(row[0]) for row in cursor.fetchall()]
        return set(hashlist)

    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(DB_PROCESSED_SCHEMA)
            self.conn.commit()
            cursor.execute(DB_PENDING_SCHEMA)
            self.conn.commit()
            cursor.close()
        except Error as e:
            print(e)
    
    def add_processed_transaction(self, currency, amount, transaction_hash, timestamp, from_address, to_address):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO crypto_processed_transactions (currency, amount, transaction_hash, timestamp, from_address, to_address)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
            (currency, amount, transaction_hash, timestamp, from_address, to_address))
            self.conn.commit()
            cursor.close()
        except Error as e:
            print(e)
    
    def add_pending_transaction(self, currency, amount):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO crypto_pending_transactions (currency, amount, remaining_ttl)
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
                DELETE FROM crypto_pending_transactions
                WHERE remaining_ttl <= 0
                """
            )
            self.conn.commit()
            cursor.close()
        except Error as e:
            print(e)

    def get_transactions(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM crypto_processed_transactions")
            rows = cursor.fetchall()
            cursor.execute("SELECT * FROM crypto_pending_transactions")
            rows += cursor.fetchall()
            cursor.close()
            return rows
        except Error as e:
            print(e)
            return []

    def update_transactions_ttl(self, tick_interval):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                UPDATE crypto_pending_transactions
                SET remaining_ttl = remaining_ttl - ?
                WHERE remaining_ttl > 0
                """,
                (tick_interval,)
            )
            self.conn.commit()
            cursor.close()
        except Error as e:
            print(e)

    def initialize_database(self):
        self.create_tables()
    
    