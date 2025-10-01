from scraper import Scraper
import logging
import re
# This is a scraper for CCL Online, a UK-based online computer hardware retailer.

#links!
#  "cpu" : "https://www.cclonline.com/pc-components/cpu-processors/"
#  "ddr4" : "https://www.cclonline.com/pc-components/memory/desktop-memory/ddr4-desktop-memory/"
#  "ddr5" : "https://www.cclonline.com/pc-components/memory/desktop-memory/ddr5-desktop-memory/"
#  "ssd" : "https://www.cclonline.com/storage/solid-state-drives-ssds/"
#  "motherboard" : "https://www.cclonline.com/pc-components/motherboards/"
#  "psu" : "https://www.cclonline.com/pc-components/power-supplies/"

def safe_xpath(item, path, index=0):
    try:
        result = item.xpath(path)
        return result[index].strip() if result and len(result) > index else None
    except Exception:
        return None

class cclonline(Scraper):
    def __init__(self):
        logging.info("cclonline initialised")
        super().__init__()
        self.base_url = "https://www.cclonline.com/"

    def components(self):
        return {"cpu":"pc-components/cpu-processors/", "ddr4" : "pc-components/memory/desktop-memory/ddr4-desktop-memory/", "ddr5"  : "pc-components/memory/desktop-memory/ddr5-desktop-memory/", "ssd" : "storage/solid-state-drives-ssds/", "motherboard" : "pc-components/motherboards/", "psu" : "pc-components/power-supplies/", "gpu" : "pc-components/graphics-cards/"}
        # "ddr4" : "memory/desktop-memory/ddr4-desktop-memory/", "ddr5"  : "memory/desktop-memory/ddr5-desktop-memory/", "ssd" : "storage/solid-state-drives-ssds/", "hdd" : "storage/hard-drives/", "motherboard" : "motherboards/", "psu" : "power-supplies/"} 

    
    def process(self):
        components = self.components()
        output = []
        for key, value in components.items():
            found_items = []

            logging.info(f"Looking for {key}")
            page = 1
            dom = self.scrape(url=f"{self.base_url}{value}page_{page}")
            items = dom.xpath("(//div[contains(@class,'product-card-wrapper product-card-v2')])")
            i = 1
            logging.info(f"Total items found: {len(items)}")
            if len(items) == 0:
                logging.info("Requests library failed, attempting with selenium")
                dom = self.scrape_with_selenium(url=f"{self.base_url}{value}page_{page}")
                items = dom.xpath("(//div[contains(@class,'product-card-wrapper product-card-v2')])")
                logging.info(f"Total items found: {len(items)}")
                found_items += items
                while len(items) > 0:
                    page += 1
                    dom = self.scrape_with_selenium(url=f"{self.base_url}{value}page_{page}")
                    items = dom.xpath("(//div[contains(@class,'product-card-wrapper product-card-v2')])")
                    logging.info(f"Total items found: {len(items)}")
                    found_items += items


            for item in found_items:

                unavailable = False
                PName = safe_xpath(item, ".//h3/a/text()")
                Url = safe_xpath(item, ".//h3/a/@href")

                price_part1 = item.xpath(".//div[contains(@class, 'price d-inline-block mr-3')]/p/span[2]/text()")
                price_part2 = item.xpath(".//div[contains(@class, 'price d-inline-block mr-3')]/p/span[3]/text()")
                
                Price = price_part1[0].strip() + price_part2[0].strip() if price_part1 and price_part2 else "N/A"
                Price = Price.replace("£", "").replace(",", "").strip() if Price else "N/A"
                if Price == "N/A":
                    unavailable = True
            

                Memory = Boost = Cores = Socket = PowerRating = PowerType = ModularType = Speed = Capacity = Latency = Interface = FormFactor = RamType = Chipset = GamingScore = WorkStationScore = None

                if key == "cpu":
                    Boost = safe_xpath(item, ".//ul/li[1]/text()")
                    Cores = safe_xpath(item, ".//ul/li[2]/text()")
                    match = re.search(r'(\d+(\.\d+)?)\s*GHz', Boost or "")
                    boost_val = float(match.group(1)) if match else 0
                    logging.info(f"Boost: {boost_val}")
                    match = re.search(r'(\d+)', Cores or "")
                    cores_val = float(match.group(0)) if match else 0   
                    logging.info(f"Cores: {cores_val}")
                    GamingScore = boost_val * 1000 * 0.6 + cores_val * 10 * 0.3
                    WorkStationScore = cores_val * 15 * 0.6 + boost_val * 1000 * 0.3

                if key in ["cpu", "motherboard"]:
                    Socket = safe_xpath(item, ".//ul/li[3]/text()")

                if key in ["ddr4", "ddr5"]:
                    PowerRating = safe_xpath(item, ".//ul/li[1]/text()")
                    Latency = safe_xpath(item, ".//ul/li[2]/text()")
                    match = re.search(r'\d+GB', PName or "")
                    Capacity = match.group(0) if match else None
                    Speed = safe_xpath(item, ".//ul/li[3]/text()")
                    match = re.search(r"(\d+)\s*(MHz|MT/s)", Speed or "")
                    speed_val = int(match.group(1)) if match else 0
                    Speed = speed_val
                    match = re.search(r'(\d+)', Capacity or "")
                    capacity_val = int(match.group(0)) if match else 0
                    GamingScore = speed_val * 0.05
                    WorkStationScore = capacity_val * 0.3 + speed_val * 0.1

                if key == "ssd":
                    Interface = safe_xpath(item, ".//ul/li[1]/text()")
                    match = re.search(r'(\d+(?:\.\d+)?)\s*(TB|GB)', PName or "")
                    if match:
                        size = float(match.group(1))
                        unit = match.group(2)
                        if unit == "TB":
                            size *= 1000
                        Capacity = int(size)
                    Speed = safe_xpath(item, ".//ul/li[3]/text()")
                    speed_val = int(re.search(r'(\d+)', Speed or "0").group(0)) if Speed else 0
                    Speed = speed_val
                    WorkStationScore = speed_val * 0.05 + Capacity * 0.01
                    GamingScore = speed_val * 0.03 + Capacity * 0.01

                if key == "motherboard":
                    FormFactor = safe_xpath(item, ".//ul/li[1]/text()")
                    Chipset = safe_xpath(item, ".//ul/li[2]/text()")
                    RamType = safe_xpath(item, ".//ul/li[4]/text()")
                    GamingScore = 0
                    WorkStationScore = 0

                if key == "psu":
                    FormFactor = safe_xpath(item, ".//ul/li[1]/text()")
                    match = re.search(r'\d+W', PName or "")
                    if match:
                        PowerRating = match.group(0)
                    match = re.search(r'\b(gold|bronze|silver|platinum)\b', PName or "", re.IGNORECASE)
                    if match:
                        PowerType = match.group(0).capitalize()
                    modular_check = safe_xpath(item, ".//ul/li[2]/text()")
                    if modular_check == "Fully Modular":
                        ModularType = modular_check
                    GamingScore = 0
                    WorkStationScore = 0

                if key == "gpu":
                    Capacity = 0
                    Modifier = 1.0
                    Memory = safe_xpath(item, ".//ul/li[1]/text()")
                    match = re.search(r'(\d+)\s*GB', Memory or "")
                    if match:
                        Capacity = int(match.group(1))
                    if "OC" in PName:
                        Modifier = 1.2
                    match = re.search(r'GDDR(\d+)', Memory)
                    if match:
                        gddr_version = int(match.group(1))
                    else:
                        gddr_version = 5
                    GamingScore = gddr_version * 0.1 + int(Capacity) * 0.05 * Modifier
                    WorkStationScore = int(Capacity) * 0.1 + gddr_version * 0.05 * Modifier
                if unavailable == True:
                    Price = "N/A"
                    GamingScore = 0
                    WorkStationScore = 0
                else:   
                    tempdict = {
                        "Part": key,
                        "Name": PName,
                        "Price": Price,
                        "Boost": Boost,
                        "Cores": Cores,
                        "Socket": Socket,
                        "PowerRating": PowerRating,
                        "Url": Url,
                        "Speed": Speed,
                        "Capacity": Capacity,
                        "Latency": Latency,
                        "Interface": Interface,
                        "FormFactor": FormFactor,
                        "RamType": RamType,
                        "Chipset": Chipset,
                        "PowerType": PowerType,
                        "ModularType": ModularType,
                        "Memory": Memory,
                        "GamingScore": GamingScore,
                        "WorkStationScore": WorkStationScore
                    }

                for k in list(tempdict.keys()):
                    if tempdict[k] is None:
                        del tempdict[k]

                output.append(tempdict)
                logging.info(tempdict)
                i += 1

        return output
