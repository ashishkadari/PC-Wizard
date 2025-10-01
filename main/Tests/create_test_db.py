import sqlite3

def create_and_populate_db(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.executescript("""
    DROP TABLE IF EXISTS cpu;
    CREATE TABLE cpu (
        ID INTEGER PRIMARY KEY,
        Name TEXT,
        Url TEXT,
        Price TEXT,
        GamingScore INTEGER,
        WorkStationScore INTEGER,
        Socket TEXT,
        PowerRating TEXT
    );

    DROP TABLE IF EXISTS gpu;
    CREATE TABLE gpu (
        ID INTEGER PRIMARY KEY,
        Name TEXT,
        Url TEXT,
        Price TEXT,
        GamingScore INTEGER,
        WorkStationScore INTEGER,
        PowerRating TEXT
    );

    DROP TABLE IF EXISTS motherboard;
    CREATE TABLE motherboard (
        ID INTEGER PRIMARY KEY,
        Name TEXT,
        Url TEXT,
        Price TEXT,
        GamingScore INTEGER,
        WorkStationScore INTEGER,
        Socket TEXT,
        RamType TEXT
    );

    DROP TABLE IF EXISTS ssd;
    CREATE TABLE ssd (
        ID INTEGER PRIMARY KEY,
        Name TEXT,
        Url TEXT,
        Price TEXT,
        GamingScore INTEGER,
        WorkStationScore INTEGER
    );

    DROP TABLE IF EXISTS ram;
    CREATE TABLE ram (
        ID INTEGER PRIMARY KEY,
        Name TEXT,
        Url TEXT,
        Price TEXT,
        GamingScore INTEGER,
        WorkStationScore INTEGER,
        RamType TEXT
    );

    DROP TABLE IF EXISTS ddr4;
    CREATE TABLE ddr4 AS SELECT * FROM ram;

    DROP TABLE IF EXISTS ddr5;
    CREATE TABLE ddr5 AS SELECT * FROM ram;

    DROP TABLE IF EXISTS psu;
    CREATE TABLE psu (
        ID INTEGER PRIMARY KEY,
        Name TEXT,
        Url TEXT,
        Price TEXT,
        GamingScore INTEGER,
        WorkStationScore INTEGER
    );
    """)

    cpu_data = [
        (1, "Ryzen 5 5600", "http://example.com/ryzen5600", "£130", 85, 75, "AM4", "65W"),
    ]
    gpu_data = [
        (1, "RTX 3060", "http://example.com/rtx3060", "£450", 90, 70, "170W"),
    ]
    mobo_data = [
        (1, "ASUS B550", "http://example.com/asusb550", "£100", 70, 60, "AM4", "DDR4"),
    ]
    ssd_data = [
        (1, "Samsung 970 Evo", "http://example.com/970evo", "£80", 70, 80),
    ]
    ram_data = [
        (1, "Corsair 16GB DDR4", "http://example.com/corsair16", "£60", 60, 65, "DDR4"),
    ]
    psu_data = [
        (1, "Corsair 650W", "http://example.com/psu650", "£75", 50, 55),
    ]

    cursor.executemany("INSERT INTO cpu VALUES (?, ?, ?, ?, ?, ?, ?, ?)", cpu_data)
    cursor.executemany("INSERT INTO gpu VALUES (?, ?, ?, ?, ?, ?, ?)", gpu_data)
    cursor.executemany("INSERT INTO motherboard VALUES (?, ?, ?, ?, ?, ?, ?, ?)", mobo_data)
    cursor.executemany("INSERT INTO ssd VALUES (?, ?, ?, ?, ?, ?)", ssd_data)
    cursor.executemany("INSERT INTO ram VALUES (?, ?, ?, ?, ?, ?, ?)", ram_data)
    cursor.executemany("INSERT INTO psu VALUES (?, ?, ?, ?, ?, ?)", psu_data)

    cursor.execute("INSERT INTO ddr4 SELECT * FROM ram")
    cursor.execute("INSERT INTO ddr5 SELECT * FROM ram")  # Just to avoid errors, even though it's DDR4

    conn.commit()
    conn.close()
    print("Test database created and populated.")

if __name__ == "__main__":
    create_and_populate_db("test_builds.db")