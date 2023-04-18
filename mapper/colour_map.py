import logging

class ColourMap:
    map = {
        "DEFAULT": (255, 50, 255),
        "ERROR": (50, 255, 255),
        "minecraft:air": (0, 0, 0),
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        woods = [
            ["oak", (181, 146, 91), (76, 59, 34), (43, 61, 29)]
        ]

        for wood, planks, log, leaves in woods:
            self.map[f"minecraft:{wood}_button"] = planks
            self.map[f"minecraft:{wood}_door"] = planks
            self.map[f"minecraft:{wood}_fence"] = planks
            self.map[f"minecraft:{wood}_fence_gate"] = planks
            self.map[f"minecraft:{wood}_leaves"] = leaves
            self.map[f"minecraft:{wood}_log"] = log
            self.map[f"minecraft:{wood}_planks"] = planks
            self.map[f"minecraft:{wood}_pressure_plate"] = planks
            self.map[f"minecraft:{wood}_sapling"] = leaves
            self.map[f"minecraft:{wood}_sign"] = planks
            self.map[f"minecraft:{wood}_slab"] = planks
            self.map[f"minecraft:{wood}_stairs"] = planks
            self.map[f"minecraft:{wood}_trapdoor"] = planks
            self.map[f"minecraft:{wood}_wood"] = log

    def __getitem__(self, key):
        if key not in ColourMap.map:
            self.logger.error(f"No colour found for {key}")
            return ColourMap.map["DEFAULT"]

        return ColourMap.map[key]
