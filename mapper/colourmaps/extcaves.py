from . import _map
from . import minecraft

class Map(_map.MapBase):
    def __init__(self):
        super().__init__()

    def generate(self):
        m = minecraft.Map()
        m.blocks()

        self.map["extcaves:brokenstone"] = m.map["minecraft:cobblestone"]
        self.map["extcaves:rockpile_three_stone"] = m.map["minecraft:cobblestone"]
