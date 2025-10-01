class Utility:
    def __init__(self):
        pass
    def get_gaming_component_price(self, totalprice):
        dict = {
            "gpu": 0.38*totalprice,
            "cpu": 0.3*totalprice,   
            "motherboard": 0.05*totalprice, 
            "ram": 0.12*totalprice,
            "ssd": 0.1*totalprice,
            "psu": 0.05*totalprice
        }
        return dict
    def get_workstation_component_price(self, totalprice):
        dict = {
            "gpu": 0.2*totalprice,
            "cpu": 0.4*totalprice,   
            "motherboard": 0.1*totalprice, 
            "ram": 0.15*totalprice,
            "ssd": 0.1*totalprice,
            "psu": 0.05*totalprice
        }
        return dict
