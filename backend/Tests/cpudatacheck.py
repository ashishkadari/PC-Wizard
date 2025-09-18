import sqlite3

def check_cpu_data(db_path="pcparts.db"):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("Connected to database.")

        # Show CPU count
        cursor.execute("SELECT COUNT(*) FROM cpu;")
        count = cursor.fetchone()[0]
        print(f"Total CPUs in database: {count}")

        # Fetch top 10 CPUs by price
        cursor.execute("""
            SELECT Name, Price, GamingScore, WorkStationScore
            FROM cpu
            LIMIT 10;
        """)
        rows = cursor.fetchall()

        print("\nSample CPU data:")
        for row in rows:
            name, price, gaming_score, workstation_score = row
            print(f"- {name}\n  Price: {price} | Gaming: {gaming_score} | Workstation: {workstation_score}\n")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_cpu_data()