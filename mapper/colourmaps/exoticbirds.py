from . import _map

class Map(_map.MapBase):
    def __init__(self):
        super().__init__()

    def generate(self):
        self.map["exoticbirds:nest"] = (184, 144, 96)
