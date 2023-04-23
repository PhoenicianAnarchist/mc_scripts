from . import _map

class Map(_map.MapBase):
    def __init__(self):
        super().__init__()

    def generate(self):
        self.map["appliedenergistics2:sky_stone_block"] = (46, 51, 49)
