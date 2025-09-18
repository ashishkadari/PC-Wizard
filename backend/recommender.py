import logging
from sqlite3 import Error
import sqlite3

gamingOrder = ["gpu", "cpu", "motherboard", "ssd", "ram", "psu"]
workstationOrder = ["cpu", "motherboard", "ssd", "ram", "gpu", "psu"]

class Recommender:
    def __init__(self, connection, totalprice, pc_type="gaming"):
        self.connection = connection
        self.totalprice = totalprice
        self.type = pc_type
        self.type = self.type.lower()

        if not hasattr(self.connection, 'row_factory'):
            self.connection.row_factory = sqlite3.Row

    def recommend(self, currentbuild=None, componentindex=0):
        logging.info(f"[DEBUG] recommend() started with type: {self.type}")
        if currentbuild is None:
            currentbuild = {}
        
        if self.type == "gaming":
            order = gamingOrder
        elif self.type == "workstation":
            order = workstationOrder
        else:
            logging.error("Invalid type specified. Must be 'gaming' or 'workstation'.")
            return None

        if componentindex >= len(order):
            logging.info("All components have been selected")
            return currentbuild

        component = order[componentindex]
        logging.info(f"Processing component: {component}")

        candidates = self.select_all_components(component, currentbuild)
        for cand in candidates:
            currentbuild[component] = cand
            logging.info(f"Selected {component}: {cand['Name']} @ £{cand['Price']}")
            result = self.recommend(currentbuild, componentindex + 1)
            if result:
                return result
            logging.info(f"Backtracking on {component}: {cand['Name']}")
            del currentbuild[component]

        logging.info(f"No valid build found at {component}")
        return None

    def select_all_components(self, component, currentbuild):
        cursor = self.connection.cursor()
        budget_used = sum([float(currentbuild[comp]["Price"].replace('£', '')) for comp in currentbuild])
        budget_remaining = self.totalprice - budget_used

        # Query to select components within the remaining budget
        query = f"SELECT * FROM {component} WHERE CAST(REPLACE(Price,'£','') AS FLOAT) <= {budget_remaining}"

        # Filter motherboard by CPU socket type if CPU is selected
        if component == "motherboard" and "cpu" in currentbuild:
            sock = currentbuild["cpu"]["Socket"]
            query += f" AND Socket = '{sock}'"

        # For RAM, filter by type based on motherboard RAM type (DDR4/DDR5)
        if component == "ram" and "motherboard" in currentbuild:
            table = "ddr5" if "DDR5" in currentbuild["motherboard"]["RamType"] else "ddr4"
            component = table
            query = f"SELECT * FROM {component} WHERE CAST(REPLACE(Price,'£','') AS FLOAT) <= {budget_remaining}"

        # Sorting to prioritize components with higher scores (e.g., GamingScore or WorkStationScore)
        score_column = "GamingScore" if self.type == "gaming" else "WorkStationScore"
        query += f" ORDER BY {score_column} DESC, CAST(REPLACE(Price,'£','') AS FLOAT) DESC"

        try:
            logging.info(f"Executing query: {query}")
            cursor.execute(query)
            rows = cursor.fetchall()
            comps = []
            for r in rows:
                comps.append({
                    "Name": r["Name"],
                    "Url": r["Url"],
                    "Price": r["Price"],
                    "GamingScore": r["GamingScore"] if self.type == "gaming" else None,
                    "WorkStationScore": r["WorkStationScore"] if self.type == "workstation" else None,
                    "Socket": r["Socket"] if "Socket" in r.keys() else None,
                    "PowerRating": r["PowerRating"] if "PowerRating" in r.keys() else None,
                    "RamType": r["RamType"] if "RamType" in r.keys() else None
                })
            return comps
        except Error as e:
            logging.error(f"Error with selecting components - {e}")
            return []

    def calculate_power_requirements(self, currentbuild):
        total_power = 0
        if "cpu" in currentbuild:
            cpu_p = currentbuild["cpu"].get("PowerRating", 0)
            if isinstance(cpu_p, str) and cpu_p.endswith("W"):
                cpu_p = int(cpu_p[:-1])
            total_power += cpu_p
        logging.info(f"Total power requirement: {total_power}W")
        return total_power