from . import _map

class Map(_map.MapBase):
    def __init__(self):
        super().__init__()

    def generate(self):
        self.map["biomesoplenty:flowering_oak_leaves"] = (43, 61, 29)
        self.map["biomesoplenty:sprout"] = (100, 100, 100)
        self.map["biomesoplenty:toadstool"] = (164, 101, 51)
        self.map["biomesoplenty:toadstool_block"] = (196, 111, 49)

        self.flowers()
        self.woods()

    def flowers(self):
        self.map["biomesoplenty:barley"] = (219, 190, 101)
        self.map["biomesoplenty:goldenrod"] = (249, 234, 110)
        self.map["biomesoplenty:lavender"] = (151, 117, 206)

    def woods(self):
        woods = {
            ## Wood Name:   [ planks, log, stripped, leaves ]
            "jacaranda":  [(207, 181, 172), (106, 87, 80), (140, 122, 114), (154, 135, 221)]
        }

        for wood, [planks, log, stripped, leaves] in woods.items():
            self.map[f"biomesoplenty:{wood}_button"] = planks
            self.map[f"biomesoplenty:{wood}_door"] = planks
            self.map[f"biomesoplenty:{wood}_fence"] = planks
            self.map[f"biomesoplenty:{wood}_fence_gate"] = planks
            self.map[f"biomesoplenty:{wood}_hanging_sign"] = planks
            self.map[f"biomesoplenty:{wood}_planks"] = planks
            self.map[f"biomesoplenty:{wood}_pressure_plate"] = planks
            self.map[f"biomesoplenty:{wood}_sign"] = planks
            self.map[f"biomesoplenty:{wood}_slab"] = planks
            self.map[f"biomesoplenty:{wood}_stairs"] = planks
            self.map[f"biomesoplenty:{wood}_trapdoor"] = planks

            self.map[f"biomesoplenty:{wood}_leaves"] = leaves
            self.map[f"biomesoplenty:{wood}_log"] = log
            self.map[f"biomesoplenty:{wood}_sapling"] = leaves
            self.map[f"biomesoplenty:{wood}_wood"] = log
            self.map[f"biomesoplenty:stripped_{wood}_log"] = stripped
            self.map[f"biomesoplenty:stripped_{wood}_wood"] = stripped
