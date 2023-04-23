from . import _map
from . import minecraft

class Map(_map.MapBase):
    def __init__(self):
        super().__init__()

    def generate(self):
        m = minecraft.Map()
        m.bricks()
        self.map["chisel:bricks/prism"] = m.map["minecraft:bricks"]

        m.blocks_polished()
        self.map["chisel:andesite/cracked_bricks"] = m.map["minecraft:andesite"]
        self.map["chisel:andesite/soft_bricks"] = m.map["minecraft:andesite"]

        m.woods()
        self.map["chisel:planks/oak/log_cabin"] = m.map["minecraft:oak_planks"]
