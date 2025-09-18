from cclonline import cclonline
from database import Database
import logging
from recommender import Recommender
import sqlite3
logging.basicConfig(level=logging.INFO)


sites = [cclonline()]

def update_database():
    for site in sites:
        logging.info(f"Running {site.base_url}")
        data =  site.process()
        db = Database("pcparts.db")
        db.create_connection()
        logging.info("Database connection established")
        db.create_tables()
        logging.info("Tables created in database")  
        db.update_tables(data)
        logging.info("Data updated in database")
        db.close_connection()
        logging.info("Database connection closed")

def getrecommend(totalprice, type):
    logging.info("Recommender run method started")
    conn = sqlite3.connect("pcparts.db")
    conn.row_factory = sqlite3.Row
    recommender = Recommender(conn, totalprice, type)
    recommendations = recommender.recommend()
    conn.close()
    logging.info("Recommender run method finished")
    if recommendations is None:
        logging.info("No valid build found")
        return {"error": "No valid build found"}
    return recommendations
