import json
import sqlite3
from database import Database
from backend.Tests.dataexample import data # Assuming dataexample.py contains the sample data
# Step 1: Load sample data
# This should be replaced with the actual data fetching logic
# from cclonline import cclonlinec

# Step 2: Create and setup database
db = Database("pcparts.db")
db.create_tables()
db.update_tables(data)

# Step 3: Check the output (example: show what's in the CPU table)
conn = sqlite3.connect("pcparts.db")
cursor = conn.cursor()

print("CPUs in database:")
for row in cursor.execute("SELECT * FROM cpu"):
    print(row)

print("\nSSDs in database:")
for row in cursor.execute("SELECT * FROM ssd"):
    print(row)

conn.close()