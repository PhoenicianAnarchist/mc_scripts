from . import _map
from . import minecraft

class Map(_map.MapBase):
    def __init__(self):
        super().__init__()

    def generate(self):
        m = minecraft.Map()
        m.blocks()

        self.map["xkdeco:cobblestone_path"] = m.map["minecraft:cobblestone"]
        self.map["xkdeco:cobblestone_path_stair"] = m.map["minecraft:cobblestone"]
