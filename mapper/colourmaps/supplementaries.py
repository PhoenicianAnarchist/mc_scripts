from . import _map

class Map(_map.MapBase):
    def __init__(self):
        super().__init__()

    def generate(self):
        self.map["supplementaries:sack"] = (199, 159, 105)
