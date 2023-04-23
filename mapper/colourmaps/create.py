from . import _map
from . import minecraft

class Map(_map.MapBase):
    def __init__(self):
        super().__init__()

    def generate(self):
        m = minecraft.Map()
        m.blocks_polished()
        self.andesite = m.map["minecraft:andesite"]

        m.woods()
        self.oak_planks = m.map["minecraft:oak_planks"]
        self.oak_log = m.map["minecraft:oak_log"]

        m.ores()
        self.copper_ore = m.map["minecraft:copper_ore"]

        self.ores()
        self.blocks()
        self.mechanisms()

    def ores(self):
        self.map["create:zinc_ore"] = (151, 151, 179)
        self.map["create:copper_ore"] = self.copper_ore

    def blocks(self):
        self.map["create:andesite_cobblestone"] = self.andesite
        self.map["create:weathered_limestone_cobblestone"] = (122, 124, 112)

    def mechanisms(self):
        self.map["create:shaft"] = self.andesite
        self.map["create:sail_frame"] = self.oak_planks
        self.map["create:white_sail"] = self.oak_planks
        self.map["create:linear_chassis"] = self.oak_log
        self.map["create:radial_chassis"] = self.oak_log
        self.map["create:windmill_bearing"] = self.oak_log
