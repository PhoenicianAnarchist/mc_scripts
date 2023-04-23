from . import _map

class Map(_map.MapBase):
    def __init__(self):
        super().__init__()

    def generate(self):
        self.map["randomium:randomium_ore"] = (104, 24, 123)
