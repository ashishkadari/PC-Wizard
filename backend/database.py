import sqlite3
import logging
from sqlite3 import Error

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None
        self.create_connection()

    def create_connection(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            logging.info("Database connection established")
        except Error as e:
            logging.error(f"Error with connecting to database - {e}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed")

    def create_tables(self):
        try:
            cursor = self.connection.cursor()

            # Create table for CPU
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS cpu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Url TEXT,
                Boost TEXT,
                Cores INTEGER,
                Socket TEXT,
                Power TEXT,
                Price TEXT,
                GamingScore REAL,
                WorkStationScore REAL
                        
            )
            ''')

            # Create table for Motherboard
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS motherboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Url TEXT,
                Price TEXT,
                Socket TEXT,
                FormFactor TEXT,
                Chipset TEXT,
                RamType TEXT,
                GamingScore REAL,
                WorkStationScore REAL
            )
            ''')


            # Create table for SSD
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ssd (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Url TEXT,
                Price TEXT,
                Capacity TEXT,
                Interface TEXT,
                Speed TEXT,
                GamingScore REAL,
                WorkStationScore REAL
            )
            ''')

            # Create table for PSU
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS psu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Url TEXT,
                Price TEXT,
                PowerRating TEXT,
                PowerType TEXT,
                ModularType TEXT,
                FormFactor TEXT,
                GamingScore REAL,
                WorkStationScore REAL
            )
            ''')

            # Create table for RAM (DDR4)
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ddr4 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Url TEXT,
                Price TEXT,
                PowerRating TEXT,
                Latency TEXT,
                Speed TEXT,
                Capacity TEXT,
                GamingScore REAL,
                WorkStationScore REAL
            )
            ''')

            # Create table for RAM (DDR5)
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ddr5 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Url TEXT,
                Price TEXT,
                PowerRating TEXT,
                Latency TEXT,
                Speed TEXT,
                Capacity TEXT,
                GamingScore REAL,
                WorkStationScore REAL
            )
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS gpu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Url TEXT,
                Price TEXT,
                Memory TEXT,
                Capacity INTEGER,
                GDDR_Version INTEGER,
                GamingScore REAL,
                WorkStationScore REAL
            )
            ''')

            # Commit changes and close the cursor
            self.connection.commit()
            logging.info("Tables created successfully")
        except Error as e:
            logging.error(f"Error creating tables - {e}")
            self.connection.rollback()
    
    def update_tables(self, data):
        for item in data:
            
            table = item["Part"].lower()  # Using the "Part" field for the table name
            columns = [key for key in item.keys() if key != "Part"]
            values = [item[key] for key in columns]
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(values))})" 
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, values)
                self.connection.commit()
            except Error as e:
                logging.error(f"Error updating {table} table: {e}")
                self.connection.rollback() 