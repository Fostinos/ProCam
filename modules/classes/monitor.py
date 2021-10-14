import jsonpickle
from modules.classes.monitoring import *

class Monitor:
    
    # constructor

    def __init__(self):
        self.cpu = CPU()
        self.memory = RAM()
        self.disk = DISK()
    
    # static method (return json format)
    @staticmethod
    def getJson():
        current = Monitor()
        return jsonpickle.encode(current, indent=4)
