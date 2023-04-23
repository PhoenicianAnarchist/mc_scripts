from . import _map

from . import minecraft

class Map(_map.MapBase):
    def __init__(self):
        super().__init__()

    def generate(self):
        m = minecraft.Map()
        m.woods()
        self.map["decorative_blocks:oak_seat"] = m.map["minecraft:oak_planks"]
