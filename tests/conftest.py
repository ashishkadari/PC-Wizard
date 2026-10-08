import os
import sqlite3
import sys

import pytest

# Let the tests import modules from main/ (e.g. "from recommender import Recommender")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "main"))

SCHEMA = """
CREATE TABLE cpu (Name TEXT, Url TEXT, Price TEXT, GamingScore INTEGER, WorkStationScore INTEGER, Socket TEXT, PowerRating TEXT);
CREATE TABLE gpu (Name TEXT, Url TEXT, Price TEXT, GamingScore INTEGER, WorkStationScore INTEGER, PowerRating TEXT);
CREATE TABLE motherboard (Name TEXT, Url TEXT, Price TEXT, GamingScore INTEGER, WorkStationScore INTEGER, Socket TEXT, RamType TEXT);
CREATE TABLE ssd (Name TEXT, Url TEXT, Price TEXT, GamingScore INTEGER, WorkStationScore INTEGER);
CREATE TABLE ddr4 (Name TEXT, Url TEXT, Price TEXT, GamingScore INTEGER, WorkStationScore INTEGER, RamType TEXT);
CREATE TABLE ddr5 (Name TEXT, Url TEXT, Price TEXT, GamingScore INTEGER, WorkStationScore INTEGER, RamType TEXT);
CREATE TABLE psu (Name TEXT, Url TEXT, Price TEXT, GamingScore INTEGER, WorkStationScore INTEGER);
"""


def add(conn, table, name, price, gaming, workstation, **extra):
    cols = ["Name", "Url", "Price", "GamingScore", "WorkStationScore", *extra.keys()]
    vals = [name, "http://example.com", f"£{price}", gaming, workstation, *extra.values()]
    conn.execute(
        f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join('?' * len(vals))})",
        vals,
    )


@pytest.fixture
def db():
    """Small in-memory parts catalogue with known prices, scores and compatibility."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)

    # GPUs: the best one is expensive
    add(conn, "gpu", "GPU Fast", 400, 100, 40, PowerRating="300W")
    add(conn, "gpu", "GPU Budget", 150, 60, 20, PowerRating="150W")

    # CPUs on two different sockets
    add(conn, "cpu", "CPU AM5", 200, 80, 95, Socket="AM5", PowerRating="105W")
    add(conn, "cpu", "CPU LGA1700", 180, 85, 70, Socket="LGA1700", PowerRating="125W")

    # Motherboards: one per socket, with different RAM types
    add(conn, "motherboard", "Board AM5 DDR5", 120, 50, 50, Socket="AM5", RamType="DDR5")
    add(conn, "motherboard", "Board LGA1700 DDR4", 100, 50, 50, Socket="LGA1700", RamType="DDR4")

    add(conn, "ssd", "SSD 1TB", 60, 50, 50)
    add(conn, "ddr4", "RAM DDR4 16GB", 40, 50, 50, RamType="DDR4")
    add(conn, "ddr5", "RAM DDR5 16GB", 60, 50, 50, RamType="DDR5")
    add(conn, "psu", "PSU 750W", 70, 50, 50)

    conn.commit()
    yield conn
    conn.close()


def price(component):
    return float(component["Price"].replace("£", ""))


def total_price(build):
    return sum(price(c) for c in build.values())
