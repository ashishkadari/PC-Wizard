import sqlite3

def check_gpu_data(db_path="pcparts.db"):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("Connected to database.")

        # Show GPU count
        cursor.execute("SELECT COUNT(*) FROM gpu;")
        count = cursor.fetchone()[0]
        print(f"Total GPUs in database: {count}")

        # Fetch top 10 GPUs by price
        cursor.execute("""
            SELECT Name, Price, GamingScore, WorkStationScore
            FROM gpu
            LIMIT 10;
        """)
        rows = cursor.fetchall()

        print("\nSample GPU data:")
        for row in rows:
            name, price, gaming_score, workstation_score = row
            print(f"- {name}\n  Price: {price} | Gaming: {gaming_score} | Workstation: {workstation_score}\n")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_gpu_data()