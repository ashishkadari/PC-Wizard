import sqlite3
import logging

# Set up logging to show info in console
logging.basicConfig(level=logging.INFO)

def check_ssd_data(db_path="pcparts.db"):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        logging.info("Connected to database.")

        # Show SSD count
        cursor.execute("SELECT COUNT(*) FROM ssd;")
        count = cursor.fetchone()[0]
        logging.info(f"Total SSDs in database: {count}")

        # Fetch all SSD data
        cursor.execute("""
            SELECT Name, Price, Capacity, Speed, GamingScore, WorkStationScore
            FROM ssd;
        """)
        rows = cursor.fetchall()

        logging.info("\nAll SSDs data:")
        for row in rows:
            name, price, capacity, speed, gaming_score, workstation_score = row
            logging.info(f"- {name}\n  Price: {price} | Capacity: {capacity} | Speed: {speed} | GamingScore: {gaming_score} | WorkStationScore: {workstation_score}\n")

    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_ssd_data()